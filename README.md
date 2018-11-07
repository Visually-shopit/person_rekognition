# Objects Detection in uploaded Image/Video
Detects Objects in the Image(using AWS Rekognition API) and Video(using Clarifai API)

We need to upload an image/video file by going 127.0.0.1:8000/image or 127.0.0.1:8000/video urls respectively.
Python script written in Django views.py will upload it AWS or Clarifai and get the reponse and will show it at the frontend screen.

## Installations

 * AWS Rekognition API:
 
  1. sudo pip install boto3

  2. sudo nano /etc/boto.cfg

    [Credentials]
    aws_access_key_id=xxxxxxxxxxxx
    aws_secret_access_key=xxxxxxxxxxxxxxxxxxxxxxxx
   
   
  * Clarifai API:
 
  1. sudo pip install clarifai --upgrade
