# %%
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from fastapi import FastAPI
from pydantic import BaseModel

# %%
from dotenv import load_dotenv

load_dotenv()

# %%
import os


# %%
##Lets read the document
def read_doc(directory):
    file_loader = PyPDFDirectoryLoader(directory)
    documents = file_loader.load()
    return documents


# %%
doc = read_doc("documents/")
doc

# %%
# Divide the docs into chunks


def chunk_data(docs, chunk_size=800, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_documents(docs)
    return chunks


# %%
document = chunk_data(docs=doc)
document
# len(document)


# %%
# Embedding technique with OpenAI
embeddings = OpenAIEmbeddings(api_key=os.environ["OPENAI_API_KEY"])
embeddings

# %%
vectors = embeddings.embed_query("How are you?")
vectors
# len(vectors)
# 1536

# %%
# Vector search db in pinecone
index_name = "job-question-responder"
vector_store = PineconeVectorStore(index_name=index_name, embedding=embeddings)
index = vector_store.add_documents(document)
index


# %%
# Retrieve Cosine similarity results
def retrieve_query(query, k=2):
    results = vector_store.similarity_search(query, k=k)
    return results


# %%
# Search answers from vector database
def retrieve_answers(query):
    doc_search = retrieve_query(query)
    return doc_search


# %%
app = FastAPI()


# Define a Pydantic model for the query input
class QueryInput(BaseModel):
    query: str


@app.post("/search")
def search_documents(query_input: QueryInput):
    query = query_input.query
    answer = retrieve_answers(query)
    return {"query": query, "results": answer}


# Uncomment the following lines if you want to run the server directly from this script
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
