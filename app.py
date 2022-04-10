from fastapi import FastAPI, Request, Depends
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette import status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, ORJSONResponse, HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from core.settings import STATIC_URL, STATIC_ROOT, JWT, TEMPLATE, ORIGIN, docs_url, redoc_url, HOST, ENVIRONMENT
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
import base64, time
from services.user_mngmt.models import get_revoked_tokens
from services.food_advisor.model import get_user_details

from services.food_advisor import controller as advisor_control
from services.user_mngmt import controller as user_control
from services.workout import controller as workout_control
from services.terrace_farm import controller as farm_control

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded


limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])
app = FastAPI(  title="Food Advisor",
                description="Food Advisor - Innovaccer",
                version="0.0.1",
                docs_url=docs_url(), 
                redoc_url=redoc_url()
            )
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.mount(STATIC_URL, StaticFiles(directory=STATIC_ROOT), name=STATIC_ROOT)


app.add_middleware(
    CORSMiddleware, 
    allow_origins=ORIGIN,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=HOST)
app.add_middleware(GZipMiddleware, minimum_size=50000)
app.add_middleware(SlowAPIMiddleware)



@AuthJWT.load_config
def get_config():
    return JWT()


@app.middleware("http")
async def validate_request(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["x-process-time"] = str(process_time)
        return response
    except Exception as e:
        print(e)
        return ORJSONResponse(content=jsonable_encoder({'status': 503, "desc": "Service Unavailable."}), status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


@app.get("/ping/", response_class=ORJSONResponse)
async def ping(request: Request):
    return ORJSONResponse(content=jsonable_encoder({"ping": "pong"}))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, Authorize: AuthJWT = Depends()):
    Authorize.jwt_optional()
    if Authorize.get_jwt_subject():
        return RedirectResponse('/users/dashboard/', status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    else:
        return TEMPLATE.TemplateResponse('auth.html', context={"request": request})


@app.exception_handler(AuthJWTException)
async def auth_exception_handler(request: Request, exc: AuthJWTException, Authorize: AuthJWT = Depends()):
    p: str = request.url.path
    if p.find('/api/') != -1:
        return ORJSONResponse(content=jsonable_encoder({'status': 'session', 'location': '/'}), status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        return RedirectResponse('/', status_code=status.HTTP_307_TEMPORARY_REDIRECT)


@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token['jti']
    tokens = get_revoked_tokens()
    return jti in tokens


@app.exception_handler(StarletteHTTPException)
async def app_exception_handler(request: Request, exc: StarletteHTTPException):
    return ORJSONResponse(content=jsonable_encoder({'status': exc.status_code, "desc": exc.detail}), status_code=exc.status_code)


app.include_router(advisor_control.router, tags=['Advisor'])
app.include_router(user_control.router, tags=['User Management'])
app.include_router(workout_control.router, tags=['Workout'])
app.include_router(farm_control.router, tags=['Tereace Farm'])
