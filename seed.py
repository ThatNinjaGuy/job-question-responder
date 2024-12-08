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

    # Perform a dummy search to check if any documents exist
    try:
        results = vector_store.similarity_search(query="dummy", k=1)
        if len(results) > 0:
            print(
                "Vector index already contains documents. Skipping embedding creation."
            )
            return
        print("Vector index is empty. Proceeding with embedding creation.")
    except Exception as e:
        print("Error during dummy search:", str(e))
        print("Proceeding with embedding creation.")

    # Read and process documents
    doc = read_doc("documents/")
    document = chunk_data(docs=doc)

    # Add documents to the vector store
    vector_store.add_documents(document)
    print("Documents have been embedded and added to the vector store.")


if __name__ == "__main__":
    embeddings = OpenAIEmbeddings(api_key=os.environ["OPENAI_API_KEY"])
    populate_vector_store()
