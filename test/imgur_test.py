# 法一
from imgurpython import ImgurClient     # pip3 install imgurpython
from datetime import datetime


def upload(client_data, album, name = 'test-name!', title = 'test-title' ):
    config = {
        'album':  album,
        'name': name,
        'title': title,
        'description': f'test-{datetime.now()}'
    }

    print("Uploading image... ")
    image = client_data.upload_from_path('test.jpg', config=config, anon=False)
    print("Done")

    return image


if __name__ == "__main__":
    client_id = 'client_id'              # 修改 'client_id'
    client_secret = 'client_secret'      # 修改 'client_secret'
    access_token = "YOUR ACCESS TOKEN"
    refresh_token = "YOUR REFRESH TOKEN"
    album = "album_id"                   # 修改 'album_id'
    local_img_file = "test.jpg"

    client = ImgurClient(client_id, client_secret, access_token, refresh_token)
    image = upload(client, 'test.jpg', album)
    print(f"圖片網址: {image['link']}")
   
  
    
#--------------------------------------------------------------------------------

'''   
#法二
import pyimgur                            # pip3 install pyimgur

CLIENT_ID = "client_id"                   # 修改 'client_id'
PATH = "test.jpg" #A Filepath to an image on your computer"
title = "Uploaded with PyImgur"

im = pyimgur.Imgur(CLIENT_ID)
uploaded_image = im.upload_image(PATH, title=title)
print(uploaded_image.title)
print(uploaded_image.link)
print(uploaded_image.type)
'''
