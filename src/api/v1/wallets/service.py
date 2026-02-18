from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from src.database import get_session
from .models import Wallet


class WalletService:
    def __init__(self):
        ...

    # def __init__(self, session: AsyncSession = Depends(get_session)):
    #     self.session = session

    # async def get(self, wallet_uuid):
    #     statement = select(Wallet).where(Wallet.id == wallet_uuid).with_for_update()
    #     result = await self.session.execute(statement)
    #     wallet = result.scalars().one_or_none()
    #     return wallet

    async def get(self, db: AsyncSession, wallet_uuid):
        statement = select(Wallet).where(Wallet.id == wallet_uuid).with_for_update()
        result = await db.execute(statement)
        wallet = result.scalars().one_or_none()
        return wallet

    # async def create(self, wallet_uuid, amount):
    #     statement = insert(Wallet).values((wallet_uuid, amount)).returning(Wallet)
    #     result = await self.session.execute(statement)
    #     wallet = result.scalars().one()
    #     await self.session.commit()
    #     await self.session.refresh(wallet)
    #     return wallet

    async def create(self, db: AsyncSession, wallet_uuid, amount):
        statement = insert(Wallet).values((wallet_uuid, amount)).returning(Wallet)
        result = await db.execute(statement)
        wallet = result.scalars().one()
        await db.commit()
        await db.refresh(wallet)
        return wallet

    async def update(self, db: AsyncSession, wallet, operation_data):
        wallet.balance += int(operation_data.operation_type + str(operation_data.amount))
        await db.commit()
        await db.refresh(wallet)
        return wallet


    # async def update(self, wallet, operation_data):
    #     wallet.balance += int(operation_data.operation_type + str(operation_data.amount))
    #     await self.session.commit()
    #     await self.session.refresh(wallet)
    #     return wallet
