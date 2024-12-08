from fastapi import FastAPI
from pydantic import BaseModel
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings

import os

load_dotenv()

app = FastAPI()


# Define a Pydantic model for the query input
class QueryInput(BaseModel):
    query: str


# Initialize the vector store
index_name = "job-question-responder"
embeddings = OpenAIEmbeddings(api_key=os.environ["OPENAI_API_KEY"])
vector_store = PineconeVectorStore(index_name=index_name, embedding=embeddings)


def retrieve_query(query, k=2):
    results = vector_store.similarity_search(query, k=k)
    return results


def retrieve_answers(query):
    doc_search = retrieve_query(query)
    return doc_search


@app.post("/search")
def search_documents(query_input: QueryInput):
    query = query_input.query
    answer = retrieve_answers(query)
    return {"query": query, "results": answer}


# Uncomment the following lines if you want to run the server directly from this script
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
