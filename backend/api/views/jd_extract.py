from ninja import Router, Form
from google import genai
from google.genai import types


router = Router()

@router.post("/jd-extract-gemini")
async def format_job_description_gemini(request, raw_text: str = Form(...)):
    
    client = genai.Client(api_key="AIzaSyDYU5WWmvU5Bht3kOq_7EROhHWUdX87Gmo")
    
    async with client.aio as async_client:
        response = await async_client.models.generate_content(
            model='gemini-3.1-flash',
            contents=[
                "Extract only Title and Company Name. Use Exact Format: Title | Company",
                raw_text
            ],
            config=types.GenerateContentConfig(temperature=0)
        )
    
    try:
        title, company = response.text.split("|", 1)
        extracted_title = title.strip()
        extracted_company = company.strip()
    except Exception:
        extracted_title = "Not Found"
        extracted_company = "Not Found"

    return {
        "status": "success",
        "title": extracted_title,
        "company": extracted_company,
        "full_response": response.text
    }