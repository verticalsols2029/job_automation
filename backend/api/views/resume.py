from ninja import Router


router = Router()

@router.get("/list-resumes", response=list[dict])
def list_resumes(request):
    return [{"id": 1, "title": "Software Engineer"}]