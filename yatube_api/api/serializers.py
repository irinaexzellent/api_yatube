from rest_framework import serializers
from posts.models import Post, Group, Comment


class CommentSerializer(serializers.ModelSerializer):
    """Класс для преобразования сложных данных в простые типы данных Python,
    которые конвертируются в JSON.
    """
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ("post",)


class CommentListSerializer(serializers.ModelSerializer):
    """Класс для преобразования сложных данных в простые типы данных Python,
    которые конвертируются в JSON.
    """

    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    """Класс для преобразования сложных данных в простые типы данных Python,
    которые конвертируются в JSON.
    """
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        fields = ('id', 'text', 'author',
                  'group', 'image', 'pub_date', 'comments')
        model = Post


class GroupSerializer(serializers.ModelSerializer):
    """Класс для преобразования сложных данных в простые типы данных Python,
    которые конвертируются в JSON.

    Методы:
    create -- сохранение экземпляра объекта в базе
    """
    class Meta:
        fields = ('id', 'title', 'slug', 'description')
        model = Group

    def create(self, validated_data):
        return Group.objects.create(**validated_data)
