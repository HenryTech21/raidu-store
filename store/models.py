from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):

    name = models.CharField(max_length=200)
    size = models.CharField(max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(max_length=2000, blank=True)
    out_of_stock = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(blank=True,null=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    

class Album(models.Model):
    name = models.CharField(blank=True,max_length=20)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(blank=True,null=True)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Order(models.Model):

    STATUS = (('Pending', 'Pending'),
              ('Out for delivery', 'Out for delivery'),
              ('Delivered', 'Delivered'),
              ('Cancelled', 'Cancelled'),)

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    complete = models.BooleanField(default=False)
    note = models.CharField(max_length=1000, null=True, blank=True)


    def __str__(self):
        return str(self.transaction_id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_order_item(self):
        return self.orderitem_set.all()

    @property
    def shipping_address(self):
        return self.shippingaddress_set.all()


class OrderItem(models.Model):

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(max_length=None, default='')

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

class BlogPost(models.Model):

    title = models.CharField(max_length=200, null=False)
    author = models.CharField(max_length=200, null=False, default="")
    text = models.TextField(null=False)
    image = models.ImageField(blank=True,null=True)
    publish = models.BooleanField(default=False, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

        


