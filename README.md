# Job Question Responder

This application is designed to process documents, create vector embeddings, and expose a search functionality over an API. It uses Langchain for document processing, OpenAI for embeddings, and Pinecone for vector storage and similarity search.

## Features

- **Document Processing**: Reads PDF documents and splits them into manageable chunks.
- **Vector Embeddings**: Uses OpenAI's embeddings to convert document chunks into vector representations.
- **Vector Storage**: Stores vectors in Pinecone for efficient similarity search.
- **API Exposure**: Provides a FastAPI-based endpoint to query the vector store and retrieve relevant document chunks.

## Setup

1. **Create a Virtual Environment**:

   ```bash
   conda create -p venv python==3.10
   conda activate /Users/deadshot/Desktop/Code/job-question-responder/venv
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Create and Configure Environment File**:

   Copy the example environment file and update it with your API keys:

   ```bash
   cp .env.example .env
   ```

   Open `.env` and replace the placeholder values with your actual API keys.

4. **(Optional) Jupyter Support**:
   If you plan to work with Jupyter notebooks, install the kernel:

   ```bash
   pip install ipykernel
   ```

## Running the Application

### Option 1: Run the server

#### Step 1: Start the FastAPI Server

Run the server to expose the search functionality over an API.

```bash
python run.py
```

This command will execute both the seeding process and start the FastAPI server.

### Option 2: Run scripts individually

#### Step 1: Seed the Vector Store

This step will check if the vector store already contains documents and skip the embedding process if it does.

```bash
python seed.py
```

#### Step 2: Start the FastAPI Server

```bash
python main.py
```

## API Usage

You can query the API using a POST request to search for relevant document chunks based on your query.

### Example using `curl`

```bash
curl -X POST "http://localhost:8000/search" \
     -H "Content-Type: application/json" \
     -d '{"query": "assistant vice president"}'
```

This command will return the document chunks that are most similar to the query "assistant vice president".

## Notes

- Ensure that your `.env` file contains the necessary API keys and environment variables for OpenAI and Pinecone.
- The application is designed to skip the embedding process if the vector store already contains documents, optimizing the workflow.
