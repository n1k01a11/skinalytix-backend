from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from . import models
from .database import engine
from .routers import users, consultations, products, analysis, skin_profiles

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SKINALYTIX API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # fine for a capstone; a public production app would restrict this
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(users.router)
app.include_router(consultations.router)
app.include_router(products.router)
app.include_router(analysis.router)
app.include_router(skin_profiles.router)

@app.get("/")
def root():
    return {"message": "SKINALYTIX API is running"}