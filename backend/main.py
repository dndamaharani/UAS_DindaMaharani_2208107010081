from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Set up the Gemini API
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print(os.getenv("GEMINI_API_KEY"))
    raise ValueError("API key for Gemini is not set in environment variables")

genai.configure(api_key=api_key)

# Initialize FastAPI app
app = FastAPI(title="Intelligent Email Writer API")

# Configure CORS to allow requests from Streamlit app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development. Limit this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailRequest(BaseModel):
    category: str
    tone: str
    language: str
    recipient: str
    subject: str
    key_points: List[str]
    sender_name: Optional[str] = None
    sender_position: Optional[str] = None

class EmailResponse(BaseModel):
    email_content: str

# Mapping for tone translations
tone_translations = {
    "formal": {
        "en": "formal",
        "id": "formal"
    },
    "neutral": {
        "en": "neutral",
        "id": "netral"
    },
    "casual": {
        "en": "casual",
        "id": "santai"
    }
}

# Mapping for category translations
category_translations = {
    "academic": {
        "en": "academic",
        "id": "akademik"
    },
    "thesis": {
        "en": "thesis",
        "id": "skripsi"
    },
    "internship": {
        "en": "internship",
        "id": "magang"
    },
    "general": {
        "en": "general",
        "id": "umum"
    }
}


@app.get("/")
async def root():
    return {"message": "Intelligent Email Writer API is running"}


@app.post("/generate-email", response_model=EmailResponse)
async def generate_email(request: EmailRequest):
    try:
        # Determine language-specific tone and category
        lang_code = "en" if request.language.lower() == "english" else "id"
        tone = tone_translations.get(request.tone.lower(), {}).get(lang_code, request.tone)
        category = category_translations.get(request.category.lower(), {}).get(lang_code, request.category)
        
        # Construct key points text
        key_points_text = "\n".join([f"- {point}" for point in request.key_points])
        
        # Create prompt based on language
        if lang_code == "en":
            prompt = f"""
            Generate a professional {tone} email for {category} purposes.

            Email Details:
            - Recipient: {request.recipient}
            - Subject: {request.subject}
            - Tone: {tone}
            
            Key points to include:
            {key_points_text}
            
            {f"Sender: {request.sender_name}" if request.sender_name else ""}
            {f"Position: {request.sender_position}" if request.sender_position else ""}
            
            Write a complete, well-structured email with appropriate greeting, body paragraphs that address all key points, and professional closing. 
            Format the email ready to send (include Subject line, To, From if provided).
            """
        else:  # Indonesian
            prompt = f"""
            Buatkan email profesional dengan nada {tone} untuk keperluan {category}.
            
            Detail Email:
            - Penerima: {request.recipient}
            - Subjek: {request.subject}
            - Nada: {tone}
            
            Poin-poin penting yang perlu disampaikan:
            {key_points_text}
            
            {f"Pengirim: {request.sender_name}" if request.sender_name else ""}
            {f"Jabatan: {request.sender_position}" if request.sender_position else ""}
            
            Tuliskan email lengkap dengan struktur yang baik termasuk salam pembuka, paragraf isi yang mencakup semua poin penting, dan penutup yang profesional.
            Format email siap kirim (sertakan baris Subjek, Kepada, Dari jika disediakan).
            """

        # Call Gemini API
        model = genai.GenerativeModel('gemini-1.5-flash')  # Replace with a different model
        response = model.generate_content(prompt)
        
        # Return the generated email
        return EmailResponse(email_content=response.text)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating email: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)