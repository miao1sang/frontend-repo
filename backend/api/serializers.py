from rest_framework import serializers

from blog.models import User, Blog, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'u_name': {'required': False},
        }


class BlogSerializer(serializers.ModelSerializer):
    u_name = serializers.CharField(source='u_id.u_name', read_only=True)
    avatar = serializers.ImageField(source='u_id.avatar', read_only=True)

    class Meta:
        model = Blog
        fields = '__all__'
        extra_kwargs = {
            'u_id': {'required': False},
        }


class CommentSerializer(serializers.ModelSerializer):
    u_name = serializers.CharField(source='u_id.u_name', read_only=True)
    avatar = serializers.ImageField(source='u_id.avatar', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
