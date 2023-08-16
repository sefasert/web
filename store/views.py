import json

from django.shortcuts import render, get_object_or_404, redirect

from .models import Product, Related_Product

from category.models import Category

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from django.db.models import Q

from django.http import JsonResponse , HttpResponsePermanentRedirect
from django.urls import reverse

from .filters import ProductFilter

# Create your views here.

def home(request):
    products = Product.objects.filter(is_available=True).order_by("-id")

    paginator = Paginator(products, 12)
    page = request.GET.get("page")
    paged_products = paginator.get_page(page)

    context = {
        "products": paged_products,
    }

    if request.htmx:
        return render(request, 'list.html', context)
    return render(request, "index.html", context)


def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug:
        categories     = get_object_or_404(Category, slug=category_slug)
        products       = Product.objects.filter(category=categories, is_available=True).order_by("-id")

    myFilter       = ProductFilter(request.GET, queryset=products)
    products       = myFilter.qs
    paginator      = Paginator(products, 30)
    page           = request.GET.get("page")
    paged_products = paginator.get_page(page)
    product_count  = products.count()

    context = {
        "categories"    : categories,
        "products"      : paged_products,
        "product_count" : product_count,
        "myFilter"      : myFilter,
    }
    return render(request, "store/store.html", context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        products = Product.objects.filter(category=single_product.category, is_available=True)
        categories     = get_object_or_404(Category, slug=category_slug)


    except Product.DoesNotExist: #Eğer ürün bulunamazsa,
    #üründen önceki kategoriye git 301 yönlendirmesi
        categories = get_object_or_404(Category, slug=category_slug)
        messages.success(request, "Bilgi: ürün sayfası bulunamadı, kategori sayfasına yönlendirildiniz!")
        return HttpResponsePermanentRedirect(categories.get_url())


    related_product = Related_Product.objects.filter(product_id=single_product.id)

    context = {
        "single_product" : single_product,
        "categories"     : categories,
        "related_product": related_product,
        "products": products, #benzer ürün
    }
    return render(request, "store/product_detail.html", context)


def search(request):
    products = Product.objects.filter(is_available=True).order_by("-created_date")

    if "keyword" in request.GET:
        keyword = request.GET["keyword"]
        if keyword:
            products       = Product.objects.filter(is_available=True).order_by("-created_date").filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            #filter
            myFilter       = ProductFilter(request.GET, queryset=products)
            products       = myFilter.qs
            product_count  = products.count()
        else:
            return redirect("store")

    search_query = keyword  # Arama sorgusu değişkeni

    context = {
        "products"      : products,
        "product_count" : product_count,
        "myFilter"      : myFilter,
        "search_query"  : search_query,
    }
    return render(request, "store/store.html", context)


def otoyazi(request):
    query_original = request.GET.get("term")
    queryset = Product.objects.filter(product_name__icontains=query_original, is_available=True)[:21]

    results = []
    for product in queryset:
        category_slug = product.category.slug
        product_slug = product.slug
        label = product.product_name
        value = product.product_name
        url = reverse('product_detail', args=[category_slug, product_slug])

        result = {
            'category_slug': category_slug,
            'product_slug': product_slug,
            'label': label,
            'value': value,
            'url': url
        }
        results.append(result)

    return JsonResponse(results, safe=False)


def filter_results(request):
    products = Product.objects.filter(is_available=True).order_by("-id")
    # myfilter
    myFilter = ProductFilter(request.GET, queryset=products)
    products = myFilter.qs

    # Fiyat aralığı filtresi
    price_range = request.GET.get('price_range')
    if price_range:
        if price_range == '100-300':
            products = products.filter(price__gte=100, price__lte=300).order_by('price')
        elif price_range == '300-500':
            products = products.filter(price__gte=300, price__lte=500).order_by('price')
        elif price_range == '500-1000':
            products = products.filter(price__gte=500, price__lte=1000).order_by('price')
        elif price_range == '1000-2000':
            products = products.filter(price__gte=1000, price__lte=2000).order_by('price')

    #fiyatı küçükten büyüğe doğru sıralama
    products = products.order_by('price')

    context = {
        'products': products,
        'myFilter': myFilter,
    }
    return render(request, 'store/store.html', context)
