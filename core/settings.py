from fastapi.templating import Jinja2Templates
import os
from pydantic import BaseModel


TEMPLATE: object = Jinja2Templates(directory=os.path.join("templates"))


STATIC_URL: str = "/assets"
STATIC_ROOT: object = os.path.join("assets")


SECRET_KEY: str = "3iaA8LArhEPM96FYpd9XxPYfM9Ji2r0GV1dPy6uj5tNmWe3E"
CLAIM_SECRET: str = "zyLv79aQyb23z6gNFUw67YX8WvDgVGrd8PMDnHU7fMy0NuTj"


# DB_USER: str = os.environ['FOOD_DB_USER']
# DB_PSWD: str = os.environ['FOOD_DB_PSWD']
# DB_HOST: str = os.environ['FOOD_DB_HOST']
# DB_PORT: str = os.environ['FOOD_DB_PORT']
DB_USER: str = 'root'
DB_PSWD: str = 'Ms240995'
DB_HOST: str = 'localhost'
DB_PORT: str = '3306'
DATABASE: str = 'food_advisor'
DATABASE_URL: str = 'mysql+pymysql://{}:{}@{}:{}/'.format(
    DB_USER, DB_PSWD, DB_HOST, DB_PORT)


AWS_ACCESS_KEY: str = os.environ['APP_AWS_KEY']
AWS_SECRET_KEY: str = os.environ['APP_AWS_SECRET']


ORIGIN: list = [
    "*"
]

HOST: list = [
    "*"
]


ENVIRONMENT: str = os.environ['APP_ENV']


def docs_url():
    if ENVIRONMENT == 'Development': return '/docs'
    else: return None

def redoc_url():
    if ENVIRONMENT == 'Development': return '/redoc'
    else: return None

def secure():
    if ENVIRONMENT == 'Development': return False
    else: return True


class JWT(BaseModel):
    authjwt_secret_key: str = SECRET_KEY
    authjwt_decode_algorithms: set = {"HS384", "HS512"}
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = True
    authjwt_access_cookie_key: str = "X-TOKEN-ID"
    authjwt_refresh_cookie_key: str = "X-TOKEN-IDL"
    authjwt_access_csrf_cookie_key: str = "X-CSRF-ID"
    authjwt_access_csrf_header_name: str = "X-CSRF-ID"
    authjwt_refresh_csrf_cookie_key: str = "X-CSRF_IDL"
    authjwt_refresh_csrf_header_name: str = "X-CSRF_IDL"
    authjwt_header_name: str = "X-TOKEN-ID"
    authjwt_cookie_secure: bool = secure()
    authjwt_cookie_samesite: str = "lax"
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access","refresh"}
    authjwt_access_token_expires: int = 8*60*60
    authjwt_refresh_token_expires: int = 2*24*60*60
