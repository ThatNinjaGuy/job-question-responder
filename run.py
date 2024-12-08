import subprocess
import os


def run_seed():
    print("\n" + "=" * 30)
    print("Running seed script...")
    print("=" * 30 + "\n")
    subprocess.run(["python", "seed.py"], check=True)
    print("\n" + "=" * 30)
    print("Seed script completed.")
    print("=" * 30 + "\n")


def run_server():
    print("\n" + "=" * 30)
    print("Starting FastAPI server...")
    print("=" * 30 + "\n")
    subprocess.run(
        ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"], check=True
    )


if __name__ == "__main__":
    run_seed()
    run_server()
