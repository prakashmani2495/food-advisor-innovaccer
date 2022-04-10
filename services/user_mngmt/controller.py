
import time, uuid
from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse, HTMLResponse, RedirectResponse
from fastapi_jwt_auth import AuthJWT
from passlib.hash import pbkdf2_sha256
from datetime import timedelta, datetime
from core.settings import TEMPLATE
from starlette import status
from .struct import *
from .models import *


router: object = APIRouter(prefix='/users', tags=['User Management'])


@router.get("/details/", response_class=HTMLResponse)
async def home(request: Request, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    chck: dict = await check_user_details(Authorize.get_jwt_subject())
    if chck:
        return RedirectResponse('/users/dashboard/', status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    else:
        return TEMPLATE.TemplateResponse('userDetails.html', context={"request": request})


@router.get("/alert-notifications/", response_class=HTMLResponse)
async def home(request: Request, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return TEMPLATE.TemplateResponse('alerts.html', context={"request": request})


@router.get("/dashboard/", response_class=HTMLResponse)
async def home(request: Request, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    chck: dict = await check_user_details(Authorize.get_jwt_subject())
    if chck:
        diet = await today_diet_plan(Authorize.get_jwt_subject())
        return TEMPLATE.TemplateResponse('dashboard.html', context={"request": request, "details": chck, "today_diet":diet})
    else:
        return RedirectResponse('/users/details/', status_code=status.HTTP_307_TEMPORARY_REDIRECT)


@router.post('/register/api/', response_class=ORJSONResponse)
async def register_user(user: NewUser, Authorize: AuthJWT = Depends()):
    Authorize.jwt_optional()
    if Authorize.get_jwt_subject():
        return ORJSONResponse(content=jsonable_encoder({"status": "success", "desc": "Authenticated."}))
    else:
        hashed: str = pbkdf2_sha256.hash(user.password)
        res = await create_new_user(user.full_name, user.email_id, hashed)
        return ORJSONResponse(content=jsonable_encoder(res))


@router.post('/login/api/', response_class=ORJSONResponse)
async def authenticate_login_user(user: User, Authorize: AuthJWT = Depends()):
    Authorize.jwt_optional()

    if Authorize.get_jwt_subject():
        return ORJSONResponse(content=jsonable_encoder({"status": "success", "desc": "Authenticated."}))
    else:
        res = await authenticate_user(user.email_id)
        if res and pbkdf2_sha256.verify(user.password, res['Password']):
            access_token = Authorize.create_access_token(subject=user.email_id, algorithm="HS384", fresh=True)
            refresh_token = Authorize.create_refresh_token(subject=user.email_id, algorithm="HS512")
            response = ORJSONResponse(content=jsonable_encoder({"status": "success", "location": "/users/dashboard/"}))
            Authorize.set_access_cookies(access_token, response, max_age= 8*60*60)
            Authorize.set_refresh_cookies(refresh_token, response, max_age= 24*60*60)
            response.set_cookie(key='X-TKN-AG', value=int(time.mktime((datetime.now() + timedelta(minutes=7*60)).timetuple())), httponly=False, max_age=9*60*60, secure=True)
            await create_user_session(uuid.uuid4().hex, res['UserAccess_ID'], Authorize.get_jti(access_token), Authorize.get_jti(refresh_token))
            return response
        return ORJSONResponse(content=jsonable_encoder({"status": "error", "desc": "Access Denied !"}))


@router.post('/raf/', response_class=ORJSONResponse)
async def refresh_access_token(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    access_jti = Authorize.get_raw_jwt()['jti']
    access_token = Authorize.create_access_token(subject=user_id, algorithm="HS384")
    refresh_token = Authorize.create_refresh_token(subject=user_id, algorithm="HS512")
    response = ORJSONResponse(content=jsonable_encoder({"status": "success", "desc": "fresh token created."}))
    Authorize.set_access_cookies(access_token, response, max_age= 8*60*60)
    Authorize.set_refresh_cookies(refresh_token, response, max_age= 24*60*60)
    response.set_cookie(key='X-TKN-AG', value=int(time.mktime((datetime.now() + timedelta(minutes=7*60)).timetuple())), httponly=False, max_age=9*60*60, secure=True)
    await update_user_session(user_id, access_jti, Authorize.get_jti(access_token), Authorize.get_jti(refresh_token))
    return response


@router.get('/api/logout/', response_class=ORJSONResponse)
async def revoke_access(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    access_jti = Authorize.get_raw_jwt()['jti']
    res = await revoke_user_session(user_id, access_jti)
    response = ORJSONResponse(content=jsonable_encoder(res))
    Authorize.unset_jwt_cookies(response)
    return response

@router.post('/details/api/', response_class=ORJSONResponse)
async def register_user(user: UserDetails, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    res: dict = await update_user_details(user_id=Authorize.get_jwt_subject(), age=user.age, gender=user.gender, height=user.height, 
                                            weight=user.weight, activity=user.activity, medical=user.medical)
    return ORJSONResponse(content=jsonable_encoder(res))