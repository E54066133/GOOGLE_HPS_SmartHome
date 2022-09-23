import socket
import threading
import time
import pyimgur                            # pip3 install pyimgur

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
# Port to listen on (non-privileged ports are > 1023)
PORT_TRAIN = 5432
PORT_CAPTURE = 4321

def retrain():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT_TRAIN))
        s.sendall(b"ReTrain")
        data = s.recv(1024)
        print(data)

print("sleeping")
time.sleep(3)
def capture():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT_CAPTURE))
        s.sendall(b"Capture")
        _ = s.recv(1024)
            
    CLIENT_ID = '05b1a88cedb5f8f'                   # 修改 'client_id'
    PATH = "capture.png"               #A Filepath to an image on your computer"
    title = "Uploaded with PyImgur"
    
    PATH_small = "capture_small.png"
    
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=title)
    uploaded_image_small = im.upload_image(PATH_small, title=title)
    print(uploaded_image.title)
    print(uploaded_image.link)
    print(uploaded_image.type)
    print("###################")
    print(uploaded_image_small.title)
    print(uploaded_image_small.link)
    print(uploaded_image_small.type)
    return uploaded_image.link, uploaded_image_small.link
        

