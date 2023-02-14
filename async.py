import asyncio
import aiohttp
import datetime
from more_itertools import chunked
from models import engine, Session, SwapiPeople, Base

CHUNK_SIZE = 10

async def get_people(session, people_id):
    async with session.get(f'https://swapi.dev/api/people/{people_id}/') as response:
        json_data = await response.json()
        return json_data

async def paste_to_db(results):
    swapi_people = [SwapiPeople(json=item) for item in results]
    async with Session() as session:
        session.add_all(swapi_people)
        await session.commit()


async def main():
    start = datetime.datetime.now()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session = aiohttp.ClientSession()
    coros = (get_people(session, i) for i in range(1, 84))
    for coros_chunk in chunked(coros, CHUNK_SIZE):
        results = await asyncio.gather(*coros_chunk)
        print(results)
        asyncio.create_task(paste_to_db(results))

    await session.close()
    set_tasks = asyncio.all_tasks()
    for task in set_tasks:
        if task != asyncio.current_task():
            await task

    stop = datetime.datetime.now()
    print(stop - start)

if __name__ == '__main__':
    asyncio.run(main())
