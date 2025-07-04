from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from utils.pdf_analyzer import analyze_pdf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ganti ke origin Laravel kamu
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze-pdf")
async def analyze_pdf_endpoint(file: UploadFile = File(...)):
    contents = await file.read()
    result = analyze_pdf(contents)
    return result
