from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .forms import ImageForm
from django.http import HttpResponseRedirect
from .models import ImageModel, ImageMetaDataModel
from PIL import Image, ImageDraw, ExifTags, ImageColor
from django.conf import settings

import boto3

def index(request):
    return HttpResponse("Hello, world. You're at the image analyze app index.")


def upload(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            imageModel = form.save()

            session = boto3.Session(profile_name='hackday2019', region_name='us-west-2')
            client = session.client('rekognition')

            with open(imageModel.image.file.name, 'rb') as img:
                response = client.detect_labels(Image={'Bytes': img.read()})

            # read content of response
            labels = response['Labels']

            # check image height, width
            imageHeight = imageModel.image.height
            imageWidth = imageModel.image.width

            for item in labels:
                if len(item['Instances']) != 0:
                    # Synthesize the name of whatever was found
                    name = item['Name']
                    polly_client = boto3.Session(profile_name='hackday2019', region_name='us-west-2').client('polly')
                    response = polly_client.synthesize_speech(VoiceId='Joanna', OutputFormat='mp3', Text=name)
                    # Save synthesized word
                    file = open(settings.MEDIA_ROOT + '/sound/' + name + '.mp3', 'wb')
                    file.write(response['AudioStream'].read())
                    file.close()
                    print('Synthesized and saved ' + name + '.mp3')

                    # Get the bounding boxes
                    for instance in item['Instances']:
                        boundingBox = instance['BoundingBox']
                        print(boundingBox)

                        model = ImageMetaDataModel()
                        model.x1 = boundingBox['Left'] * imageWidth
                        model.y1 = boundingBox['Top'] * imageHeight
                        model.x2 = (boundingBox['Left'] + boundingBox['Width']) * imageWidth
                        model.y2 = (boundingBox['Top'] + boundingBox['Height']) * imageHeight
                        model.image = imageModel
                        model.sound = name + '.mp3'
                        model.save()

            return HttpResponseRedirect('/')
    else:
        form = ImageForm()
    return render(request, 'upload.html', {'form': form})

def detail(request, id):
    imageModel = ImageModel.objects.get(id=id)
    metaDatas = ImageMetaDataModel.objects.filter(image=imageModel)
    return render(request, 'view_image.html', {'image': imageModel, 'metadatas': metaDatas})