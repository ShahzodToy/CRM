import uvicorn
import logging

from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles

from api.employee_handler import emp_router
from api.login_handler import login_user
from api.common_handler import common_router

app = FastAPI()
main_api_router = APIRouter()
app.mount("/media", StaticFiles(directory="./media"), name="media")


main_api_router.include_router(emp_router, prefix='/employee',tags=['employee'])
main_api_router.include_router(login_user, prefix='/login', tags=['login'])
main_api_router.include_router(common_router, prefix='/common', tags=['common'])

app.include_router(main_api_router)

@app.get('/ping')
async def checking_status():
    return {'status':True}


if __name__ == '__main__':
    
    uvicorn.run(app, host='localhost',port=8000)
    