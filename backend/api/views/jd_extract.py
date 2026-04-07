from ninja import Router, Form
from ollama import AsyncClient


router = Router()


@router.post("/jd-format-ollama")
async def format_job_description_ollama(request, raw_text: str = Form(...)):
    
    client = AsyncClient(host="http://192.168.1.184:11434")
    messages = [
        {
            "role": "system",
            "content": "You are a data extractor. Extract only: Title | Company. Do not say anything else. Example: Software Engineer | Google"
        },
        {
            "role": "user",
            "content": f"Extract from this text:\n{raw_text}"
        }
    ]

    response = await client.chat(
        model='llama3', 
        messages=messages,
        options={'temperature': 0}
    )
    
    ai_text = response['message']['content']
    try:
        title, company = ai_text.split("|", 1)
        extracted_title = title.strip()
        extracted_company = company.strip()
    except ValueError:
        extracted_title = "Check original text"
        extracted_company = "Check original text"

    return {
        "status": "success",
        "title": extracted_title,
        "company": extracted_company,
        "full_response": ai_text
    }

