from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from .models import Wallet
from .schemas import WalletOperationRequest
from typing import Optional
from uuid import UUID


class WalletService:
    @staticmethod
    async def get(db: AsyncSession, wallet_uuid: UUID) -> Optional[Wallet]:
        """
        Get wallet balance by UUID from database.

        Parameters:
            db (AsyncSession): The database session.
            wallet_uuid (UUID): Wallet UUID.

        Returns:
            Optional[Wallet]: The wallet found by UUID,
            or None if not found.
        """
        statement = select(Wallet).where(Wallet.id == wallet_uuid).with_for_update()
        result = await db.execute(statement)
        wallet = result.scalars().one_or_none()
        return wallet

    @staticmethod
    async def create(
        db: AsyncSession, wallet_uuid: UUID, amount: int
    ) -> Optional[Wallet]:
        """
        Create a new wallet with given UUID and amount in the database.

        Parameters:
            db (AsyncSession): The database session.
            wallet_uuid (UUID): Wallet UUID.
            amount (int): amount to be added to the wallet upon creation.

        Returns:
            Optional[Wallet]: Wallet with given UUID,
            or None if creation failed.
        """
        statement = insert(Wallet).values((wallet_uuid, amount)).returning(Wallet)
        result = await db.execute(statement)
        wallet = result.scalars().one()
        await db.commit()
        await db.refresh(wallet)
        return wallet

    @staticmethod
    async def update(
        db: AsyncSession, wallet: Wallet, operation_data: WalletOperationRequest
    ) -> Wallet:
        """
        Update wallet's balance depending on operation:
        adds to wallet's balance with DEPOSIT operations,
        substracts from balance with WITHDRAW operations.

        Parameters:
            db (AsyncSession): The database session.
            wallet (Wallet): Wallet object to update.
            operation_data (WalletOperationRequest): Data from
            incoming request containing operation type and amount

        Returns:
            Wallet: Updated Wallet object.
        """
        wallet.balance += int(
            operation_data.operation_type + str(operation_data.amount)
        )
        await db.commit()
        await db.refresh(wallet)
        return wallet
