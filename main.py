import os

import asyncpg
import asyncio

from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from app.routers import auth, notifications


DATABASE_URL = f"postgres://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"


async def wait_for_db():
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '5432')
    user = os.getenv('DB_USER', 'postgres')
    password = os.getenv('DB_PASS', 'secret')
    db_name = os.getenv('DB_NAME', 'notifications_db')

    retries = 5
    while retries > 0:
        try:
            connection = await asyncpg.connect(
                user=user,
                password=password,
                database='postgres',
                host=host,
                port=port,
            )
            print("Connected to the PostgreSQL server!")

            result = await connection.fetchval('SELECT 1 FROM pg_database WHERE datname=$1', db_name)
            if result:
                print(f"Database '{db_name}' already exists.")
            else:
                await connection.execute(f'CREATE DATABASE {db_name}')
                print(f"Database '{db_name}' created.")
            await connection.close()
            return
        except Exception as e:
            retries -= 1
            print(f"Failed to connect to database. Retrying... {retries} attempts left")
            await asyncio.sleep(5)


async def startup():
    await wait_for_db()


app = FastAPI(on_startup=[startup])

app.include_router(auth.router)
app.include_router(notifications.router)

register_tortoise(
    app,
    db_url=f"postgres://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
    modules={"models": ["app.models.user", "app.models.notification"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
