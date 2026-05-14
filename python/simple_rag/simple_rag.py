# ============================================================
# 最小化 RAG 系统：LangChain v1.2 + ollama + Chroma
# 环境准备（建议在虚拟环境中运行）：
# pip install langchain==1.2.* langchain-deepseek langchain_classic langchain_ollama langchain-chroma chromadb python-dotenv
# ============================================================

import os
#from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama,OllamaEmbeddings

from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

# ------------------------------
# 0. 从 .env 文件加载 大模型 API Key
# ------------------------------
#load_dotenv()  # 自动寻找项目根目录下的 .env 文件并加载环境变量
# 检查 key 是否已设置（比如 DeepSeek 组件会自动读取该环境变量）
#if not os.getenv("OPENAI_API_KEY"):
#    raise ValueError("请创建 .env 文件并在其中设置 DEEPSEEK_API_KEY=你的key")

# ------------------------------
# 1. 加载文档 knowledge.txt
# ------------------------------
print("Step 1: 加载文档...")
loader = TextLoader("knowledge.txt", encoding="utf-8")
documents = loader.load()  # 返回一个 Document 列表
print(f"  共加载 {len(documents)} 个文档")

# ------------------------------
# 2. 文本分割 (Text Splitting)
# ------------------------------
print("Step 2: 文本分割...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,          # 每个块的最大字符数
    chunk_overlap=50,        # 块之间的重叠字符数
    separators=["\n\n", "\n", "。", "！", "？", "，", " ", ""]  # 分隔符优先级
)
chunks = text_splitter.split_documents(documents)
print(f"  共生成 {len(chunks)} 个文本块")

# ------------------------------
# 3. 创建向量存储 (Embedding + Chroma)
# ------------------------------
print("Step 3: 创建向量存储...")
# 使用 ollama qwen3-embedding 的嵌入模型，key 已通过环境变量传入
embeddings = OllamaEmbeddings(
       model="qwen3-embedding:4b",
       dimensions=1024,
)

# 创建 Chroma 向量数据库（持久化到本地目录，可复用）
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"  # 持久化存储路径，不需要可省略
)
print(f"  向量存储创建完成，文档数: {vectorstore._collection.count()}")

# ------------------------------
# 4. 构建检索器
# ------------------------------
print("Step 4: 构建检索器...")
retriever = vectorstore.as_retriever(
    search_type="similarity",   # 相似度搜索
    search_kwargs={"k": 4}      # 返回最相似的 4 个块
)

# ------------------------------
# 5. 构建 RAG 问答链 (RetrievalQA)
# ------------------------------
print("Step 5: 构建 RAG 问答链...")

llm = ChatOllama(
    model="qwen3:4b",      
    temperature=0.0,            # 生成稳定性，可适当调整
)

# 自定义提示模板（可选）
prompt_template = """使用以下已知信息来回答问题。
如果无法从已知信息中得到答案，请直接说"不知道"，不要编造内容。

已知信息：
{context}

问题：{question}
回答："""
PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

# 组合成 RetrievalQA 链
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",                # 将所有检索到的文档拼入 prompt
    retriever=retriever,
    return_source_documents=True,      # 返回引用来源（方便调试）
    chain_type_kwargs={"prompt": PROMPT}
)
print("  RAG 链构建完成！")

# ------------------------------
# 6. 测试问答
# ------------------------------
print("\n" + "="*50)
print("开始问答测试（输入 'exit' 退出）")
print("="*50)

while True:
    user_query = input("\n请输入你的问题: ")
    if user_query.lower() in ("exit", "quit", "q"):
        break
    # 执行问答
    result = qa_chain.invoke({"query": user_query})
    print(f"\n回答: {result['result']}")
    # 如果想查看来源文档，取消下面注释
    # for i, doc in enumerate(result["source_documents"]):
    #     print(f"来源{i+1}: {doc.page_content[:100]}...")