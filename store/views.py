from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import category
# Create your views here.
def store(request, category_slug=None):   #view function to display all products on store page and filter products based on category slug

    categories = None
    products = None
    if category_slug != None:   #if category_slug is not None then filter products based on category slug
        categories = get_object_or_404(category, slug=category_slug)  #fetching the category object based on the slug from the url
        products = Product.objects.filter(category=categories,is_available=True)  #filtering products based on the category object and is_available=True
        product_count = products.count()
    else:    #if category_slug is None then display all products
        products = Product.objects.all().filter(is_available=True) #fetching all products from Product model where is_available=True all() returns a queryset and filter() filters the data based on the condition
        product_count = products.count()


    
    context ={
        'products':products,
        'product_count':product_count,
    }       #context dictionary to pass data from views to templates i.e, html file

    return render(request,'store/store.html', context)      

def product_detail(request, category_slug, product_name):   #view function to display product details based on category slug and product name
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_name)  #fetching the product object based on category slug and product name, 
        #here category is the foreign key in Product model and we are using double underscore to access the slug field of category model
    except Exception as e:
        raise e
    context = {
        'single_product':single_product,
    }
    return render(request,'store/product_detail.html',context)

