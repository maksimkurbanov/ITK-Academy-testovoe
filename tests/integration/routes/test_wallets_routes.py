import pytest
import uuid
from random import randint
from fastapi import status


prefix = "api/v1/wallets"


@pytest.mark.asyncio
async def test_create_wallet(client):
    """Create a new wallet"""
    wallet_uuid, amount = uuid.uuid4(), randint(1, 1000)

    response = await client.post(
        f"{prefix}/{wallet_uuid}/operation",
        json={"operation_type": "DEPOSIT", "amount": amount},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["balance"] == amount


@pytest.mark.asyncio
async def test_get_nonexisting_wallet_balance(client):
    """Get balance of a non-existing wallet"""
    wallet_uuid = uuid.uuid4()
    response = await client.get(f"{prefix}/{wallet_uuid}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == f"Wallet with ID {wallet_uuid} not found"


@pytest.mark.asyncio
async def test_get_existing_wallet_balance(client):
    """Get balance of an existing wallet"""
    wallet_uuid, amount = uuid.uuid4(), randint(1, 1000)

    await client.post(
        f"{prefix}/{wallet_uuid}/operation",
        json={"operation_type": "DEPOSIT", "amount": amount},
    )

    response = await client.get(f"{prefix}/{wallet_uuid}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["balance"] == amount


@pytest.mark.asyncio
async def test_update_balance_correct_amount(client):
    """
    Update balance of an existing wallet:

    DEPOSIT: deposit amount twice and check result against 2*amount
    WITHDRAW: withdraw 1*amount from balance of 2*amount
    (from previous deposit operations) and check against 1*amount
    """
    wallet_uuid, amount = uuid.uuid4(), randint(1, 1000)

    await client.post(
        f"{prefix}/{wallet_uuid}/operation",
        json={"operation_type": "DEPOSIT", "amount": amount},
    )
    response = await client.post(
        f"{prefix}/{wallet_uuid}/operation",
        json={"operation_type": "DEPOSIT", "amount": amount},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["balance"] == 2 * amount
    response = await client.post(
        f"{prefix}/{wallet_uuid}/operation",
        json={"operation_type": "WITHDRAW", "amount": amount},
    )
    assert response.status_code == 200
    assert response.json()["balance"] == amount


@pytest.mark.asyncio
async def test_cannot_withdraw_below_zero(client):
    """
    Make sure withdrawing below 0 is prohibited:

    deposit amount once, then withdraw same amount
    (resulting in balance of 0), then try to withdraw again
    """

    wallet_uuid, amount = uuid.uuid4(), randint(1, 1000)

    await client.post(
        f"{prefix}/{wallet_uuid}/operation",
        json={"operation_type": "DEPOSIT", "amount": amount},
    )
    response = await client.post(
        f"{prefix}/{wallet_uuid}/operation",
        json={"operation_type": "WITHDRAW", "amount": amount},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["balance"] == 0
    response = await client.post(
        f"{prefix}/{wallet_uuid}/operation",
        json={"operation_type": "WITHDRAW", "amount": amount},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Insufficient wallet balance"


@pytest.mark.asyncio
async def test_negative_amount(client):
    """Make sure negative amount is not allowed"""
    wallet_uuid, amount = uuid.uuid4(), randint(-1000, -1)

    response = await client.post(
        f"{prefix}/{wallet_uuid}/operation",
        json={"operation_type": "DEPOSIT", "amount": amount},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json()["detail"][0]["msg"] == "Input should be greater than 0"
    response = await client.post(
        f"{prefix}/{wallet_uuid}/operation",
        json={"operation_type": "WITHDRAW", "amount": amount},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json()["detail"][0]["msg"] == "Input should be greater than 0"


@pytest.mark.asyncio
async def test_zero_amount(client):
    """Make sure zero amount is not allowed"""
    wallet_uuid, amount = uuid.uuid4(), 0

    response = await client.post(
        f"{prefix}/{wallet_uuid}/operation",
        json={"operation_type": "DEPOSIT", "amount": amount},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json()["detail"][0]["msg"] == "Input should be greater than 0"
    response = await client.post(
        f"{prefix}/{wallet_uuid}/operation",
        json={"operation_type": "WITHDRAW", "amount": amount},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json()["detail"][0]["msg"] == "Input should be greater than 0"


@pytest.mark.asyncio
async def test_none_amount(client):
    """Make sure None (defaults to null in JSON) amount is not allowed"""
    wallet_uuid, amount = uuid.uuid4(), None

    response = await client.post(
        f"{prefix}/{wallet_uuid}/operation",
        json={"operation_type": "DEPOSIT", "amount": amount},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json()["detail"][0]["msg"] == "Input should be a valid integer"
    response = await client.post(
        f"{prefix}/{wallet_uuid}/operation",
        json={"operation_type": "WITHDRAW", "amount": amount},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json()["detail"][0]["msg"] == "Input should be a valid integer"


@pytest.mark.asyncio
async def test_missing_amount(client):
    """Make sure requests without "amount" field are denied"""
    wallet_uuid = uuid.uuid4()

    response = await client.post(
        f"{prefix}/{wallet_uuid}/operation", json={"operation_type": "DEPOSIT"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json()["detail"][0]["msg"] == "Field required"
    response = await client.post(
        f"{prefix}/{wallet_uuid}/operation", json={"operation_type": "WITHDRAW"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json()["detail"][0]["msg"] == "Field required"


@pytest.mark.asyncio
async def test_wrong_operation_type(client):
    """
    Make sure operation_type values in requests belong to
    allowed types (case-sensitive).

    Test cases have last letters in operation types in lower-case
    """
    wallet_uuid, amount = uuid.uuid4(), randint(1, 1000)

    response = await client.post(
        f"{prefix}/{wallet_uuid}/operation",
        json={"operation_type": "DEPOSIt", "amount": amount},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert (
        response.json()["detail"][0]["msg"] == "Input should be 'DEPOSIT' or 'WITHDRAW'"
    )
    response = await client.post(
        f"{prefix}/{wallet_uuid}/operation",
        json={"operation_type": "WITHDRAw", "amount": amount},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert (
        response.json()["detail"][0]["msg"] == "Input should be 'DEPOSIT' or 'WITHDRAW'"
    )


@pytest.mark.asyncio
async def test_none_operation_type(client):
    """Make sure None (defaults to null in JSON) operation_type is not allowed"""
    wallet_uuid, amount = uuid.uuid4(), randint(1, 1000)

    response = await client.post(
        f"{prefix}/{wallet_uuid}/operation",
        json={"operation_type": None, "amount": amount},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert (
        response.json()["detail"][0]["msg"] == "Input should be 'DEPOSIT' or 'WITHDRAW'"
    )


@pytest.mark.asyncio
async def test_missing_operation_type(client):
    """Make sure requests without "operation_type" field are denied"""
    wallet_uuid, amount = uuid.uuid4(), randint(1, 1000)

    response = await client.post(
        f"{prefix}/{wallet_uuid}/operation", json={"amount": amount}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json()["detail"][0]["msg"] == "Field required"


@pytest.mark.asyncio
async def test_missing_operation_type_and_missing_amount(client):
    """Make sure requests without "amount" AND "operation_type" fields are denied"""
    wallet_uuid = uuid.uuid4()

    response = await client.post(f"{prefix}/{wallet_uuid}/operation", json={})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    for elem in response.json()["detail"]:
        assert elem["msg"] == "Field required"
