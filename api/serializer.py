from rest_framework import serializers
from rest_framework.fields import empty
from accounts.serilizer import PostUserSerializer
from .models import Catagory, Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ( 'id', 'title', 'author','slug')

class PostDetailSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields  = kwargs.pop('fields', None)
        super(PostDetailSerializer,self).__init__(*args,**kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def create(self, validated_data):
        catagory = validated_data.pop('category')
        object = Catagory.objects.get(name = catagory)
        validated_data['category'] = object
        instance =  self.Meta.model(**validated_data)
        instance.save()
        return instance
    author = PostUserSerializer(read_only=True)
    queryset = Catagory.objects.all()
    categoryChoices = []
    for query in queryset:
        categoryChoices.append(query.name)
    category = serializers.ChoiceField(categoryChoices)
    class Meta:
        model = Post 
        fields = '__all__'
        depth = 1
