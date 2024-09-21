import requests, json


class KASINA:
    def __init__(self):
        self.url = "https://www.kasina.co.kr/product-detail/"

    def url_setting(self, url):
        return url.split("/")[-1]

    def get_clientid(self, product_code):
        header = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'ccept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Host': 'shop-api.e-ncp.com',
            'Origin': 'https://www.kasina.co.kr',
            'Referer': 'https://www.kasina.co.kr/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'company': 'Kasina/Request',
            'platform': 'PC',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'version': '1.'
        }
        req = requests.get(f"https://www.kasina.co.kr/product-detail/{product_code}", headers=header)
        js_kansina = "https://static.kasina-store.com/_next/static/chunks/pages/_app" + req.text.split("ext/static/chunks/pages/_app")[-1].split('" ')[0]
        req = requests.get(js_kansina)
        return req.text.split(',clientId:"')[-1].split('",')[0]

    def run(self, product_code):
        if "kasina" in product_code:
            product_code = self.url_setting(product_code)
        clientId = self.get_clientid(product_code)
        payload = {}
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Host': 'shop-api.e-ncp.com',
            'Origin': 'https://www.kasina.co.kr',
            'Referer': 'https://www.kasina.co.kr/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'clientid': clientId,
            'company': 'Kasina/Request',
            'platform': 'PC',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'version': '1.0'
        }
        url = f"https://shop-api.e-ncp.com/products/{product_code}?useCache=true"
        req = requests.get(url, headers=headers, data=payload)
        try:
            output = {
                "Name": req.json()["baseInfo"]["productNameEn"],
                "Model": req.json()["baseInfo"]["productManagementCd"],
                "Image": f'https:{req.json()["baseInfo"]["imageUrls"][0]}',
                "Price": req.json()["price"]["salePrice"],
                "Url": "https://www.kasina.co.kr/product-detail/"+ str(product_code),
                "Stock": {},
            }
        except:
            output = {
                "Stock"
            }
        url = f"https://shop-api.e-ncp.com/products/{product_code}/options?useCache=true"

        req = requests.get(url, headers=headers, data=payload)
        for i in req.json()["multiLevelOptions"]:
            data = {
                i["value"]: i["stockCnt"]
            }
            output["Stock"].update(data)
        return output


url = "https://www.kasina.co.kr/product-detail/123245137"

# print(json.dumps(KASINA().run(url), ensure_ascii=False, indent=4))