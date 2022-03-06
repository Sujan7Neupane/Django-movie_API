from rest_framework import serializers
from movie_app.models import WatchList, StreamPlatform, Review

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ['watchlist']
        # fields = "__all__"

class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = WatchList
        # exclude = ['watchlist']
        fields = "__all__"

class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)
    # watchlist = serializers.StringRelatedField(many=True) -------->for String relatedField
    # watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True) ===> for Pk read_only
    # watchlist = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='watch-details') --> for links

    class Meta:
        model = StreamPlatform
        fields = "__all__"
        # exclude = ['watchlist']
  
#  ---------------> for custom extra field which is not in database
# def get_len_name(self, object):
#     length = len(object.name)
#     return length
#  ---------------> for custom extra field which is not in database

#validators(third type of validation)
# function name in name
# def name_length(name):
#     if len(name) < 3:
#         raise serializers.ValidationError("Name is too short!. It must be more than 3 letters")
# **********************************************************************************************

#serializers.Serialzers class **********************************************************
# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     # name = serializers.CharField()
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)

#     def update(self, instance, new_data):
#         instance.name = new_data.get('name',instance.name)
#         instance.description = new_data.get('description',instance.description)
#         instance.active = new_data.get('active', instance.active)

#         instance.save()
#         return instance
#serializers.Serialzers class **********************************************************

    #validation example for name field
    #field level validation(first type of validations)
    # def validate_name(self, value): 
    #     if len(value) < 3:
    #         raise serializers.ValidationError("Name is too short!. It must be more than 5 letters")
    #     else:
    #         return value

    #Object level validation(third type of validation)
    #to validate two or more fields
    # def validate(self, data):
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError("Title and description should not be same")
    #     else:
    #         return data




