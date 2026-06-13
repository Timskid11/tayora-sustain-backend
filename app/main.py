from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, donations, requests, admin
from app.database import Base, engine
from app.models import user, donation, request

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Tayora Sustain API",
    description="Backend API for the Tayora Sustain textile waste exchange platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-production-domain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(donations.router, prefix="/api/v1/donations", tags=["Donations"])
app.include_router(requests.router, prefix="/api/v1/requests", tags=["Requests"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])

@app.get("/")
def root():
    return {"message": "Tayora Sustain API is running"}