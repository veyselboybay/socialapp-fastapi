from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import user,auth

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Add router middlewares
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def health_check():
    return {"message":"healthy"}