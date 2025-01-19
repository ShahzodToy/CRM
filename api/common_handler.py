from typing import Optional, List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form

from sqlalchemy.ext.asyncio import AsyncSession

from api.action import common_action
from api.login_handler import get_current_user_from_token
from datetime import datetime

from database import schemas, session, models


common_router = APIRouter()

@common_router.get('/list-income-expected-val', response_model=List[schemas.ShowExpectedValue])
async def get_all_income_val(db:AsyncSession = Depends(session.get_db)):
    return await common_action._get_all_income_expected_value(session=db)

@common_router.get('/list-expense-expected-val', response_model=List[schemas.ShowExpectedValue])
async def get_all_income_val(db:AsyncSession = Depends(session.get_db)):
    return await common_action._get_all_expense_expected_value(session=db)

@common_router.post('/create-expected-value', response_model=schemas.ShowExpectedValue)
async def get_all_income_val(body:schemas.CreateExpectedValue, db:AsyncSession = Depends(session.get_db)):
    return await common_action._create_expected_value(session=db, body=body)

@common_router.delete('/delete-expected-val')
async def delete_expected_value(expected_val_id:int, db:AsyncSession = Depends(session.get_db)):
    return await common_action._delete_expected_value(expected_val_id=expected_val_id, session=db)

@common_router.patch('/update-expected-val')
async def update_expected_value(expected_avl_id:int ,updated_val_params:schemas.UpdateExpectedValue, db:AsyncSession = Depends(session.get_db)):
    body = updated_val_params.model_dump(exclude_none=True)
    return await common_action._update_expected_value(session=db, body=body, expected_avl_id=expected_avl_id)
