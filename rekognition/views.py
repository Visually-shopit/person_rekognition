# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from .forms import ImageForm, VideoForm
from .models import ImageRekognition, VideoRekognition

import boto3  # This is for image recognition using AWS Rekognition API
from clarifai.rest import Video as ClVideo  # This is for video recognition using clarifai API
from clarifai.rest import ClarifaiApp
import json
import codecs
from pprint import pprint

client = boto3.client('rekognition', region_name='us-east-1')        # specify the region_name
media_path = "/home/prasad/Desktop/image_rekognition/mysite/media/"  # Specify media file_path

app = ClarifaiApp()
model = app.models.get('general-v1.3')


def get_image_from_pc(filename):                # This function help me to get the images from the pc
    with open(filename, 'rb') as imgfile:
        return imgfile.read()


def image_rekognition(request):
    if request.method == 'POST':
        form = ImageForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            print 'Image Form is Valid!'
            media_file = ImageRekognition(picture=request.FILES['upload_image'])
            media_file.save()

            file_path = ImageRekognition.objects.latest('picture').picture
            image_path = media_path + str(file_path)
            print 'Image Path:', image_path
            # Image read from the PC will be in raw image (digital image)
            imgbytes = get_image_from_pc(image_path)
            response = client.detect_labels(Image={'Bytes': imgbytes}, MinConfidence=1)
            labels = []

            for label in response['Labels']:
                labels.append(label['Name'] + ' : ' + str(label['Confidence']) + ' %')

            for ele in labels:
                print ele

            context = {
                "response": labels
            }
            return render(request, "image_response.html", context)
    else:
        context = {
            "form": ImageForm(),
        }
        return render(request, "image_form.html", context)


def video_rekognition(request):
    if request.method == 'POST':
        form = VideoForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            print 'Video Form is Valid!'
            media_file = VideoRekognition(video=request.FILES['upload_video'])
            media_file.save()

            file_path = VideoRekognition.objects.latest('video').video
            video_path = media_path + str(file_path)
            print 'Video Path:', video_path
            template_video_path = "/media/" + str(file_path)
            print 'Template Video Path:', template_video_path

            video = ClVideo(filename=video_path)
            clarifai_response = model.predict([video])

            # save response locally to display the video contents at the frontend
            file_name = video_path + '.json'
            with codecs.open(file_name, 'w', 'utf-8') as ww:
                json.dump(clarifai_response, ww, ensure_ascii=False,
                          indent=2)   # Store the response in a file

            json_data = json.load(open(file_name))
            frame = []
            list_data = []
            probabilities = {}
            for elements in json_data['outputs'][0]['data']['frames']:
                for attributes in elements['data']['concepts']:
                    list_data.append({
                        'name': attributes['name'],
                        'probability': attributes['value']
                    })
                frame.append(list_data)
                list_data = []

            probabilities['data'] = list_data
            response = json.dumps(frame)
            context = {
                "response": response,
                "video_path": template_video_path
            }
            return render(request, "video_response.html", context)
    else:
        context = {
            "form": VideoForm(),
        }
        return render(request, "video_form.html", context)
