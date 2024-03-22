from fastapi import (
    FastAPI,
)

from users.views import router as users
from referralCode.views import router as refferal_code


app = FastAPI()
app.include_router(router=users)
app.include_router(router=refferal_code)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
