from fastapi import APIRouter,HTTPException,Depends

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/createuser")
async def create_user():
    return {"message":"create user"}