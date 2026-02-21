from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from .schemas import WalletResponse, WalletOperationRequest
from .service import WalletService
from uuid import UUID


router = APIRouter(prefix="/api/v1/wallets", tags=["wallets"])


@router.get("/{wallet_uuid}", response_model=WalletResponse)
async def get_wallet_balance(
    wallet_uuid: UUID,
    wallet_service: WalletService = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """
    Fetches a wallet by their UUID from the database.

    Parameters:
        wallet_uuid(UUID): UUID of the wallet to fetch.
        wallet_service(WalletService): WalletService dependency to handle logic.
        db (AsyncSession): Database session.

    Returns:
        WalletResponse: The wallet object fetched from the database.

    Raises:
        HTTPException: If the wallet with the given UUID is not found in the database.
    """
    wallet = await wallet_service.get(db, wallet_uuid)
    if not wallet:
        raise HTTPException(
            status_code=404, detail=f"Wallet with ID {wallet_uuid} not found"
        )
    return wallet


@router.post("/{wallet_uuid}/operation", response_model=WalletResponse)
async def wallet_operation(
    wallet_uuid: UUID,
    operation_data: WalletOperationRequest,
    response: Response,
    wallet_service: WalletService = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """
    Creates or modifies wallet with given UUID in the database.

    Parameters:
        wallet_uuid(UUID): UUID of the wallet to fetch.
        operation_data(WalletOperationRequest): JSON-data containing the amount
                                                and operation to perform.
        response(Response): Response object to return more descriptive responses
                            to the client (i.e. 201, not 200 on successful creation)
        wallet_service(WalletService): WalletService dependency to handle logic.
        db (AsyncSession): Database session.

    Returns:
        WalletResponse: Created or updated wallet object from the database.

    Raises:
        HTTPException: If the wallet with given UUID is not found in the database.
        HTTPException: If the wallet's balance is insufficient for given operation.
    """
    wallet = await wallet_service.get(db, wallet_uuid)
    # DEPOSIT operation mapping from schemas.py
    if operation_data.operation_type == "+":
        if not wallet:
            wallet = await wallet_service.create(db, wallet_uuid, operation_data.amount)
            response.status_code = status.HTTP_201_CREATED
            return wallet
    # WITHDRAW operation mapping from schemas.py
    if operation_data.operation_type == "-":
        if not wallet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Wallet with ID {wallet_uuid} not found",
            )
        if wallet.balance < operation_data.amount:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient wallet balance",
            )
    wallet = await wallet_service.update(db, wallet, operation_data)
    return wallet
