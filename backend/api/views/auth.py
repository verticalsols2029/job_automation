from ninja import Router
from django.contrib.auth.hashers import make_password
from ninja_jwt.tokens import RefreshToken
from ..models import User, Profile
from ..schemas.auth_schema import RegisterIn, TokenOut, ErrorOut

router = Router()

@router.post("/register", response={201: TokenOut, 400: ErrorOut})
def register(request, data: RegisterIn):
    if User.objects.filter(email=data.email).exists():
        return 400, {"message": "User already exists"}

    user = User.objects.create(
        email=data.email,
        password=make_password(data.password),
        first_name=data.first_name,
        last_name=data.last_name,
        username=data.email
    )
    Profile.objects.create(user=user, first_name=data.first_name, last_name=data.last_name)
    
    refresh = RefreshToken.for_user(user)
    return 201, {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }