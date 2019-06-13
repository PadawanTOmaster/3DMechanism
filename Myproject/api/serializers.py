from rest_framework import serializers
from rest_framework.reverse import reverse
from user_information import models as models1
from download import models as models2
from encyclopedia import models as models4
from exercise import models as exercisemodel
from news import models as newsmodel
from rest_framework_jwt.settings import api_settings
# Create your views here.


class SignupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models1.userInfor
        fields = ('username','nickname', 'email', 'information', 'flag')


class GetInforSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models1.userInfor
        fields = ('username', 'nickname', 'information','avatar')



class DownloadFileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=models2.download
        fields=('id','filepath','imgpath','filename','description')


class EncyclopediaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=models4.encyclopedia
        fields=('title','context')


class FillblanksSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = exercisemodel.fillblanks
        fields = ('number', 'problem', 'answere1', 'answere2',
                'answere3', 'answere4', 'answere5', 'answere6',
                'answere7', 'answere8', 'keyword1', 'keyword2', 'keyword3')

class DrawingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=exercisemodel.drawing
        fields =(
            'number','problemtext','problemimg','answereimg','keyword1','keyword2','keyword3','type','hasthreed'
        )


class NewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = newsmodel.schoolnews
        fields = (
            'title','news_content','release_time','URL','read_count'
        )