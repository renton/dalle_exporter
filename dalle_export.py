import requests
import time

from config import COLLECTION_ID, AUTH_BEARER

RESOURCE_LIMIT = 30
SLEEP_AMOUNT = 0.5

DOWNLOAD_PATH = "."

SAVED_IMAGES_URL = f"https://labs.openai.com/api/labs/collections/{ COLLECTION_ID }/generations"

def get_png_url(gen_id):
    return f"https://labs.openai.com/api/labs/generations/{ gen_id }/download"

def make_request(page_num=1):
    url = f"{ SAVED_IMAGES_URL }?page=1&limit={ RESOURCE_LIMIT }&page={ page_num }"
    print(url)
    r = requests.get(
            url,
            params = {},
            headers={'Authorization': f"Bearer {AUTH_BEARER}"}
    )

    return r.json()

def download_image(image_url, filename):
    print(image_url)
    filename = filename.replace(' ','_').replace(',','-').replace('"','-').replace("'",'-')
    with open(f"{ DOWNLOAD_PATH }/{ filename }.png", 'wb') as f:
        f.write(requests.get(
            image_url,
            headers={'Authorization': f"Bearer {AUTH_BEARER}"}
        ).content)

if __name__ == "__main__":
    meta_req = make_request()

    num_pages = meta_req['total_pages']
    num_models = meta_req['total_models']

    gen_data = {}

    for i in range(num_pages):
        page_num = i+1
        try:
            gen_req = make_request(page_num)
        except Exception as e:
            print("\n!!!!!!!!!!!!!!!!"+str(e)+"\n")
        for gen in gen_req['data']:
            if gen['id'] not in gen_data:
                prompt = gen['prompt']['prompt']['caption'] if 'caption' in gen['prompt']['prompt'] else ""
                gen_data[gen['id']] = {
                        'p':prompt,
                        'i':gen['generation']['image_path']
                }
        time.sleep(SLEEP_AMOUNT)
        break

    for k,v in gen_data.items():
        try:
            print("\n"+v['p'])
            download_image(get_png_url(k), v['p']+'_'+k)
        except Exception as e:
            print("\n!!!!!!!!!!!!!!"+str(e)+"\n")
        time.sleep(SLEEP_AMOUNT)
