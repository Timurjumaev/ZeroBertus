from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import api


description = """
------------------------------
**Username and password for ZeroBertusAdmin**
* Login: **zerobertusadmin**
* Parol: **zerobertus**
------------------------------
"""

app = FastAPI(
    description=description,
    contact={
        'name': "Temur Jumayev's telegram account url for questions",
        'url': 'https://t.me/Temur_Jumayev',
    },
    docs_url='/',
    redoc_url='/redoc',
)

app.include_router(api)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['https://bertuspanelsuz.netlify.app', 'https://iteachpython.uz'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





