import anyio
import json

from httpx import AsyncClient

class RedditSearch:
    def __init__(self) -> None:
        self.client = AsyncClient(
            headers={
                'User-Agent': 'windows:vLT1l6xwqp6Qrq8ZTPioGA:0.0.1 (by /u/obnoxiousfr)',
            },
            verify=False
        )
    
    async def search(self, query='hannahowo'):
        resp = await self.client.get('https://www.reddit.com/search.json', params={
            'q': query,
            'type': 'sr,user',
            'include_over_18': 'on',
            'include_unadvertisable': 'on',
        })
        
        return resp.json()
    
if __name__ == '__main__':
    redditSearch = RedditSearch()
    result = anyio.run(redditSearch.search)
    print(json.dumps(result, indent=4))