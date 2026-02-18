from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from enum import StrEnum


class Wallet(BaseModel):
    uuid: UUID
    balance: int = Field(ge=0)

class WalletResponse(BaseModel):
    balance: int = Field(ge=0)

class AllowedOperations(StrEnum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"

class WalletOperationRequest(BaseModel):
    operation_type: AllowedOperations
    amount: int = Field(gt=0)   # Only allow positive operation amounts

    @field_validator("operation_type")
    @classmethod
    def map_operation_str(cls, val: str):
        operation_map = {"DEPOSIT": "+", "WITHDRAW": "-"}
        if val in operation_map:
            return operation_map[val]
        raise ValueError("Invalid operation type")

class WalletOperationResponse(BaseModel):
    pass
