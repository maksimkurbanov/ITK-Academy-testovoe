import asyncio
import uvicorn
from fastapi import FastAPI
from src.config import dev_settings
from src.api.v1.wallets.router import router as wallets_router


app = FastAPI()

app.include_router(wallets_router)


@app.get("/")
async def root():
    """For simple healthcheck"""
    return {"message": "Hello, World!"}


async def main():
    config = uvicorn.Config(
        "main:app", host=dev_settings.SERVER_HOST, port=dev_settings.SERVER_PORT
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
