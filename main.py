from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from utils.document_analyzer import analyze_doc

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze-document")
async def analyze_document_endpoint(
    file: UploadFile = File(...), 
    color_threshold: float = 10.0,
    photo_threshold: float = 30.0,
):
    contents = await file.read()
    result = analyze_doc(contents, color_threshold, photo_threshold)
    return result
