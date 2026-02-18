from src.config import get_settings
from src.database import build_sqlalchemy_database_url_from_settings, get_ctx_db
from functools import partial
from src.api.v1.wallets.service import WalletService
from uuid import UUID


def seed_database(env):
    """
    Seed the database with initial data.

    Parameters:
        env (str): The environment in which the database is being seeded.
    """

    settings = get_settings(env)
    database_url = build_sqlalchemy_database_url_from_settings(settings)
    get_db = partial(get_ctx_db, database_url=database_url)

    with get_db() as session:
        test_wallet_uuid = UUID("6a2ac0d5-0f9e-43e9-a509-ff6c10ee4f46")
        test_user = WalletService.create(session, UUID, amount=1000)

    # create_first_superuser(session) = create_first_user(session) = user_crud.create(db, UserIn)
    # =WalletService.create