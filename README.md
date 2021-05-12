**Checkbox and radio button labelling api**
----

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
       
            
* **Sample Call:**

  `To be updated in future`
  

* **Notes:**
