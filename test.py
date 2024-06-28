import requests
# import certifi

url = "https://innovation.gov.uz/api/v1/site/post/list/?limit=1000&menu_group=news&menu_slug=&offset=0"
while True:
    r = requests.get(url, verify=False)
    print(r.status_code)