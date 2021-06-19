from django.db import models


class Branch(models.Model):
    name = models.CharField(max_length=100, default="Namaste Ongole")
    area = models.CharField(max_length=100, default="Kothapatnam (m) pallepalem (v)")
    city = models.CharField(max_length=20, default="Ongole")
    state = models.CharField(max_length=100, default="Andhra Pradesh")
    country = models.CharField(max_length=100, default="India")
    pincode = models.CharField(max_length=100)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    close_time = models.TimeField(auto_now=False, auto_now_add=False)
    gst = models.IntegerField(default=5)
    delivery_charges = models.IntegerField(default=25)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    alternate_phone_number =models.CharField(max_length=20, blank=True, null=True)
    

    def __str__(self):
        return self.name
    
    @property
    def json(self):
        return {
            "name": self.name,
            "area": self.area,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "pincode": self.pincode,
            "start_time": self.start_time,
            "close_time": self.close_time,
            "gst": self.gst,
            "delivery_charges": self.delivery_charges,
            "phone_number": self.phone_number,
            "alternate_phone_number": self.alternate_phone_number,
        }