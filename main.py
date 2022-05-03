import requests
import urllib
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
import random


def get_extention(url):
    scheme, netloc, path, _, _, _ = urlparse(url)
    clean_path = urllib.parse.unquote(path)
    head, tail = os.path.split(clean_path)
    root, extention = os.path.splitext(tail)
    return extention


def download_random_comics(url):
    response = requests.get(url)
    response.raise_for_status()
    fetch_response = response.json()
    image_url = fetch_response['img']
    ext = get_extention(image_url)
    img_responce = requests.get(image_url)
    img_responce.raise_for_status()
    with open(f'image{ext}', 'wb') as file:
        file.write(img_responce.content)


def get_comment(url):
    response = requests.get(url)
    response.raise_for_status()
    fetch_response = response.json()
    return fetch_response['alt']


def wall_post():
    pass


if __name__ == '__main__':
    load_dotenv()
    vk_access_token = os.getenv('VK_ACCESS_TOKEN')
    vk_group_id = os.getenv('VK_GROUP_ID')
    vk_app_id = os.getenv('VK_APP_CLIENT_ID')
    vk_api_version = '5.131'
    last_comics = 2614
    rand_int = random.randint(1, last_comics)
    url = f'https://xkcd.com/{rand_int}/info.0.json'
    download_random_comics(url)
    message = get_comment(url)
    upload_params = {
        'group_id': vk_group_id,
        'access_token': vk_access_token,
        'v': vk_api_version
        }
    upload_response = requests.get('https://api.vk.com/method/photos.getWallUploadServer', params=upload_params)
    upload_response.raise_for_status()
    upload_url = upload_response.json()['response']['upload_url']
    with open('image.png', 'rb') as file:
        upl_url = upload_url
        files = {
            'group_id': vk_group_id,
            'photo': file,
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
        fetch_save_response = save_response.json()
        save_wall_url = 'https://api.vk.com/method/wall.post'
        owner_id = fetch_save_response['response'][0]['owner_id']
        media_id = fetch_save_response['response'][0]['id']
        attachments = f'photo{owner_id}_{media_id}'
        wall_params = {
            'owner_id': f'-{vk_group_id}',
            'group_id': vk_group_id,
            'access_token': vk_access_token,
            'v': vk_api_version,
            'from_group': 1,
            'attachments': attachments,
            'message': message
            }
        save_wall_response = requests.post(save_wall_url, params=wall_params)
    os.remove('image.png')
