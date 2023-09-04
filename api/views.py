from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.models import ApiUser, Storage, Product
from api.serializers import UserSerializer, StorageSerializer, ProductSerializer

from .permissions import IsSupplierOrReadOnly


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = ApiUser.objects.all()
    http_method_names = ['post', 'get']
    serializer_class = UserSerializer

    authentication_classes = [TokenAuthentication,
                              SessionAuthentication,
                              ]
    permission_classes = []


class StorageModelViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer

    permission_classes = [IsAuthenticatedOrReadOnly, IsSupplierOrReadOnly]


class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    permission_classes = [IsAuthenticatedOrReadOnly, IsSupplierOrReadOnly]

    def perform_create(self, serializer):
        """Add product to storage. Only supplier can do it"""
        name = self.request.data.get('name')
        storage_id = self.request.data.get('storage')
        storage = get_object_or_404(Storage, id=storage_id)
        serializer.save(user=self.request.user, storage=storage, name=name)

    @action(detail=True, methods=['get', 'post'])
    def take_item(self, request):
        """Take product from storage. Only user can do it"""
        if request.user.cat != 'Пользователь':
            return Response("Недостаточно прав. Только пользователь может забрать товар",
                            status=403)
        product = self.get_object()
        product.delete()
        return Response("Элемент успешно забран")
