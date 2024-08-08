from fastapi import FastAPI, HTTPException
from google.cloud import storage
from typing import List

app = FastAPI()

# Replace with your Google Cloud project and bucket name
PROJECT_ID = "your-google-cloud-project-id"
BUCKET_NAME = "your-bucket-name"

# Initialize Google Cloud Storage client
storage_client = storage.Client(project=PROJECT_ID)

@app.get("/files/")
async def get_files(filetype: str) -> List[str]:
    try:
        bucket = storage_client.get_bucket(BUCKET_NAME)
        blobs = bucket.list_blobs()

        # Filter files by the metadata field "filetype"
        filtered_files = [
            blob.name for blob in blobs 
            if blob.metadata and blob.metadata.get("filetype") == filetype
        ]

        if not filtered_files:
            raise HTTPException(status_code=404, detail="No files found with the specified filetype")

        return filtered_files

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
