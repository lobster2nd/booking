from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .permissions import IsSupplierOrReadOnly
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.models import ApiUser, Storage, Product
from api.serializers import UserSerializer, StorageSerializer, ProductSerializer


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


class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    permission_classes = [IsAuthenticatedOrReadOnly, IsSupplierOrReadOnly]

    def perform_create(self, serializer):
        name = self.request.data.get('name')
        amount = self.request.data.get('amount')
        storage_id = self.request.data.get('storage')
        storage = get_object_or_404(Storage, id=storage_id)
        existing_product = Product.objects.filter(name=name, storage=storage).first()

        if existing_product:
            existing_product.amount += int(amount)
            existing_product.save()
        else:
            serializer.save(user=self.request.user, storage=storage, name=name, amount=amount)


