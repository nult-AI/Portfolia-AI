import os
from typing import List, Optional
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from app.schemas.schemas import CVExtractionResponse, ProfileCreate, ExperienceCreate, EducationCreate
import pypdf
import io
import base64
from dotenv import load_dotenv
load_dotenv()

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Cần cấu hình GOOGLE_API_KEY trong file .env")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", # Đổi lại model chính xác (thường là 1.5-flash hoặc 2.0-flash-exp)
            google_api_key=self.api_key,
            temperature=0
        )

    def extract_text_from_pdf(self, pdf_stream: io.BytesIO) -> str:
        pdf_reader = pypdf.PdfReader(pdf_stream)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text

    async def parse_cv(self, pdf_content: bytes) -> CVExtractionResponse:
        text = self.extract_text_from_pdf(io.BytesIO(pdf_content))
        
        parser = PydanticOutputParser(pydantic_object=CVExtractionResponse)
        
        prompt = ChatPromptTemplate.from_template(
            "Extract professional information from the following CV text.\n"
            "{format_instructions}\n"
            "CV Text:\n{cv_text}"
        )
        
        chain = prompt | self.llm | parser
        
        result = await chain.ainvoke({
            "cv_text": text,
            "format_instructions": parser.get_format_instructions()
        })
        
        return result

llm_service = LLMService()
