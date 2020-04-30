SERVER_PORT = 8999
DEBUG = True
SQLALCHEMY_ECHO = True
SQLALCHEMY_DATABASE_URI = 'mysql://admin:12345678@database-1.cglyd7m1y99e.us-east-2.rds.amazonaws.com/project'
SQLALCHEMY_ENCODING = "utf-8"
AUTH_COOKIE_NAME = 'interview'


## filter url
IGNORE_URLS = [
    "^/user/login",
    "^/user/register"
]

IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/.favicon.ico"
]

PAGE_SIZE=50
PAGE_DISPLAY=10