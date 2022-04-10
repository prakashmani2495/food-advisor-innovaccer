from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi_jwt_auth import AuthJWT
from core.settings import TEMPLATE


router: object = APIRouter(prefix='/advisor', tags=['Advisor'])


@router.get("/slot-booking/", response_class=HTMLResponse)
async def home(request: Request, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return TEMPLATE.TemplateResponse('advisorSlot.html', context={"request": request})
