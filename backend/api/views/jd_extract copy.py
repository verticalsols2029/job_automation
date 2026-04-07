# from ninja import Router, Form
# from ollama import AsyncClient

# from google import genai
# from google.genai import types


# router = Router()


# @router.post("/jd-format-ollama")
# async def format_job_description_ollama(request, raw_text: str = Form(...)):
    
#     client = AsyncClient()
#     messages = [
#         {
#             "role": "system",
#             "content": "You are a data extractor. Extract only: Title | Company. Do not say anything else. Example: Software Engineer | Google"
#         },
#         {
#             "role": "user",
#             "content": f"Extract from this text:\n{raw_text}"
#         }
#     ]

#     response = await client.chat(
#         model='llama3.2:1b', 
#         messages=messages,
#         options={'temperature': 0}
#     )
    
#     ai_text = response['message']['content']
#     try:
#         title, company = ai_text.split("|", 1)
#         extracted_title = title.strip()
#         extracted_company = company.strip()
#     except ValueError:
#         extracted_title = "Check original text"
#         extracted_company = "Check original text"

#     return {
#         "status": "success",
#         "title": extracted_title,
#         "company": extracted_company,
#         "full_response": ai_text
#     }



# from ninja import Router, Form
# from google import genai
# from google.genai import types


# router = Router()

# @router.post("/jd-extract-gemini")
# async def format_job_description_gemini(request, raw_text: str = Form(...)):
    
#     client = genai.Client(api_key="AIzaSyDYU5WWmvU5Bht3kOq_7EROhHWUdX87Gmo")
    
#     async with client.aio as async_client:
#         response = await async_client.models.generate_content(
#             model='gemini-3.1-flash',
#             contents=[
#                 "Extract only Title and Company Name. Use Exact Format: Title | Company",
#                 raw_text
#             ],
#             config=types.GenerateContentConfig(temperature=0)
#         )
    
#     try:
#         title, company = response.text.split("|", 1)
#         extracted_title = title.strip()
#         extracted_company = company.strip()
#     except Exception:
#         extracted_title = "Not Found"
#         extracted_company = "Not Found"

#     return {
#         "status": "success",
#         "title": extracted_title,
#         "company": extracted_company,
#         "full_response": response.text
#     }