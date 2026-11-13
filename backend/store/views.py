import uuid
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .models import (
    Users, Categories, Products, Cart, CartItem, 
    Orders, OrderItems, Payments, Reviews
)
from .serializers import (
    RegisterSerializer, UserSerializer, CategoriesSerializer, ProductsSerializer, 
    CartSerializer, CartItemSerializer, OrdersSerializer, OrderItemsSerializer, 
    PaymentsSerializer, ReviewsSerializer
)


# Helper: Maps request.user to your custom PostgreSQL Users model
def get_custom_user(user):
    if isinstance(user, Users):
        return user

    # If user is not logged in (AnonymousUser), fallback to first user in DB
    if not user or not getattr(user, 'is_authenticated', False):
        return Users.objects.first()

    email = getattr(user, 'email', '')
    username = getattr(user, 'username', '')

    custom_user = None
    if email:
        custom_user = Users.objects.filter(email=email).first()
    if not custom_user and username:
        custom_user = Users.objects.filter(full_name=username).first()

    if not custom_user:
        custom_user = Users.objects.create(
            full_name=username or 'user',
            email=email or f"{username or uuid.uuid4().hex[:6]}@example.com",
            password_hash=getattr(user, 'password', ''),
            role='buyer',
            country='Bangladesh',
            email_verified=False,
            phone_verified=False,
            is_active=True,
            is_approved=True,
            is_blocked=False,
            language='en',
            currency='BDT'
        )
    return custom_user


# ১. সব প্রোডাক্ট দেখার জন্য
@api_view(['GET'])
def get_products(request):
    products = Products.objects.all()
    serializer = ProductsSerializer(products, many=True)
    return Response(serializer.data)


# ২. নির্দিষ্ট একটি প্রোডাক্ট দেখার জন্য
@api_view(['GET'])
def get_product(request, pk):
    try:
        product = Products.objects.get(id=pk)
        serializer = ProductsSerializer(product, many=False)
        return Response(serializer.data)
    except Products.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


# ৩. সব ক্যাটেগরি দেখার জন্য
@api_view(['GET'])
def get_categories(request):
    categories = Categories.objects.all()
    serializer = CategoriesSerializer(categories, many=True)
    return Response(serializer.data)


# ৪. সব ইউজার দেখার জন্য
@api_view(['GET'])
def get_users(request):
    users = Users.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


# ৫. কার্ট (Cart) আইটেম দেখার জন্য
@api_view(['GET'])
@permission_classes([AllowAny])
def get_cart(request):
    custom_user = get_custom_user(request.user)
    cart, created = Cart.objects.get_or_create(user=custom_user)
    serializer = CartSerializer(cart)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def add_to_cart(request):
    product_id = request.data.get('product_id')
    if not product_id:
        return Response({'error': 'product_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = Products.objects.get(id=product_id)
    except Products.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    custom_user = get_custom_user(request.user)
    cart, _ = Cart.objects.get_or_create(user=custom_user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return Response({'message': 'Product added to cart', 'cart': CartSerializer(cart).data})


@api_view(['POST'])
@permission_classes([AllowAny])
def update_cart_quantity(request):
    item_id = request.data.get('item_id')
    quantity = request.data.get('quantity')

    if not item_id or quantity is None:
        return Response({'error': 'Item ID and quantity are required'}, status=400)

    try:
        item = CartItem.objects.get(id=item_id)
        if int(quantity) < 1:
            item.delete()
            return Response({'error': 'Quantity must be at least 1'}, status=400)

        item.quantity = int(quantity)
        item.save()
        serializer = CartItemSerializer(item)
        return Response(serializer.data)
    except CartItem.DoesNotExist:
        return Response({'error': 'Cart item not found'}, status=404)


@api_view(['POST'])
@permission_classes([AllowAny])
def remove_from_cart(request):
    item_id = request.data.get('item_id')
    CartItem.objects.filter(id=item_id).delete()
    return Response({'message': 'Item removed from cart'})


# ৬. সব অর্ডার দেখার জন্য
@api_view(['GET'])
def get_orders(request):
    orders = Orders.objects.all()
    serializer = OrdersSerializer(orders, many=True)
    return Response(serializer.data)


# ৭. অর্ডার আইটেমগুলো দেখার জন্য
@api_view(['GET'])
def get_order_items(request):
    order_items = OrderItems.objects.all()
    serializer = OrderItemsSerializer(order_items, many=True)
    return Response(serializer.data)


# ৮. পেমেন্ট লিস্ট দেখার জন্য
@api_view(['GET'])
def get_payments(request):
    payments = Payments.objects.all()
    serializer = PaymentsSerializer(payments, many=True)
    return Response(serializer.data)


# ৯. প্রোডাক্টের রিভিউ দেখার জন্য
@api_view(['GET'])
def get_reviews(request):
    reviews = Reviews.objects.all()
    serializer = ReviewsSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_order(request):
    try:
        data = request.data
        raw_phone = str(data.get('phone', '')).strip()
        clean_phone = raw_phone.replace('+', '').replace('-', '').replace(' ', '')

        if not clean_phone.isdigit() or len(clean_phone) < 10:
            return Response({'error': 'Invalid phone number'}, status=status.HTTP_400_BAD_REQUEST)

        # Normalize payment_method so it satisfies PostgreSQL check constraint
        raw_method = data.get('payment_method', 'COD')
        payment_method = 'COD' if raw_method in ['CreditCard', 'Cash on Delivery'] else raw_method

        custom_user = get_custom_user(request.user)
        if not custom_user:
            return Response({'error': 'No user found in database'}, status=status.HTTP_400_BAD_REQUEST)

        cart = Cart.objects.filter(user=custom_user).first() or Cart.objects.first()
        if not cart or not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        total = sum(float(item.product.sale_price or 0) * item.quantity for item in cart.items.all())

        order = Orders.objects.create(
            user=custom_user,
            order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
            order_date=timezone.now(),
            status='pending',
            subtotal=total,
            discount_amount=0,
            shipping_fee=0,
            total_amount=total,
            payment_method=payment_method,
            payment_status='pending',
            guest_email=data.get('email', custom_user.email),
            guest_phone=raw_phone,
            customer_notes=data.get('address', ''),
            created_by=custom_user.id,
            updated_by=custom_user.id
        )

        for item in cart.items.all():
            price = float(item.product.sale_price or 0)
            OrderItems.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.title,
                quantity=item.quantity,
                unit_price=price,
                total_price=price * item.quantity,
                discount_amount=0,
                created_by=custom_user.id,
                updated_by=custom_user.id
            )

        cart.items.all().delete()

        return Response({
            'message': 'Order created successfully',
            'order_id': order.id,
            'order_number': order.order_number
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {"message": "User Created Successfully", "user": UserSerializer(user).data},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)