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
