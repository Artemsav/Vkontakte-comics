# Vkontakte comics

## Project description

Script for downloading a random comic from the site [xkcd](xkcd.com) and automatically uploading it to public in [VK](vk.com/)
To run the script please type in console:

```bash
python main.py
```

## Instalation

Python3 should be already installed. Then use pip (or pip3, if there is a conflict with Python2) to install dependencies:

```bash
pip install -r requirements.txt
```

There is enviroment variables using in the application, you will need tp create ```.env``` file. A ```.env``` file is a text file containing key value pairs of all the environment variables required by the application. You can see example of it below:

```python
# example of environment variables defined inside a .env file
VK_ACCESS_TOKEN=533bacf01e1165b57531ad114461ae8736d6506a3

VK_GROUP_ID=213043905

VK_APP_CLIENT_ID=233434
```

VK_ACCESS_TOKEN - Get the user's access key. It is needed so that your application has access to your account and can post messages in groups. The key can be obtained manually without writing a single line of code. You need the following permissions: photos, groups, wall and offline. Please follo the [link](https://dev.vk.com/api/access-token/implicit-flow-user)

VK_GROUP_ID - Create group in VK. Group id you can get via [this service](https://regvk.com/id/)

VK_APP_CLIENT_ID - To get it, you need to create a ```standalone``` application in [VK](https://dev.vk.com/). You will get ```client_id``` of your application

## Project Goals

The code is written for educational purposes on online-course for web-developers [Devman](https://dvmn.org)
