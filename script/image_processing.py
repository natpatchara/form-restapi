import numpy as np
import cv2

def transform_image(img):
  img = np.asarray(img)
  
  img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
  
  return img

def process_image(img):
  '''
    placeholder function for image processing script(simple function that return size of image input)
  '''
  if img is not None:   
    return [img.width, img.height],"success"
  else:
    return None,"no image given"

def checkbox_detector(img, minBoxSize = 25, maxBoxSize = -1
              , boxSize = -1, boxSizeRange = 25
              , aspectRatio = 1, aspectRatioRange = 0.2
              , gapWidth = 2):
  '''
    function to detect checkbox in a form given as a image 
    It is derived using morphology transformation to detect line then combine to detect 
    connected area as box according to specific condition(size, aspect ratio, etc.)
    
    parameter:
      img : image to be processed; for checkbox detection(currently accept PIL-supported image format but can be expand to accept opencv-supproted image format)
      minBoxSize : parameter for minimum box size detected by function (also use as minimum lenght of line detect in function)
      maxBoxSize : parameter for maximum box size detected by function (if given size is lower than minimum box size treated as no maximum limit)
      boxSize : parameter which can be given if specific box size is needed (override minBoxsize and maxBoxSize if given)
                    [used in conjuction with boxSizeRange to get range of size wanted by function]
                    (if negative value or zero is given function will use min and max box size given before)
      boxSizeRange : parameter used in conjuction with boxSize to calculate range of size wanted by function
            {at least one of minBoxSize or boxSize must be positive or else exception will be thrown}
            {size is define as minimum of width or height}
      aspectRatio : parameter for wanted aspect ratio of checkbox (if given value is negative treated as all aspect ratio is wanted)
      aspectRatioRange : parameter for error of acceptable aspect ratio
                                  (ie. if 0.2 is given 0.8-1.2 * aspectRatio is acceptable)
                                  [if given value > 1 exception will be thrown]
      gapWidth : parameter for gap in line that is acceptable and will be filled

    default value:
      minBoxSize : 25
      maxBoxsize : -1
      boxSize : -1
      boxSizeRange : 25
      aspectRatio : 1
      aspectRatioRange : 0.2
      gapWidth : 5

      output:
      image : image with all checkbox wanted annotated

  '''

  try:
    #Check if box size is  specified if yes calculated acceptable range
    if (boxSize > 0):
      minBoxSize = max(boxSize - abs(boxSizeRange) ,1)
      maxBoxSize = boxSize + abs(boxSizeRange)

    if (minBoxSize <= 0): 
      raise ValueError("at least one of boxSize or minBoxSize must be given as positive value")
    
    if (aspectRatioRange > 1):
      raise ValueError("aspectRatioRange shouldn't exceed 1")

    #define accesory function
    def fix(img):
      img[img>127]=255
      img[img<127]=0
      return img
    
    #load image from path
    image = transform_image(img)
    
    #change image to gray scale then threshold to get binary image
    gray_scale=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    th1,img_bin = cv2.threshold(gray_scale,150,255,cv2.THRESH_BINARY)

    #Create kernel for line detection
    kernal1h = np.ones((1,gapWidth), np.uint8)
    kernal1v = np.ones((gapWidth,1), np.uint8)
    kernal6h = np.ones((1,minBoxSize), np.uint8)
    kernal6v = np.ones((minBoxSize,1), np.uint8)

    #Detect specific morphology(line)
    img_bin_h = cv2.morphologyEx(~img_bin, cv2.MORPH_CLOSE, kernal1h) # bridge gap in horizontal lines
    img_bin_h = cv2.morphologyEx(img_bin_h, cv2.MORPH_OPEN, kernal6h) # keep horizontal lines of minimal lenght
    img_bin_v = cv2.morphologyEx(~img_bin, cv2.MORPH_CLOSE, kernal1v) # bridge small gap in vertical lines
    img_bin_v = cv2.morphologyEx(img_bin_v, cv2.MORPH_OPEN, kernal6v) # keep only vertical lines by eroding everything else in vertical direction

    #combine horizontal and vertical line to create box
    img_bin_final = fix(fix(img_bin_h)|fix(img_bin_v))

    #dilate to bridge gap
    finalKernel = np.ones((5,5), np.uint8)
    img_bin_final=cv2.dilate(img_bin_final,finalKernel,iterations=1)

    # select connected component (mainly box)
    ret, labels, stats,centroids = cv2.connectedComponentsWithStats(~img_bin_final, connectivity=8, ltype=cv2.CV_32S)

    # calculate acceptable aspect ratio range
    max_aspect_ratio = aspectRatio * (1 + abs(aspectRatioRange))
    min_aspect_ratio = aspectRatio * (1 - abs(aspectRatioRange))
  ### skipping first two stats as background and select box according to condition
    results = {"coords":[],"type":"checkbox"}

    for x,y,w,h,area in stats[2:]:
      area_aspect_ratio = w/h
      if ( (maxBoxSize > minBoxSize and (w > maxBoxSize and h > maxBoxSize)) or (aspectRatio > 0 and (area_aspect_ratio > max_aspect_ratio or area_aspect_ratio < min_aspect_ratio))):
        continue
      print([x,y,w,h])
      results['coords'].append({'x':str(x-5),'y':str(y-5),'w':str(w+10),'h':str(h+10)})

    status = "success"
  except Exception as e:
    status = "Error! = " + str(e)
    results = None

  return results,status
  
