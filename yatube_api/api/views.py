from rest_framework import viewsets
from rest_framework.decorators import api_view

from posts.models import Post, Group, Comment
from .serializers import PostSerializer, GroupSerializer
from .serializers import CommentSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.permissions import IsAuthenticated


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Объектный уровень разрешения - позволяет редактировать
    объект только автору объекта.
    Предполагается, что экземпляр модели имеет аттрибут "author".
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    """
    Простой ViewSet для просмотра и редактирования постов.

    Разрешения -- доступ разрешен аутифенцированному пользователю и
    запрещен неаутифенцированному.

    Объектный уровень разрениений -- позволяет
    редактировать объект только автору объекта.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated & IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Простой ViewSet для просмотра и редактирования комментариев постов.

    Разрешения -- доступ разрешен аутифенцированному пользователю и
    запрещен неаутифенцированному.

    Объектный уровень разрениений -- позволяет
    редактировать объект только автору объекта.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated & IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, post_id=self.kwargs.get("post_id")
        )

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        new_queryset = Comment.objects.filter(post=post_id)
        return new_queryset


@api_view(['GET'])
def api_groups(request):
    """View-функция возвращает объеект класса Response;
    в этот объект в качестве аргумента передаётся
    Python-словарь в JSON формате.

    Ключевые аргументы:
    groups -- список объектов класса Group,
    serializer -- Python-словарь, сконвертированный в JSON
    """
    if request.method == 'POST':
        return Response(status=status.HTTP_400_BAD_REQUEST)
    groups = Group.objects.all()
    serializer = GroupSerializer(groups, many=True)
    return Response(serializer.data)
