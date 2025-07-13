import chromadb
from chromadb.config import Settings
from openai import OpenAI
import os


class FinancialSituationMemory:
    def __init__(self, name, config):
        self.config = config
        self.llm_provider = config.get("llm_provider", "openai").lower()
        
        if config["backend_url"] == "http://localhost:11434/v1":
            self.embedding = "nomic-embed-text"
            self.client = OpenAI(base_url=config["backend_url"])
            self.embedding_client = None
        elif config["backend_url"] == "https://api.modelarts-maas.com/v1":
            # DeepSeek不支持embedding，使用简单的文本匹配作为备选
            self.embedding = None
            self.client = None
            self.embedding_client = None
        elif self.llm_provider == "google":
            # Google使用langchain-google-genai的embedding
            self.embedding = "text-embedding-004"
            self.client = None  # Google不使用OpenAI客户端
            try:
                from langchain_google_genai import GoogleGenerativeAIEmbeddings
                self.embedding_client = GoogleGenerativeAIEmbeddings(
                    model="models/text-embedding-004",
                    google_api_key=os.getenv("GOOGLE_API_KEY")
                )
            except ImportError:
                raise ImportError("请安装langchain-google-genai包: pip install langchain-google-genai")
        else:
            self.embedding = "text-embedding-3-small"
            self.client = OpenAI(base_url=config["backend_url"])
            self.embedding_client = None
        
        self.chroma_client = chromadb.Client(Settings(allow_reset=True))
        self.situation_collection = self.chroma_client.create_collection(name=name)

    def get_embedding(self, text):
        """Get embedding for a text using the configured provider"""
        
        # 截断文本以避免超过API限制
        # Google embedding API限制: 36000字节
        # OpenAI embedding API限制: ~8000 tokens (约32000字符)
        max_length = 30000 if self.llm_provider == "google" else 30000
        
        if len(text) > max_length:
            print(f"警告: 文本长度({len(text)})超过限制({max_length})，将进行截断")
            text = text[:max_length] + "..."
        
        if self.llm_provider == "google":
            # 使用Google的embedding API
            try:
                embedding = self.embedding_client.embed_query(text)
                return embedding
            except Exception as e:
                print(f"Google embedding error: {e}")
                print("尝试使用OpenAI兼容的embedding作为备选方案...")
                # 如果Google embedding失败，尝试使用OpenAI作为备选
                try:
                    from openai import OpenAI
                    fallback_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                    response = fallback_client.embeddings.create(
                        model="text-embedding-3-small", input=text
                    )
                    return response.data[0].embedding
                except Exception as fallback_e:
                    print(f"备选embedding也失败: {fallback_e}")
                    # 如果都失败了，返回一个零向量作为默认值
                    print("返回默认零向量")
                    return [0.0] * 1536  # OpenAI embedding维度
        elif self.config["backend_url"] == "https://api.modelarts-maas.com/v1":
            # DeepSeek不支持embedding，使用简单的文本哈希作为代替
            # 这是一个简单的备选方案，不依赖外部API
            import hashlib
            hash_obj = hashlib.sha256(text.encode('utf-8'))
            hash_hex = hash_obj.hexdigest()
            
            # 将哈希值转换为1536维的向量（与OpenAI embedding兼容）
            embedding = []
            for i in range(0, len(hash_hex), 2):
                # 每两个字符作为一个十六进制数，转换为-1到1之间的浮点数
                hex_val = int(hash_hex[i:i+2], 16)
                normalized_val = (hex_val - 127.5) / 127.5
                embedding.append(normalized_val)
            
            # 补充到1536维
            while len(embedding) < 1536:
                embedding.extend(embedding)
            
            return embedding[:1536]
        else:
            # 使用OpenAI格式的embedding API
            response = self.client.embeddings.create(
                model=self.embedding, input=text
            )
            return response.data[0].embedding

    def add_situations(self, situations_and_advice):
        """Add financial situations and their corresponding advice. Parameter is a list of tuples (situation, rec)"""

        situations = []
        advice = []
        ids = []
        embeddings = []

        offset = self.situation_collection.count()

        for i, (situation, recommendation) in enumerate(situations_and_advice):
            situations.append(situation)
            advice.append(recommendation)
            ids.append(str(offset + i))
            embeddings.append(self.get_embedding(situation))

        self.situation_collection.add(
            documents=situations,
            metadatas=[{"recommendation": rec} for rec in advice],
            embeddings=embeddings,
            ids=ids,
        )

    def get_memories(self, current_situation, n_matches=1):
        """Find matching recommendations using configured embedding method"""
        
        # 检查是否有数据
        if self.situation_collection.count() == 0:
            return []
        
        if self.config["backend_url"] == "https://api.modelarts-maas.com/v1":
            # DeepSeek不支持embedding，使用简单的文本匹配
            # 获取所有存储的情况
            all_results = self.situation_collection.get(include=["metadatas", "documents"])
            
            if not all_results["documents"]:
                return []
            
            # 计算简单的文本相似度（基于共同关键词）
            import re
            current_keywords = set(re.findall(r'\b\w+\b', current_situation.lower()))
            
            similarities = []
            for i, doc in enumerate(all_results["documents"]):
                doc_keywords = set(re.findall(r'\b\w+\b', doc.lower()))
                # 计算Jaccard相似度
                intersection = current_keywords.intersection(doc_keywords)
                union = current_keywords.union(doc_keywords)
                similarity = len(intersection) / len(union) if union else 0
                
                similarities.append({
                    "matched_situation": doc,
                    "recommendation": all_results["metadatas"][i]["recommendation"],
                    "similarity_score": similarity,
                    "index": i
                })
            
            # 按相似度排序
            similarities.sort(key=lambda x: x["similarity_score"], reverse=True)
            
            # 返回前n_matches个结果
            return similarities[:n_matches]
        else:
            # 使用embedding进行相似性搜索
            query_embedding = self.get_embedding(current_situation)

            results = self.situation_collection.query(
                query_embeddings=[query_embedding],
                n_results=n_matches,
                include=["metadatas", "documents", "distances"],
            )

            matched_results = []
            for i in range(len(results["documents"][0])):
                matched_results.append(
                    {
                        "matched_situation": results["documents"][0][i],
                        "recommendation": results["metadatas"][0][i]["recommendation"],
                        "similarity_score": 1 - results["distances"][0][i],
                    }
                )

            return matched_results


