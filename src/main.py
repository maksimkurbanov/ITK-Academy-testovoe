import asyncio
import uvicorn
from fastapi import FastAPI
from src.config import settings
from src.api.v1.wallets.router import router as wallets_router


app = FastAPI()

app.include_router(wallets_router)

@app.get("/")
async def root():
    return {"message":"Hello, World!"}

async def main():
    uvicorn.run(
        app="main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True if settings.ENV != "production" else False
    )

if __name__ == "__main__":
    asyncio.run(main())
    # with asyncio.Runner() as runner:
    #     runner.run(main())
        # asyncio.run(main(), loop_factory=asyncio.SelectorEventLoop)
