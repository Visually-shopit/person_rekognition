from django import forms


class ImageForm(forms.Form):
    upload_image = forms.FileField(required=True)


class VideoForm(forms.Form):
    upload_video = forms.FileField(required=True)