if __name__ == "__main__":
    # Example usage
    matcher = FinancialSituationMemory()

    # Example data
    example_data = [
        (
            "High inflation rate with rising interest rates and declining consumer spending",
            "Consider defensive sectors like consumer staples and utilities. Review fixed-income portfolio duration.",
        ),
        (
            "Tech sector showing high volatility with increasing institutional selling pressure",
            "Reduce exposure to high-growth tech stocks. Look for value opportunities in established tech companies with strong cash flows.",
        ),
        (
            "Strong dollar affecting emerging markets with increasing forex volatility",
            "Hedge currency exposure in international positions. Consider reducing allocation to emerging market debt.",
        ),
        (
            "Market showing signs of sector rotation with rising yields",
            "Rebalance portfolio to maintain target allocations. Consider increasing exposure to sectors benefiting from higher rates.",
        ),
    ]

    # Add the example situations and recommendations
    matcher.add_situations(example_data)

    # Example query
    current_situation = """
    Market showing increased volatility in tech sector, with institutional investors 
    reducing positions and rising interest rates affecting growth stock valuations
    """

    try:
        recommendations = matcher.get_memories(current_situation, n_matches=2)

        for i, rec in enumerate(recommendations, 1):
            print(f"\nMatch {i}:")
            print(f"Similarity Score: {rec['similarity_score']:.2f}")
            print(f"Matched Situation: {rec['matched_situation']}")
            print(f"Recommendation: {rec['recommendation']}")

    except Exception as e:
        print(f"Error during recommendation: {str(e)}")
