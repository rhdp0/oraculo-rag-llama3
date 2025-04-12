import streamlit as st
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate

# 1. Carregar os dados do CSV
@st.cache_data
def load_csv_data():
    loader = CSVLoader(file_path="knowledge_base.csv", encoding="utf8")
    documents = loader.load()

    # 2. Embeddings locais
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # 3. Vetorização
    vectorstore = FAISS.from_documents(documents, embeddings)
    retriever = vectorstore.as_retriever()
    return retriever

retriever = load_csv_data()
st.title("Oráculo - NeoTech Solutions")

# 4. Modelo de linguagem (LLaMA 3 rodando via Ollama)
llm = ChatOllama(model="llama3:8b-instruct-q4_K_S")

# Configuração do prompt e do modelo
rag_prompt = """
Você é um atendente de uma empresa.
Seu trabalho é conversar com os clientes, consultando a base de conhecimento da empresa, e dar
uma resposta simples e precisa para ele, baseado na base de dados da empresa fornecida como contexto.

Contexto: {context}

question: {question}
"""

human = "{text}"
prompt = PromptTemplate.from_template(rag_prompt)

# 6. Construção da cadeia RAG
chain = (
    {
        "context": lambda x: retriever.invoke(x["question"]),
        "question": lambda x: x["question"]
    }
    | prompt
    | llm
)

# --------------- Interface com streamlit ---------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe mensagens do histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Caixa de entrada para o usuário
if user_input := st.chat_input("Você:"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Adiciona um container para a resposta do modelo
    response_stream = chain.stream({"question": user_input})    
    full_response = ""
    
    response_container = st.chat_message("assistant")
    response_text = response_container.empty()
    
    for partial_response in response_stream:
        full_response += str(partial_response.content)
        response_text.markdown(full_response + "▌")

    # Salva a resposta completa no histórico
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    