import requests
import asyncio
import aiohttp
import datetime

from async_models import init_db, engine, Session, People
from pprint import pprint
from more_itertools import chunked


async def character(client, id_character):
    http_resp = await client.get(f'https://swapi.dev/api/people/{id_character}/')
    result = await http_resp.json()
    return result

async def get_data(client, url_):
    http_resp = await client.get(url_)
    result = await http_resp.json()
    return result

async def insert_db(datas):
    models = []
    res =  People(**datas)
    models.append(res)
    async with Session() as session:
        session.add_all(models)
        await session.commit()
  
MAX_CHUNK = 5
async def main():
    await init_db()

    client = aiohttp.ClientSession()
    
    # 
    for chunk in chunked(range(1, 90), MAX_CHUNK) :
        print('OTSECHKA 1 ', ' - '*10)
        print('chunk', chunk)
        coros = [character(client, person_id) for person_id in chunk]
        list_dicts_people =  await asyncio.gather(*coros)
        print()
        print()
        for dict_man in list_dicts_people:
            
            # test for data is real
            if 'name' not in dict_man :
                continue

            #     # add_films
            print('NAME == ', dict_man['name'])
            film_list_coros = [get_data(client, one_url) for one_url in dict_man['films']]
            list_dicts_films = await asyncio.gather(*film_list_coros)
            list_films =  [film_data['title'] for film_data in list_dicts_films]
            films_str = ', '.join(list_films)
            if len(films_str) == 0 :
                films_str = 'no data'
            # print('films_str == ', films_str)

            # # # add_species
            species_list_coros = [get_data(client, one_url) for one_url in dict_man['species']]
            list_dicts_species = await asyncio.gather(*species_list_coros)
            list_species =  [species_data['name'] for species_data in list_dicts_species]
            species_str = ', '.join(list_species)
            if len(species_str) == 0 :
                species_str = 'no data'
            # print(species_str)

            # # # add_starships
            starships_list_coros = [get_data(client, one_url) for one_url in dict_man['starships']]
            list_dicts_starships = await asyncio.gather(*starships_list_coros)
            list_starships =  [starships_data['name'] for starships_data in list_dicts_starships]
            starships_str = ', '.join(list_starships)
            if len(starships_str) == 0 :
                starships_str = 'no data'
            # print('starships_str == ',  starships_str)

            # # # add_vehicles
            vehicles_list_coros = [get_data(client, one_url) for one_url in dict_man['vehicles']]
            list_dicts_vehicles = await asyncio.gather(*vehicles_list_coros)
            list_vehicles =  [vehicles_data['name'] for vehicles_data in list_dicts_vehicles]
            vehicles_str = ', '.join(list_vehicles)
            if len(vehicles_str) == 0 :
                vehicles_str = 'no data'
            # print('vehicles_str == ', vehicles_str)

            # # add_homeworld
            coro = get_data(client, dict_man['homeworld'])
            list_dict_home = await asyncio.gather(coro)
            homeworld = list_dict_home[0]['name']

            data_dict = {
                'birth_year': dict_man['birth_year'],
                'eye_color': dict_man['eye_color'],
                'films': films_str,
                'gender': dict_man['gender'],
                'hair_color': dict_man['hair_color'],
                'height': dict_man['height'],
                'homeworld': homeworld,
                'mass': dict_man['mass'],
                'name': dict_man['name'],
                'skin_color': dict_man['skin_color'],
                'species': species_str,
                'starships': starships_str,
                'vehicles': vehicles_str
            }       


            # pprint(data_dict)
            print('INSERT !!')
            print()
            asyncio.create_task(insert_db(data_dict))

    tasks_set = asyncio.all_tasks()
    tasks_set.remove(asyncio.current_task())
    await asyncio.gather(*tasks_set)
    
    print()
    await client.close()
    print(' - await client.close()')

    await engine.dispose()

if __name__=='__main__':
    start = datetime.datetime.now()
    asyncio.run(main())
    finish = datetime.datetime.now()
    print('TIME : ', finish - start)