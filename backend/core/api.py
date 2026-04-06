from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from api.views.auth import router as auth_router
from api.views.resume import router as resume_router
from api.views.jd_extract import router as jd_extract_router

api = NinjaExtraAPI(title="Simplify Clone API")
api.register_controllers(NinjaJWTDefaultController)

api.add_router("/auth", auth_router)
api.add_router("/resume", resume_router)
api.add_router("/jd", jd_extract_router)

@api.get("/health")
def health_check(request):
    return {"status": "ok"}