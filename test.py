import trio
import json

from httpx import AsyncClient

class testRedditAPI:
    def __init__(self):
        self.baseUrl = 'https://www.reddit.com/'
        self.client = AsyncClient(
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
                # 'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Sec-GPC': '1',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Connection': 'keep-alive',
                # 'Cookie': 'loid=000000000vdsz1pwyo.2.1709431603764.Z0FBQUFBQmw0OXMxWlB5MnNKenhyRGYzY013UUc4djZELVFsc2JHdHFGVWdCYUFOWWRaVFV6dENwSnVLTzg5dmloSnlwRmlxYzdnbmlEUTl2MThjYVc5N3VQVkI1Wnk4NXFaLXdFeUwweGhLNTVlVlpsbm1TM2pIeXgwTUFTM3dZU09CNzVCN2hIMDM; csv=2; edgebucket=IGzcKtwxB0WBG4c35y; USER=eyJwcmVmcyI6eyJ0b3BDb250ZW50RGlzbWlzc2FsVGltZSI6MCwiZ2xvYmFsVGhlbWUiOiJSRURESVQiLCJuaWdodG1vZGUiOnRydWUsImNvbGxhcHNlZFRyYXlTZWN0aW9ucyI6eyJmYXZvcml0ZXMiOmZhbHNlLCJtdWx0aXMiOmZhbHNlLCJtb2RlcmF0aW5nIjpmYWxzZSwic3Vic2NyaXB0aW9ucyI6ZmFsc2UsInByb2ZpbGVzIjpmYWxzZX0sInRvcENvbnRlbnRUaW1lc0Rpc21pc3NlZCI6MH19; recent_srs=t5_2tqnh%2Ct5_39009%2Ct5_388p4%2Ct5_3imub%2Ct5_2sf9e%2Ct5_3maow%2Ct5_2qh6i%2Ct5_2ru5b%2Ct5_2t1cc%2Ct5_2qm4e; g_state={"i_l":2,"i_t":1709441540644,"i_p":1709483280849}; over18=true; pc=ci; pref_quarantine_optin=true; theme=1; eu_cookie={%22opted%22:true%2C%22nonessential%22:false}; csrf_token=9c9c26b816e2beb48fdd9d8ad1613478; session=2ab30a99f86507eefd008ead63038eb7ad8b18d6gAWVSQAAAAAAAABKweDjZUdB2TW1NTy0TX2UjAdfY3NyZnRflIwoNWU5ZWY0MGRkZTE4OTQ3MTA3ZTUzMmMxNGE1N2ZkNGFkZDcwYjIzMJRzh5Qu; Helpful_Inside_2072_recentclicks2=t3_fkvn1j%2Ct3_bphwwl%2Ct3_5ye9au%2Ct3_vdtpan%2Ct3_lrc0vl; t2_heiqgg370_recentclicks3=t3_fkvn1j%2Ct3_bphwwl%2Ct3_5ye9au%2Ct3_vdtpan%2Ct3_lrc0vl; session_tracker=hmndcoofjdlopmeipj.0.1709434131154.Z0FBQUFBQmw0LVVUWXZBeTVQRVlwLVZucEozcmtWZzN1cFRORVdoQ2p4WGc2bEw4MlhCV1BKRnAwUnpVMWh5QTdydFV3cHh2NF8yMjdISG5ya25RbS1BRlZSb2l3V3lMNm8tZlpSSUVIeFEwdzZIejEtWlFMVk5ib1F2S2pQQmE1RFJxY0NtTjJaQ1U; token_v2=eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpzS3dsMnlsV0VtMjVmcXhwTU40cWY4MXE2OWFFdWFyMnpLMUdhVGxjdWNZIiwidHlwIjoiSldUIn0.eyJzdWIiOiJ1c2VyIiwiZXhwIjoxNzA5NTE5NDg5LjIxOTM3OSwiaWF0IjoxNzA5NDMzMDg5LjIxOTM3OSwianRpIjoicWxENW5Uc2tpYkhoOV9PUzJjbVFhQ1J1dGlFNndnIiwiY2lkIjoiMFItV0FNaHVvby1NeVEiLCJsaWQiOiJ0Ml92ZHN6MXB3eW8iLCJhaWQiOiJ0Ml92ZHN6MXB3eW8iLCJsY2EiOjE3MDk0MzE2MDM3NjQsInNjcCI6ImVKeGtrZEdPdERBSWhkLWwxejdCX3lwX05odHNjWWFzTFFhb2szbjdEVm9jazcwN2NMNGlIUDhuS0lxRkxFMnVCS0drS1dFRld0T1VOaUx2NTh5OU9aRUZTeUZUUjg0M3l3b2thVXBQVW1ONXB5bFJ3V1prTGxmYXNVS0RCNllwVlM2WjIwS1BTNXZRM0kxRnowNk1xbHhXSHRUWW8zSnBiR01LMnhQanpjWnFReXF1eTZsTVlGa29uOFdMZnZ5Ry10WS1mN2JmaEhZd3JLZ0tEX1RPdUZ4d1lfSERGSGJfbnByMGJGMndxTDNYZzlRLTEtTjI3Yk5tb2RtNV9WelB2emFTY1RtRzVpZll2N3QtQ1IxNDVIbVpVUWN3WWcwX3lyQWo2X0N2T29ES0JRV01KWWhQSTVBcmwyX19KZGl1VGY4YXR5ZC0tR2JFVFdfNHJSbW81eExFb1VfajZ6Y0FBUF9fWERfZTR3IiwicmNpZCI6Ikd6czl6VUt2dkZHcEZjNWFTVXlsQl8tN3lhVGdpeXdZUVJlTW5NdzlLZlEiLCJmbG8iOjJ9.QVGEXGrMjX8VD8kJucUwWxHsnpZwTmxH0GKYnlQGYaUEUANRVD4jOCQi90KkYrLhMBeaujlhKU-6A8xcMZvxivtm-Eyywk7IDz1mVLXkJNkpjKANJoO9oadpd1mOxlYZuU7FhWWzafaCPlndJw12W57wR9bhTsXfjJ3QiIKNwBCs0WiIjpx5vtMRtLnVmKmcjFX84DtvMDmywbksGc28PMAD_yBIXsRwehiu3VhPijxxRdS5lAwVId4diBhdErA8w4x1f8FuH7mMxWUWmPTkLUrF79oJrFepF9O9ec-_f_p7Yct9z8ca-f44I8Wwiiz4Xy7RzRLyhsGQssmBYE7qUw; reddit_session=88536210374688%2C2024-03-03T02%3A07%3A07%2Cff2e222d05c4075ed9bc21d61db0e925ef64cb40; t2_vdsz1pwyo_recentclicks3=t3_z10wzz%2Ct3_k1lo76%2Ct3_18r6n4v%2Ct3_143pcbg%2Ct3_s5ogkm%2Ct3_18d3428%2Ct3_nboz09%2Ct3_8m3kiu%2Ct3_8lllsx%2Ct3_vcpdst',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                # Requests doesn't support trailers
                # 'TE': 'trailers',
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