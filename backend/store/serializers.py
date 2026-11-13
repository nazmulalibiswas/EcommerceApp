from rest_framework import serializers
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.hashers import make_password
from .models import (
    Users, Categories, Products, Cart, CartItem, 
    Orders, OrderItems, Payments, Reviews
)


class UserSerializer(serializers.ModelSerializer):
    # Maps 'username' to 'full_name' so frontend code expecting 'username' works
    username = serializers.CharField(source='full_name', read_only=True)

    class Meta:
        model = Users
        fields = ['id', 'username', 'full_name', 'email', 'phone', 'role']


class RegisterSerializer(serializers.ModelSerializer):
    # Maps incoming 'username' from frontend directly to 'full_name'
    username = serializers.CharField(source='full_name', required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Users
        fields = ['username', 'email', 'password', 'password2']

    def validate_email(self, value):
        # Only block if the user already exists in BOTH tables
        if Users.objects.filter(email=value).exists() and AuthUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        full_name = validated_data['full_name']
        email = validated_data.get('email', '')
        raw_password = validated_data['password']

        # 1. Save in Django's built-in auth_user table (Required for JWT Login)
        auth_user, _ = AuthUser.objects.update_or_create(
            username=full_name,
            defaults={
                'email': email,
                'is_active': True,
            }
        )
        auth_user.set_password(raw_password)
        auth_user.save()

        # 2. Save in your custom PostgreSQL 'users' table (With role='buyer')
        user, _ = Users.objects.update_or_create(
            email=email,
            defaults={
                'full_name': full_name,
                'password_hash': make_password(raw_password),
                'role': 'buyer',
                'country': 'Bangladesh',
                'email_verified': False,
                'phone_verified': False,
                'is_active': True,
                'is_approved': True,
                'is_blocked': False,
                'language': 'en',
                'currency': 'BDT',
            }
        )
        return user


class CategoriesSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Categories
        fields = '__all__'

    def get_parent(self, obj):
        if obj.parent:
            return {
                "id": obj.parent.id,
                "name": obj.parent.name,
                "slug": obj.parent.slug,
                "description": obj.parent.description,
                "image_url": obj.parent.image_url.url if obj.parent.image_url else None
            }
        return None


class ProductsSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)

    class Meta:
        model = Products
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.title', read_only=True)
    product_price = serializers.DecimalField(source='product.sale_price', max_digits=10, decimal_places=2, read_only=True)
    product_image = serializers.CharField(source='product.image_url', read_only=True)

    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = '__all__'


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = '__all__'


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = '__all__'