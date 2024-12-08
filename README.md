conda create -p venv python==3.10
conda activate /Users/deadshot/Desktop/Code/job-question-responder/venv
pip install -r requirements.txt
<!-- For working in jupyter -->
pip install ipykernel
uvicorn main:app --host 0.0.0.0 --port 8000
