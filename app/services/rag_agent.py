from langchain.memory import RedisChatMessageHistory, ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.schema import SystemMessage
from qdrant_client import QdrantClient
from langchain.vectorstores import Qdrant
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA

import os


def get_rag_agent(user_id="default"):
    # Memory Layer
    redis_url = os.getenv("REDIS_URL")
    message_history = RedisChatMessageHistory(session_id=user_id, url=redis_url)
    memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=message_history, return_messages=True)

    # Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Vector DB
    qdrant = Qdrant(
        client=QdrantClient(url=os.getenv("VECTOR_DB_HOST")),
        collection_name="documents",
        embeddings=embeddings
    )

    retriever = qdrant.as_retriever()

    # Tool: Document search
    doc_search_tool = Tool(
        name="SearchDocs",
        func=lambda q: retriever.get_relevant_documents(q),
        description="Search relevant documents"
    )

    # Agent
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    agent = initialize_agent(
        tools=[doc_search_tool],
        llm=llm,
        memory=memory,
        agent="chat-conversational-react-description",
        verbose=True
    )
    return agent
