from django.db import models
from django.conf import settings
from django.urls import reverse
from acc.models import *
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


#Item model, for storing different items to be sold
class ContractService(models.Model):
    skill = models.ForeignKey(
        UserSkill, on_delete=models.CASCADE, default=None)
    tag = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    startTime = models.DateTimeField(auto_now_add=False)
    endTime = models.DateTimeField(auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    contractor = models.ForeignKey(User, on_delete=models.CASCADE, default=None,related_name="contractor")


    def __str__(self):
        return f'{self.contractor} ordered {self.skill}'


    def get_absolute_url(self):
        return reverse("core:product", kwargs={'slug': self.slug})


    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={'slug': self.slug})


    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={'slug': self.slug})


#Order Item, checks on a particular item if ordered
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(ContractService, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


    def __str__(self):
        return f"{self.quantity} of {self.item}"


    def get_total_item_price(self):
        return self.quantity * self.item.price


    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price


    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()


    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


#Order Model, Details on the Order made
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    # shipping_address = models.ForeignKey('Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    # billing_address = models.ForeignKey('Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    mobile_service = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user}"


    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


#Address Model
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    # address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)


    def __str__(self):
        return self.street_address


    class Meta:
        verbose_name_plural = 'Addresses'


#Payment Model Using stripe
class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user}"


#Coupon Model
class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()
    def __str__(self):
        return self.code


#Refund Model
class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()


    def __str__(self):
        return f"{self.pk}"


#UserProfile receiver
# def userprofile_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         userprofile = UserProfile.objects.create(user=instance)


# post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)



