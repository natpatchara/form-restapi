import requests
import base64
from PIL import Image
from io import BytesIO
import numpy as np
import cv2
import json


def send_base64(src,oper_type,params={}):
  url = 'http://127.0.0.1:8080/label'
  with open(src, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
  test = {'image':[{"base64":encoded_string}],'op_type':oper_type,'params':params}
  return requests.post(url, json=test)

def display_response(src,res):
  img = cv2.imread(src)
  res = res.json()
  if(res['status'] == 'success'):
    coords = res['result'][0]['coords']
  
    for coord in coords:
      x = int(coord['x'])
      y = int(coord['y'])
      w = int(coord['w'])
      h = int(coord['h'])
      cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.imwrite("test/output-test/test.jpg",img)
  
  return res['status']

test_file = "test/test7.png"
res = send_base64(test_file,'Radio')

# convert server response into JSON format.
print(display_response(test_file,res))
#print(r.json())