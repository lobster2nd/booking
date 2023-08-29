from rest_framework import serializers
from rest_framework import validators

from api.models import ApiUser, Storage, Product


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128, validators=[
        validators.UniqueValidator(ApiUser.objects.all())
    ])
    email = serializers.EmailField(validators=[
        validators.UniqueValidator(ApiUser.objects.all())
    ])
    password = serializers.CharField(min_length=6, max_length=20, write_only=True)
    cat = serializers.ChoiceField(choices=ApiUser.CATEGORY_CHOICES)

    def update(self, instance, validated_data):
        if email := validated_data.get("email"):
            instance.email = email
            instance.save(update_fields=["email"])

        if password := validated_data.get("password"):
            instance.set_password(password)
            instance.save(update_fields=["password"])

        return instance

    def create(self, validated_data):
        user = ApiUser.objects.create(
            email=validated_data["email"],
            username=validated_data["username"],
            cat=validated_data["cat"],
        )

        user.set_password(validated_data["password"])
        user.save(update_fields=["password"])
        return user


class StorageSerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    def get_product_count(self, storage):
        total_count = 0
        for product in storage.items.all():
            total_count += product.amount
        return total_count

    class Meta:
        model = Storage
        fields = ['id', 'name', 'product_count']
        extra_kwargs = {"id": {"read_only": True}}


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['name', 'amount', 'storage', 'user']
        read_only_fields = ['user']
        extra_kwargs = {"id": {"read_only": True}}
