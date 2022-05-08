from typing import Generator

import motor.motor_asyncio

from ..config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)


def get_db() -> Generator:
    db = None
    try:

        db = client.test_first_vds
        yield db
    finally:
        pass
