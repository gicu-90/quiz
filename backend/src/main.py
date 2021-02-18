from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from API import gamesApi, usersApi

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(gamesApi.router)
app.include_router(usersApi.router)
