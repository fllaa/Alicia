import aiohttp


class AioHttp:
    @staticmethod
    async def get_json(link, params=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(link, params=params) as resp:
                return await resp.json()

    @staticmethod
    async def get_text(link, params=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(link, params=params) as resp:
                return await resp.text()

    @staticmethod
    async def get_raw(link, params=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(link, params=params) as resp:
                return await resp.read()

    @staticmethod
    async def get(link, params=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(link, params=params) as resp:
                return resp

    @staticmethod
    async def post_json(link, json=None):
        async with aiohttp.ClientSession() as session:
            async with session.post(link, json=json) as resp:
                return await resp.json()
