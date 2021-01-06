from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Post, Comment

User = get_user_model()


class CustomPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):

    def to_representation(self, value):
        rep = super().to_representation(value)
        user = User.objects.filter(pk=rep).first()
        # user = self.queryset.filter(pk=rep).first()  # when read_only=False

        return user.__str__()


class PostSerializer(serializers.ModelSerializer):
    owner = CustomPrimaryKeyRelatedField(
            # queryset=User.objects.all(),
            many=False, required=False, read_only=True)

    class Meta:
        model = Post
        fields = ['title', 'body', 'created', 'owner']


class PostDetailSerializer(serializers.ModelSerializer):
    # comment_set = serializers.SerializerMethodField(method_name=get_comment_set)
    comment_set = serializers.HyperlinkedRelatedField(view_name='comment_detail', many=True, read_only=True)
    owner = CustomPrimaryKeyRelatedField(many=False, required=False, read_only=True)

    class Meta:
        model = Post
        fields = ['title', 'body', 'created', 'updated', 'owner', 'comment_set']

    # def get_comment_set(self):


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['body']
