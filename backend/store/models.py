import uuid
from django.db import models


class Cart(models.Model):
    user = models.ForeignKey('Users', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} for {self.user}"

    @property
    def total(self):
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

    @property
    def total_price(self):
        price = self.product.sale_price or 0
        return self.quantity * price


class Categories(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.CharField(unique=True, max_length=100)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', models.CASCADE, blank=True, null=True)
    image_url = models.ImageField(upload_to='categories/', blank=True, null=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'categories'


class OrderItems(models.Model):
    id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey('Orders', models.CASCADE)
    product = models.ForeignKey('Products', models.CASCADE)
    product_name = models.CharField(max_length=200, blank=True, null=True)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    created_by = models.BigIntegerField(blank=True, null=True)
    updated_by = models.BigIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'order_items'


class Orders(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('Users', models.CASCADE, null=True, blank=True)
    order_number = models.CharField(unique=True, max_length=50)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=30, default='COD')
    payment_status = models.CharField(max_length=20, default='pending')
    guest_email = models.CharField(max_length=100, blank=True, null=True)
    guest_phone = models.CharField(max_length=20, blank=True, null=True)
    customer_notes = models.TextField(blank=True, null=True)
    created_by = models.BigIntegerField(blank=True, null=True)
    updated_by = models.BigIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_number

    class Meta:
        managed = False
        db_table = 'orders'


class Payments(models.Model):
    id = models.BigAutoField(primary_key=True)
    order = models.OneToOneField(Orders, models.CASCADE)
    user = models.ForeignKey('Users', models.CASCADE)
    transaction_id = models.CharField(unique=True, max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    payment_method = models.CharField(max_length=30)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'payments'


class Products(models.Model):
    id = models.BigAutoField(primary_key=True)
    seller = models.ForeignKey('Users', models.CASCADE)
    category = models.ForeignKey(Categories, models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=200)
    slug = models.CharField(unique=True, max_length=200)
    description = models.TextField(blank=True, null=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sku = models.CharField(unique=True, max_length=50, blank=True)
    stock_quantity = models.IntegerField(default=1)
    image_url = models.ImageField(upload_to='products/', blank=True, null=True)
    variants = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def price(self):
        return self.sale_price

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = f"SKU-{uuid.uuid4().hex[:8].upper()}"
        if self.variants is None:
            self.variants = []
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'products'


class Reviews(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Products, models.CASCADE)
    user = models.ForeignKey('Users', models.CASCADE)
    order = models.ForeignKey(Orders, models.DO_NOTHING, blank=True, null=True)
    rating = models.IntegerField()
    title = models.CharField(max_length=200, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    videos = models.JSONField(default=list, blank=True)
    verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'reviews'


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=254)
    phone = models.CharField(unique=True, max_length=20, blank=True, null=True)
    password_hash = models.CharField(max_length=255)
    role = models.CharField(max_length=20, default='buyer')
    country = models.CharField(max_length=50, default='Bangladesh')
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    language = models.CharField(max_length=10, default='en')
    currency = models.CharField(max_length=3, default='BDT')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    class Meta:
        managed = False
        db_table = 'users'