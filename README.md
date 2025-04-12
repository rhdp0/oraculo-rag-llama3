# Oráculo - NeoTech Solutions

**Oráculo** é um assistente virtual baseado em *Retrieval Augmented Generation* (RAG) que integra uma base de conhecimento local em formato CSV com um modelo de linguagem LLaMA 3 para responder perguntas com base nesse conteúdo. A aplicação foi desenvolvida utilizando **Streamlit** para a interface de usuário e **Langchain** para a construção da cadeia RAG.

## Como Funciona

1. **Carregamento de Dados**: A base de conhecimento é carregada de um arquivo CSV e é processada para gerar embeddings usando o modelo `sentence-transformers/all-MiniLM-L6-v2`.
2. **Vetorização e Recuperação de Dados**: Os dados são vetorizados usando o FAISS, o que permite a recuperação eficiente de informações relevantes com base em perguntas do usuário.
3. **Modelo de Linguagem**: O modelo LLaMA 3, executado via **Ollama**, é utilizado para gerar respostas com base nas informações recuperadas da base de conhecimento.
4. **Cadeia RAG**: Combina a recuperação dos dados com o modelo de linguagem para gerar respostas precisas para o usuário.

## Pré-Requisitos

Antes de executar o projeto, instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

## Dependências
streamlit: Para a construção da interface web.

langchain_community: Para carregar dados, embeddings, e interagir com o modelo de linguagem.

FAISS: Para vetorização e recuperação eficiente de documentos.

HuggingFaceEmbeddings: Para geração de embeddings de documentos.

ChatOllama: Para interação com o modelo LLaMA 3 via Ollama.

## Como Usar
Certifique-se de ter o arquivo knowledge_base.csv com os dados que serão usados como base de conhecimento. O arquivo CSV deve estar no mesmo diretório que o script.

Execute o script:

```bash
streamlit run oracle.py
```
Na interface web, digite suas perguntas e o modelo responderá com base na base de conhecimento carregada.

## Funcionalidades
Consulta de Base de Conhecimento: O assistente consulta um arquivo CSV local para encontrar a resposta mais relevante para as perguntas do usuário.

Modelo de Respostas: A aplicação usa um modelo LLaMA 3 para gerar respostas precisas baseadas no contexto fornecido.

Armazenamento de Mensagens: O histórico de conversas é salvo para mostrar interações anteriores no chat.
