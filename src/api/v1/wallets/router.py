from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import WalletResponse, WalletOperationRequest
from .service import WalletService
from uuid import UUID
from src.database import get_session


router = APIRouter(
    prefix="/api/v1/wallets",
    tags=["wallets"]
)

@router.get("/{wallet_uuid}", response_model=WalletResponse)
async def get_wallet_balance(
        wallet_uuid: UUID,
        wallet_service: WalletService = Depends(),
        db: AsyncSession = Depends(get_session),
):
    wallet = await wallet_service.get(db, wallet_uuid)
    if not wallet:
        raise HTTPException(status_code=404, detail=f"Wallet with ID {wallet_uuid} not found")
    return wallet

# @router.get("/{wallet_uuid}", response_model=WalletResponse)
# async def get_wallet_balance(wallet_uuid: UUID, wallet_service: WalletService = Depends()):
#     wallet = await wallet_service.get(wallet_uuid)
#     if not wallet:
#         raise HTTPException(status_code=404, detail=f"Wallet with ID {wallet_uuid} not found")
#     return wallet

# @router.post("/{wallet_uuid}/operation", response_model=WalletResponse)
# async def wallet_operation(
#     wallet_uuid: UUID,
#     operation_data: WalletOperationRequest,
#     wallet_service: WalletService = Depends(),
# ):
#     wallet = await wallet_service.get(wallet_uuid)
#     if operation_data.operation_type == "+":    # DEPOSIT operation
#         if not wallet:
#             wallet = await wallet_service.create(wallet_uuid, operation_data.amount)
#             return wallet
#     if operation_data.operation_type == "-":    # WITHDRAW operation
#         if not wallet:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Wallet with ID {wallet_uuid} not found")
#         if wallet.balance < operation_data.amount:
#             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient wallet balance")
#     wallet = await wallet_service.update(wallet, operation_data)
#     return wallet

@router.post("/{wallet_uuid}/operation", response_model=WalletResponse)
async def wallet_operation(
    wallet_uuid: UUID,
    operation_data: WalletOperationRequest,
    wallet_service: WalletService = Depends(),
    db: AsyncSession = Depends(get_session)
):
    wallet = await wallet_service.get(db, wallet_uuid)
    if operation_data.operation_type == "+":    # DEPOSIT operation
        if not wallet:
            wallet = await wallet_service.create(db, wallet_uuid, operation_data.amount)
            return wallet
    if operation_data.operation_type == "-":    # WITHDRAW operation
        if not wallet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Wallet with ID {wallet_uuid} not found")
        if wallet.balance < operation_data.amount:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient wallet balance")
    wallet = await wallet_service.update(db, wallet, operation_data)
    return wallet
