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


async def item_get(item_, item_k,):
    return item_.get(item_k)


async def get_f(url_):
    session_ = aiohttp.ClientSession()
    response_ = await session_.get(url_)
    response_json_ = await response_.json()
    await session_.close()
    return response_json_


async def f(item_, item_key_, name_):
    if item_.get(item_key_):
        crs = []
        for i in item_.get(item_key_):
            coruntine_ = get_f(i)
            crs.append(coruntine_)
        result_ = await asyncio.gather(*crs)
        names_list = []
        for res in result_:
            names_list.append(res.get(name_, ''))
        name_str = ','.join(names_list)
        return name_str
    else:
        return ''


async def paste_to_db(results):
    swapi_people = [SwapiPeople(birth_year=item.get('birth_year'),
                                eye_color=item.get('eye_color'),
                                # films=','.join(item.get('films', '')),
                                films=await f(item, 'films', 'title'),
                                gender=item.get('gender'),
                                hair_color=item.get('hair_color'),
                                height=item.get('height'),
                                homeworld=item.get('homeworld'),
                                mass=item.get('mass'),
                                name=item.get('name'),
                                skin_color=item.get('skin_color'),
                                species=await f(item, 'species', 'name'),
                                starships=await f(item, 'starships', 'name'),
                                vehicles=await f(item, 'vehicles', 'name'))
                    for item in results]
    async with Session() as session:
        session.add_all(swapi_people)
        await session.commit()


async def main():
    start = datetime.datetime.now()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    session = aiohttp.ClientSession()
    coros = (get_people(session, i) for i in range(1, 84))
    for coros_chunk in chunked(coros, CHUNK_SIZE):
        results = await asyncio.gather(*coros_chunk)
        # pprint(results)
        asyncio.create_task(paste_to_db(results, ))

    await session.close()
    set_tasks = asyncio.all_tasks()
    for task in set_tasks:
        if task != asyncio.current_task():
            await task

    stop = datetime.datetime.now()
    print(stop - start)

if __name__ == '__main__':
    asyncio.run(main())
