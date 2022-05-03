from turtle import up
from urllib import request
import requests
import urllib
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
from pprint import pprint

def get_extention(url):
    scheme, netloc, path, _, _, _ = urlparse(url)
    clean_path = urllib.parse.unquote(path)
    head, tail = os.path.split(clean_path)
    root, extention = os.path.splitext(tail)
    return extention


if __name__ == '__main__':
    load_dotenv()
    vk_access_token = os.getenv('VK_ACCESS_TOKEN')
    vk_group_id = os.getenv('VK_GROUP_ID')
    vk_app_id = os.getenv('VK_APP_CLIENT_ID')
    vk_api_version = '5.131'
    url = 'https://xkcd.com/353/info.0.json'
    response1 = requests.get(url)
    response1.raise_for_status()
    image_url = response1.json()['img']
    ext = get_extention(image_url)
    img_responce = requests.get(image_url)
    img_responce.raise_for_status()
    with open(f'image{ext}', 'wb') as file:
        file.write(img_responce.content)
    upload_params = {
        'group_id': vk_group_id,
        'access_token': vk_access_token,
        'v': vk_api_version
        }
    upload_response = requests.get('https://api.vk.com/method/photos.getWallUploadServer', params=upload_params)
    upload_response.raise_for_status()
    pprint(upload_response.json(), indent=4)
    upload_url = upload_response.json()['response']['upload_url']
    with open('image.png', 'rb') as file:
        upl_url = upload_url
        files = {
            'group_id': vk_group_id,
            'photo': file,  # Вместо ключа "media" скорее всего нужно подставить другое название ключа. Какое конкретно см. в доке API ВК.
            }
        response = requests.post(upl_url, files=files)
        response.raise_for_status()
        fetch_response = response.json()
        save_url = 'https://api.vk.com/method/photos.saveWallPhoto'
        params = {
            'group_id': vk_group_id,
            'access_token': vk_access_token,
            'v': vk_api_version,
            'photo': fetch_response['photo'],
            'server': fetch_response['server'],
            'hash': fetch_response['hash']
            }
        save_response = requests.post(save_url, params=params)
        save_response.raise_for_status()
        #pprint(save_response.json(), indent=4)
        fetch_save_response = save_response.json()
        save_wall_url = 'https://api.vk.com/method/wall.post'
        owner_id = fetch_save_response['response'][0]['owner_id']
        message = response1.json()['alt']
        attachments = f'photo{owner_id}{message}'
        wall_params = {
            'group_id': vk_group_id,
            'access_token': vk_access_token,
            'v': vk_api_version,
            'from_group': 1,
            'attachments': attachments,
            'message': 'message'
            }
        save_wall_response = requests.post(save_wall_url, params=wall_params)
        print(save_wall_response.json())