def generate_kernel(d = 20):
  '''
  function for create empty circle kernel
  param:
    d : circle diameter which want kernel to generate
  output:
    kernel of specify size
  '''
  #create temporary kernel to hold kernel of circle inside(area)
  temp = np.zeros((d,d),np.uint8)
  temp[1:-1,1:-1] = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(d-2,d-2))
  
  #substracted frm larger circle to get kernel of only outline
  kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(d,d)) - temp
  return kernel

def radio_button_detector(img, minRadius = 20, maxRadius = 50, stepWidth = 3, numIter = 1):
  '''
    function to detect radio button in form given as a image 
    It is derived using morphology transformation to detect circle then detect 
    connected area as a button according specific condition(mainly radius range)
    
    parameter:
      src : file path for form given as image (acceptable file type are on accepted by cv2.imread function)
      minRadius : parameter for minimum cirlce radius detected by function
      maxRadius : parameter for maximum circle radius detected by function 
      stepWidth : parameter for step used in iteration over radius range(higher mean faster but more likely to get false negative)
      numIter : parameter for number of iteration of dilation before try detecing circle(higher mean less false negative but more false positive)

    default value:
      minRadius : 20
      maxRadius : 50
      stepWidth : 3
      numIter : 1

      output:
      image : image with radio button annotated
  '''
  def fix(img):
    img[img>127]=255
    img[img<127]=0
    return img
  
  try:
  #transform image to given format
    image = transform_image(img)
  
  #preprocess image to get binary image
    gray_scale=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    th1,img_bin = cv2.threshold(gray_scale,200,255,cv2.THRESH_BINARY)

  #delete solid component of image and keep only outline
    temp = cv2.dilate(img_bin,None,  iterations = 2)
    temp = cv2.erode(temp,None, iterations = 2)
    img_process = ~img_bin - ~temp
  
  #dilate image to make outline thicker (making it less susceptible to radius variation)
    img_process  = cv2.dilate(img_process,None, numIter)

  #create final blank image to hold all image found using all radius in given range
    img_final = np.zeros(img_process.shape, dtype = "uint8")

  #loop over given radius range with step width specify between each iteration
    for radius in range(minRadius, maxRadius + stepWidth, stepWidth):
      kernel = generate_kernel(radius*2)
      temp = cv2.erode(img_process,kernel)
      temp = cv2.dilate(temp,kernel)
      img_final = img_final | temp

  #fix image to be binary image
    fix(img_final)

  #find connected area mainly radio button
    ret, labels, stats,centroids = cv2.connectedComponentsWithStats(img_final, connectivity=8, ltype=cv2.CV_32S)

    results = {'coords':[],'type':'radio'}
    #draw all button detected
    for x,y,w,h,area in stats[1:]:
      area_aspect_ratio = w/h
      if ( (w > radius*2+5 and h > radius*2+5) or (area_aspect_ratio > 1.2 or area_aspect_ratio < 0.8)):
        continue
      results['coords'].append({'x':str(x-5),'y':str(y-5), 'w':str(w+10),'h':str(h+10)})

    return results, 'success'
  except Exception as e:
    status = 'Error! = ' + str(e)
    return None,status

  
