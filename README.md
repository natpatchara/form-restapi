# Checkbox and radio button labelling api

Github repository for automatic Checkbox and radiobutton labelling API

## Table of contents
* [Table of contents](#Table-of-contents)
* [project structure](#Project-structure)
* [Technologies](#Technologies)
* [Setup](#Setup)
* [Status](#Status)
* [Documentation](#Document)

## Project structure
```
    .
    ├── bin                     # Directory for server starter script
    ├── resource                # Directory for main python API handler
    ├── script                  # Directory for python image processing script
    ├── test                    # Directory for example test image and result
    ├── Dockerfile              # File for running start and run docker constainer
    ├── requirement.txt         # Text file containing requirement library
    ├── app.py                  # Python script for routing flask server
    ├── wsgi.py                 # Python script for start wsgi server
    └── README.md

```

## Technologies
* python 3.9.7
* Flask 1.1.2
* Flask-RESTful==0.3.8
* opencv-python-headless==4.5.1.48
* Pillow==8.2.0
* gunicorn==20.1.0

## Setup

In progress

## Status
As of writing this markdown file, this project is compatible for small real world usage. Example of such API was hosted and have already been taken down before.
Example of some input and output image to such API can be found in test directory.

In summary our current features and todo includes:

* features
    * Working script for hosting working docker container.
    * Server for handling input API request accoring to REST API methodology.
    * Working image processing script for automatic detection of checkbox and radio button using conventional computer vision algorithm

* todo
    * Improve documentation
    * Intensive testing
    * Optimization
    * Diversify algorithm for detection including recent method such as CNN 


## Documentations

* **URL**

  `/label`
  

* **Method:**
  
  `POST`
  
  
*  **URL Params**
 
   `-`


* **Data Params**
 
    * `image`
   
      list of `image object` handled by API
    
      <pre>
      <b>image object</b>   
      
      dictionary represent individual image 
          
      have following keys/values pair
     
        'base64' : image content encoded in base64 string format
      </pre>    
   
   * `op_type`
   
      type of operator wanted to do (can be either `'Checkbox'` or `'Radio'`)
      
   
   * `params`
   
      dictionary of keys,values of parameters to use when label image (varied according to type of operator)
      

* **Response:**

    **Content:**
    
    
    * `status`
    
      status of API call will return 'success' or _details of error_ accordingly
      
    
    * `results`
      
      list of `result` return from API with same order as image supplied
         
      <pre>
      <b>result</b>
          
      dictionary repreent result processed from API 
          
      have following keys/values pairs
      
        'type' : type of operator done on image
         
        'coords': list of coordination marking area as specify by operator type (dictionary consist of x,y,w,h keys)
      </pre>
