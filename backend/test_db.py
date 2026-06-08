import asyncio
from dotenv import load_dotenv
load_dotenv()

from app.database.postgres import engine
from app.database.mongo import init_mongo

async def test():
    try:
        async with engine.begin() as conn:
            print('Postgres connected successfully')
    except Exception as e:
        print(f'Postgres error: {e}')

    try:
        await init_mongo()
        print('Mongo connected successfully')
    except Exception as e:
        print(f'Mongo error: {e}')

asyncio.run(test())
