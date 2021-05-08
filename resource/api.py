from flask import jsonify
from flask_restful import Resource, reqparse
import werkzeug
from io import BytesIO
import base64
import script.image_processing as improc
from PIL import Image

class binary_api(Resource):
  def __init__(self):
    # Create a request parser
    parser = reqparse.RequestParser()
    parser.add_argument("image", type=werkzeug.datastructures.FileStorage, location='files')
    # Sending more info in the form? simply add additional arguments, with the location being 'form'
    # parser.add_argument("other_arg", type=str, location='form')
    self.req_parser = parser

    # This method is called when we send a POST request to this endpoint
  def post(self):
  	# The image is retrieved as a file
    image_file = self.req_parser.parse_args(strict=True).get("image", None)
        
    if (image_file):
      img = Image.open(image_file)
      return jsonify({'msg': 'success', 'size': [img.width, img.height]})

    else:
      return jsonify({"msg":"no image found"})

class path_api(Resource):
  def __init__(self):
    # Create a request parser
    parser = reqparse.RequestParser()
    parser.add_argument("path", type=str, action='append')
    # Sending more info in the form? simply add additional arguments, with the location being 'form'
    # parser.add_argument("other_arg", type=str, location='form')
    self.req_parser = parser

    # This method is called when we send a POST request to this endpoint
  def post(self):
  	# The image is retrieved as a file
    image_path = self.req_parser.parse_args(strict=True).get("path", None)
        
    '''if (image_file):
      img = Image.open(image_file)
      return jsonify({'msg': 'success', 'size': [img.width, img.height]})

    else:
      return jsonify({"msg":"no image found"})'''
    print(image_path)

class base64_api(Resource):

  def __init__(self):
    # Create a request parser
    parser = reqparse.RequestParser()
    parser.add_argument("image", type=str, action='append')
    # Sending more info in the form? simply add additional arguments, with the location being 'form'
    # parser.add_argument("other_arg", type=str, location='form')
    self.req_parser = parser

    # This method is called when we send a POST request to this endpoint
  def post(self):
  	# The image is retrieved as a file
    imgs = self.req_parser.parse_args(strict=True).get("image", None)
        
    '''if (image_file):
      img = Image.open(image_file)
      return jsonify({'msg': 'success', 'size': [img.width, img.height]})

    else:
      return jsonify({"msg":"no image found"})'''


    if len(imgs) == 0: return jsonify({"msg": "no image found"})

    for img in imgs:
      print(img[:20])
      if img is not None:
        
        decoded_img = base64.b64decode(img)
        img = Image.open(BytesIO(decoded_img))
        
        file_name = "test.jpg"
        img.save(file_name, "jpeg")
        return jsonify({'msg': 'success', 'size': [img.width, img.height]})

      '''  # Base64 DATA
      elif "data:image/png;base64," in img:
        decoded_img = base64.b64decode(img)
        img = Image.open(BytesIO(decoded_img))

        file_name = "test.png"
        img.save(file_name, "png")
        return jsonify({'msg': 'success', 'size': [img.width, img.height]})
      '''

class label(Resource):

  def __init__(self):
    parser = reqparse.RequestParser()
    parser.add_argument("image", type=dict, action="append")
    parser.add_argument("op_type", type=str)
    parser.add_argument("params", type=dict)

    self.req_parser = parser

  def loadbase64(self,base64_img):

    try:
      img = base64.b64decode(base64_img)
      decoded_img = Image.open(BytesIO(img)).convert('RGBA')
      
      status = "Succesfully decode base64 image"
    except Exception as e:
        status = "Error! = " + str(e)
        decoded_img=None
    return (decoded_img,status)

  def post(self):
    args = self.req_parser.parse_args()
    imgs = args.get("image",None)
    op_type = args.get("op_type",None)
    params = args.get("params",None)
    
    if(params is None): params = {}
    results = []

    if (op_type == "Checkbox"): op = improc.checkbox_detector
    elif (op_type == "Radio"): op = improc.radio_button_detector
    elif (op_type == None): op = improc.checkbox_detector
    else: return jsonify({"result":None, "status":"Operator type not support refer to ... for details"})
    
    for img in imgs:
      if "base64" in img:
        decoded_img,status = self.loadbase64(img["base64"])
        
        if (decoded_img is None): return jsonify({"result":None,"status":status})
        
      
      res,status = op(decoded_img, **params)
      
      if res is None: return jsonify({"result":None,"status":status}) 

      results.append(res)
    
    return jsonify({"result":results,"status":"success"})



    


      

  def get(self):
    pass