from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Base(DeclarativeBase):
    pass


class Wallet(Base):
    __tablename__ = "wallet"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    balance: Mapped[int] = mapped_column(
        Integer, CheckConstraint("balance >= 0", name="check_balance_non_negative")
    )
