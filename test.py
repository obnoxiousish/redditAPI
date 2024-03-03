import trio
import json

from httpx import AsyncClient

class testRedditAPI:
    def __init__(self):
        self.baseUrl = 'https://www.reddit.com/'
        self.client = AsyncClient(
            headers={
                'User-Agent': 'windows:vLT1l6xwqp6Qrq8ZTPioGA:0.0.1 (by /u/obnoxiousfr)',
            },
            verify=False
        )
        
        self.accessToken = None

    async def testing(self):
        await self.access_token()
        await self.search()
        
    async def search(self, query='hannahowo'):
        resp = await self.client.get(self.baseUrl + 'api/v1/search', params={
            'q': query,
            'type': 'sr,user',
            'include_over_18': 'on',
            'include_unadvertisable': 'on',
        })
        jsonData = resp.json()
        
        print(json.dumps(jsonData, indent=4))

    async def access_token(self):
        resp = await self.client.post(self.baseUrl + 'api/v1/access_token', data={
            'grant_type': 'password',
            'username': 'obnoxiousfr',
            'password': 'Apple123!',
            'scope': 'read',
        }, auth=('vLT1l6xwqp6Qrq8ZTPioGA', 'puwxyidhesbnCBC4l0EzEqBes8rBvg'))
        jsonData = resp.json()
        
        if jsonData.get('access_token'):
            self.client.headers['Authorization'] = f'Bearer {jsonData["access_token"]}'
            self.accessToken = jsonData['access_token']
        
        print(f'Access Token: {self.accessToken}')
        
    async def me(self):
        resp = await self.client.get(self.baseUrl + 'api/v1/me')
        jsonData = resp.json()
        
        print(json.dumps(jsonData, indent=4))
        
if __name__ == '__main__':
    test = testRedditAPI()
    trio.run(test.testing)