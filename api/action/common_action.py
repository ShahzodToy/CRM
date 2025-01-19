from fastapi import UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import schemas
from datetime import datetime
from dals import common_dal


async def _get_all_income_expected_value(session: AsyncSession):
    async with session.begin():
        com_dal = common_dal.CommonDal(session)

        all_income = await com_dal.get_income_expected_val()

        return [
            schemas.ShowExpectedValue(
                id=income_val.id,
                name=income_val.name,
                date=income_val.date,
                description=income_val.description,
                type=income_val.type
            )
            for income_val in all_income
        ]
    

async def _get_all_expense_expected_value(session: AsyncSession):
    async with session.begin():
        com_dal = common_dal.CommonDal(session)

        all_income = await com_dal.get_expence_expected_val()

        return [
            schemas.ShowExpectedValue(
                id=income_val.id,
                name=income_val.name,
                date=income_val.date,
                description=income_val.description,
                type=income_val.type
            )
            for income_val in all_income
        ]
    
async def _create_expected_value(session:AsyncSession, body:schemas.CreateExpectedValue):
    async with session.begin():
        com_dal = common_dal.CommonDal(session)

        create_val = await com_dal.create_expected_val(body=body)

        return schemas.ShowExpectedValue(
            id=create_val.id,
            name=create_val.name,
            date=create_val.date,
            description=create_val.description,
            type=create_val.type
        )
    

async def _delete_expected_value(session:AsyncSession, expected_val_id:int):
    async with session.begin():
        com_dal = common_dal.CommonDal(session)

        delete_val = await com_dal.delete_expected_val(expected_val_id=expected_val_id)

        if delete_val:
            return {'succes':True,
                    'message':"Deleted successfully"}
        
async def _update_expected_value(session:AsyncSession,expected_avl_id:int, body:dict):
    async with session.begin():
        com_dal = common_dal.CommonDal(session)

        update_val = await com_dal.update_expected_val(expected_avl_id=expected_avl_id, **body)

        if update_val:
            return {'succes':True,
                    'message':"Updated successfully"}
        return {'succes':False,
                    'message':"Error occured"}

