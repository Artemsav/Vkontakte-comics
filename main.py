import requests
import urllib
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
import random
from requests import HTTPError


class VkApiError(HTTPError):
    """An VKApi error occurred."""


def get_extention(url):
    scheme, netloc, path, *_ = urlparse(url)
    clean_path = urllib.parse.unquote(path)
    head, tail = os.path.split(clean_path)
    root, extention = os.path.splitext(tail)
    return extention


def get_last_comics_page():
    response = requests.get('https://xkcd.com/info.0.json')
    response.raise_for_status()
    return response.json()['num']


def download_random_comics(url):
    response = requests.get(url)
    response.raise_for_status()
    fetch_response = response.json()
    image_url = fetch_response['img']
    ext = get_extention(image_url)
    img_response = requests.get(image_url)
    img_response.raise_for_status()
    filename = f'image{ext}'
    with open(filename, 'wb') as file:
        file.write(img_response.content)
    return (filename, fetch_response['alt'])


def handle_vk_exceptions(response):
    decode_response = response.json()
    if decode_response.get('error'):
        raise VkApiError(decode_response['error']['error_msg'])


def get_wall_upload_server(vk_access_token, vk_group_id, vk_api_version):
    upload_params = {
        'group_id': vk_group_id,
        'access_token': vk_access_token,
        'v': vk_api_version
        }
    upload_response = requests.get('https://api.vk.com/method/photos.getWallUploadServer', params=upload_params)
    upload_response.raise_for_status()
    handle_vk_exceptions(upload_response)
    return upload_response


def upload_pict_to_server(vk_group_id, upload_response, filename):
    upload_url = upload_response.json()['response']['upload_url']
    with open(filename, 'rb') as file:
        upl_url = upload_url
        files = {
            'group_id': vk_group_id,
            'photo': file,
            }
        response = requests.post(upl_url, files=files)
        response.raise_for_status()
        handle_vk_exceptions(response)
    return response


def save_wall_photo(vk_access_token, vk_group_id, vk_api_version, response):
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
    handle_vk_exceptions(save_response)
    return save_response


def post_to_wall(vk_access_token, vk_group_id, vk_api_version, response):
    fetch_save_response = response.json()
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
    wall_response = requests.post(save_wall_url, params=wall_params)
    wall_response.raise_for_status()
    handle_vk_exceptions(wall_response)


if __name__ == '__main__':
    load_dotenv()
    vk_access_token = os.getenv('VK_ACCESS_TOKEN')
    vk_group_id = os.getenv('VK_GROUP_ID')
    vk_api_version = '5.131'
    try:
        last_comics = get_last_comics_page()
        rand_num = random.randint(1, last_comics)
        url = f'https://xkcd.com/{rand_num}/info.0.json'
        filename, message = download_random_comics(url)
        upload_response = get_wall_upload_server(
            vk_access_token,
            vk_group_id,
            vk_api_version
            )
        wall_upload_server = upload_pict_to_server(
            vk_group_id,
            upload_response,
            filename
            )
        wall_photo = save_wall_photo(
            vk_access_token,
            vk_group_id,
            vk_api_version,
            wall_upload_server
            )
        post_to_wall(vk_access_token, vk_group_id, vk_api_version, wall_photo)
    finally:
        os.remove(filename)
