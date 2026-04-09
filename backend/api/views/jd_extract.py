import re
import base64
from ninja import Router, Form
from ollama import AsyncClient
from api.config import settings

router = Router()

@router.post("/jd-format-ollama")
async def format_job_description_ollama(request, raw_text: str = Form(...)):
    client = AsyncClient(host=settings.ollama_host)
    messages = [
        {
            "role": "system",
            "content": "You are only a data extractor. Extract only: Title | Company. Do not say anything else. Example: Software Engineer | Google"
        },
        {
            "role": "user",
            "content": f"Extract only Title and Company from this text:\n{raw_text}"
        }
    ]

    response_ai = await client.chat(
        model='llama3', 
        messages=messages,
        options={'temperature': 0}
    )
    
    ai_text = response_ai['message']['content'].strip()
    
    try:
        title, company = ai_text.split("|", 1)
        extracted_title = title.strip()
        extracted_company = company.strip()
    except ValueError:
        extracted_title = "Extracted_Job"
        extracted_company = "Description"

    file_text = f"Title: {extracted_title}\nCompany: {extracted_company}\n\nJob Description:\n\n{raw_text}"

    b64_content = base64.b64encode(file_text.encode('utf-8')).decode('utf-8')

    clean_title = re.sub(r'[^\w\s-]', '', extracted_title).strip().replace(' ', '_')
    clean_company = re.sub(r'[^\w\s-]', '', extracted_company).strip().replace(' ', '_')
    filename = f"{clean_title}_{clean_company}.txt"

    return {
        "status": "success",
        "title": extracted_title,
        "company": extracted_company,
        "filename": filename,
        "file_content_b64": b64_content
    }