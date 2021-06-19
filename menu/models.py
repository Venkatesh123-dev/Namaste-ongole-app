from django.db import models
from django.shortcuts import reverse


class Category(models.Model):
    category = models.CharField(max_length=100)
    # description = models.TextField()
    image = models.ImageField(upload_to='menu/categories/images')
    slug = models.SlugField()
    is_enabled = models.BooleanField(default=False)
    # icon = models.ImageField(blank=True, null=True, upload_to='menu/categories/icons')

    def __str__(self):
        return self.category

    def get_absolute_url(self):
        return reverse("core:category", kwargs={
            'slug': self.slug
        })

    def products_count(self,):
        return self.product_set.count()

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    product = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50, blank=True, null=True)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField()
    image = models.ImageField(upload_to='menu/products/images')
    is_enabled = models.BooleanField(default=False)
    # description = models.TextField()

    def __str__(self):
        return self.product
    
    @property
    def current_price(self):
        if self.discount_price:
            return self.discount_price
        return self.price

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })





class Offer(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='menu/offers/images')
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    close_time = models.TimeField(auto_now=False, auto_now_add=False)
    expiry_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    is_enabled = models.BooleanField(default=False)
    is_daily_offer = models.BooleanField(default=False)
    for_all_products = models.BooleanField(default=False)
    products = models.ManyToManyField(Product, related_name="products", blank=True, null=True)
    exclude_products = models.ManyToManyField(Product, related_name="exclude_products", blank=True, null=True)
    applicable_quantity = models.IntegerField()
    # icon = models.ImageField(blank=True, null=True, upload_to='menu/categories/icons')

    def __str__(self):
        return self.title



    class Meta:
        verbose_name_plural = "Offers"
