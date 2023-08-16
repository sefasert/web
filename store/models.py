from PIL import Image

from django.db import models

from category.models import Category

from django.urls import reverse

from ckeditor.fields import RichTextField

# Create your models here.

class Product(models.Model):

    BRAND_CHOICE = {
        (".", ""),
        ("VESTEL", "Vestel"),
        ("PHILIPS", "Philips"),
        ("Dreamstar", "dreamstar"),
        ("SAMSUNG", "Samsung"),
        ("SANYO-NORDMENDE", "Sanyo-Nordmende"),
        ("SUNNY", "Sunny"),
        ("AWOX", "Awox"),
        ("DIJITSU", "Dijitsu"),
        ("LG", "LG"),
        ("Profilo", "Profilo"),
        ("Arçelik-Beko-Grundig", "Arçelik-Beko-Grundig"),
        ("ROWELL", "Rowell"),
        ("ONVO-SABA", "Onvo-Saba"),
        ("Next", "Next"),
        ("Skytech", "Skytech"),
        ("SONY", "Sony"),
        ("YUMATU", "Yumatu"),
        ("Premier", "Premier"),
        ("SUNNY-AXEN-WOON-SHEEN" , "Sunny-Axen-Woon-Sheen"),
        ("Navitech", "Navitech"),
        ("Panasonic", "Panasonic"),
        ("Lifemaxx", "lifemaxx"),
        ("Hisense", "Hisense"),
        ("Hi-Level", "Hi-Level"),
        ("TELENOVA-RONAX", "Telenova-Ronax"),
        ("BOE", "BOE"),
        ("WOON", "Woon"),
        ("SHARP", "Sharp"),
        ("AUO", "Auo"),
        ("DARFON", "Darfon"),
        ("CHIMEI-INNOLUX", "Chimei-Innolux"),
        ("TOSHIBA", "Toshiba"),
        ("AFTRON", "Aftron"),
        ("NEMU", "Nemu"),
        ("PANDA", "Panda"),
        ("FISHER", "Fisher"),
        ("Haier", "Haier"),
        ("WDX", "WDX"),
        ("Acer", "Acer"),
        ("Casper", "Casper"),
        ("Exper", "Exper"),
        ("REDLINE", "REDLINE"),

    }

    DURUM_CHOICE = {
    #    ("Sıfır", "0"),
        ("2.EL", "2"),
    }

    YENI_CHOICE = {
        ("Yeni", "yeni"),
    }

    EKRAN_CHOICE = {
        ("LED", "led"),
        ("LCD", "lcd"),
        ("Plazma", "plazma"),
        ("LED-LCD", "led-lcd")
    }

    category      = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE)
    product_name  = models.CharField(max_length=200, blank=False)
    slug          = models.SlugField(max_length=200, unique=True, blank=False)
    brand         = models.CharField(max_length=100, choices=BRAND_CHOICE, blank=True)
    durum         = models.CharField(max_length=50, choices=DURUM_CHOICE, blank=True)
    yeni          = models.CharField(max_length=10, choices=YENI_CHOICE, blank=True)
    price         = models.IntegerField(blank=True)
    images        = models.ImageField(upload_to= "photos/products", blank=True, null=True)
    webp          = models.ImageField(upload_to= "webp/products", blank=True, null=True)
    images2       = models.ImageField(upload_to= "photos2/products", blank=True, null=True)
    webp2         = models.ImageField(upload_to= "webp2/products", blank=True, null=True)
    images3       = models.ImageField(upload_to= "photos3/products", blank=True, null=True)
    webp3         = models.ImageField(upload_to= "webp3/products", blank=True, null=True)
    images4       = models.ImageField(upload_to= "photos4/products", blank=True, null=True)
    webp4         = models.ImageField(upload_to= "webp4/products", blank=True, null=True)
    images5       = models.ImageField(upload_to= "photos5/products", blank=True, null=True)
    webp5         = models.ImageField(upload_to= "webp5/products", blank=True, null=True)
    images6       = models.ImageField(upload_to= "photos6/products", blank=True, null=True)
    webp6         = models.ImageField(upload_to= "webp6/products", blank=True, null=True)
    stock         = models.IntegerField(blank=False)
    ekran         = models.CharField(max_length=10, choices=EKRAN_CHOICE, blank=True, verbose_name="Ekran Türü")
    tags          = models.CharField(max_length=1000, blank=True)
    description   = RichTextField(blank=True)
    is_available  = models.BooleanField(default=True)
    created_date  = models.DateField(auto_now_add=True)
    sontarih      = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self): #kategori slug ve ürünün kendi slug'ı al
        return reverse("product_detail", args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

    def resize_image(self, image_field, max_size=1600):
        if image_field:
            img = Image.open(image_field.path)
            if img.height > max_size or img.width > max_size:
                output_size = (max_size, max_size)
                img.thumbnail(output_size)
                img.save(image_field.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.resize_image(self.images)
        self.resize_image(self.webp)

class Related_Product(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    benzerresimlink = models.CharField(max_length=200, blank=True)
    benzerad  = models.CharField(max_length=200)
    benzerlink = models.CharField(max_length=200)
    benzerfiyat = models.IntegerField()

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name_plural = "related product"
