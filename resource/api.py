from flask import jsonify
from flask_restful import Resource, reqparse
from io import BytesIO
import base64
import script.image_processing as improc
from PIL import Image

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
    '''
    Current Post request handler
    Only accept base64 image req
    Might expand to haddle further format
    # more information will be documented in future  
    '''
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

    '''
    Empty GET request handler
    Might implement to return document when request 
    
    '''

    pass