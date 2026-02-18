import pytest
from tests.conftest import client, TEST_SQLALCHEMY_DATABASE_URL
from tests.integration.conftest import get_test_db
from src.api.v1.wallets.service import WalletService
import uuid
import os


prefix = "api/v1/wallets"
wallet_uuid_fixed = uuid.UUID('19fc4b9c-09d6-49bf-8bc5-332a370f5e3d')


# @pytest.mark.asyncio
# async def test_get_fixed_wallet_balance(client):
#     response = await client.get(f"{prefix}/{wallet_uuid_fixed}")
#     print(response.content)
#
# @pytest.mark.asyncio
# async def test_get_wallet_balance2(client):
#     response = await client.get(f"{prefix}/{wallet_uuid}")
#     print(response.content)
#
# @pytest.mark.asyncio
# async def test_get_fixed_wallet_balance3(client):
#     response = await client.get(f"{prefix}/{wallet_uuid_fixed}")
#     print(response.content)


@pytest.mark.asyncio
async def test_create_wallet(client):
    wallet_uuid = uuid.uuid4()
    response = await client.post(f"{prefix}/{wallet_uuid}/operation", json={"operation_type":"DEPOSIT", "amount":333})
    print("ENV variable: ", os.getenv("ENV"))
    print("DB URL USED: ",os.environ.get("POSTGRES_HOST"))
    assert response.status_code == 200
    assert response.json()["balance"] == 333

@pytest.mark.asyncio
async def test_get_nonexisting_wallet_balance(client):
    wallet_uuid = uuid.uuid4()
    response = await client.get(f"{prefix}/{wallet_uuid}")
    print("ENV variable: ", os.getenv("ENV"))
    print("DB URL USED: ", os.getenv("POSTGRES_HOST"))
    assert response.status_code == 404
    assert response.json()["detail"] == f"Wallet with ID {wallet_uuid} not found"

@pytest.mark.asyncio
async def test_get_fixed_wallet_balance_no_pref(client):
    response = await client.get(f"{prefix}/{wallet_uuid_fixed}")
    print("ENV variable: ", os.getenv("ENV"))
    print("DB URL USED: ", os.getenv("POSTGRES_HOST"))
    print(response.content)

# @pytest.mark.asyncio
# async def test_get_fixed_wallet_balance3(client):
#     response = await client.get(f"{prefix}/{wallet_uuid_fixed}")
#     print(response.content)



