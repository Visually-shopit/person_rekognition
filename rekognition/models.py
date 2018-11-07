from django.db import models


class ImageRekognition(models.Model):
    picture = models.ImageField(upload_to='pictures')

    def __str__(self):
        return self.picture


class VideoRekognition(models.Model):
    video = models.FileField(upload_to='videos')

    def __str__(self):
        return self.video
