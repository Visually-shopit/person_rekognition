# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import ImageRekognition, VideoRekognition

# Register your models here.
admin.site.register(ImageRekognition)
admin.site.register(VideoRekognition)
