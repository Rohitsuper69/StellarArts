import pathlib
from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.urls import reverse

PROTECTED_MEDIA_ROOT = settings.PROTECTED_MEDIA_ROOT
protected_storage = FileSystemStorage(str(PROTECTED_MEDIA_ROOT))

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    name = models.CharField(max_length=120)
    desc = models.CharField(max_length=1000, null=True, blank=True)
    handle = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    og_price = models.DecimalField(max_digits=10, decimal_places=2,  default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"handle":self.handle})
    
    def get_manage_url(self):
        return reverse("products:manage", kwargs={"handle":self.handle})
    
def handle_product_attachment_upload(instance, filename):
    return f"products/{instance.product.handle}/attachments/{filename}"
    
class ProductAttachment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, blank=True, null=True)
    file = models.FileField(upload_to=handle_product_attachment_upload, storage=protected_storage)
    isFree = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self,*args,**kwargs):
        if not self.name:
            self.name = pathlib.Path(self.file.name).name
        super().save(*args,**kwargs)

    @property
    def display_name(self):
        return self.name or self.file.name
    
    def get_download_url(self):
        return reverse("products:download", kwargs={"handle":self.product.handle, "pk":self.pk})
    
 