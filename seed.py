from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

load_dotenv()


def read_doc(directory):
    file_loader = PyPDFDirectoryLoader(directory)
    documents = file_loader.load()
    return documents


def chunk_data(docs, chunk_size=800, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_documents(docs)
    return chunks


def populate_vector_store():
    index_name = "job-question-responder"
    vector_store = PineconeVectorStore(index_name=index_name, embedding=embeddings)

    # Check if the index already exists
    if vector_store.index_exists():
        print("Vector index already exists. Skipping embedding creation.")
        return

    # Read and process documents
    doc = read_doc("documents/")
    document = chunk_data(docs=doc)

    # Add documents to the vector store
    vector_store.add_documents(document)
    print("Documents have been embedded and added to the vector store.")


if __name__ == "__main__":
    embeddings = OpenAIEmbeddings(api_key=os.environ["OPENAI_API_KEY"])
    populate_vector_store()
