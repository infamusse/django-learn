from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404

from .models import Product
from .forms import ProductModelForm


# Create your views here.
def home_view(request, *args, **kwargs):
    # return HttpResponse("<h1>Hello World</h1>")
    query = request.GET.get('q')
    qs = Product.objects.filter(title__icontains=query[0])
    print(query, qs)
    contex = {'name': 'Mati', "query": query}
    return render(request, 'home.html', contex)


def bad_view(request, *args, **kwargs):
    print(dict(request.GET))
    return HttpResponse('Dont do this')

# OLD VERSION
# def product_create_view(request, *args, **kwargs):
#     if request.method == 'POST':
#         post_data = request.POST or None
#         if post_data != None:
#             my_form = ProductForm(request.POST)
#             if my_form.is_valid():
#                 print(my_form.cleaned_data.get('title'))
#                 title_from_input = Product.objects.create(
#                     title=my_form.cleaned_data.get('title'))
#                 print('post_data', post_data)
#     return render(request, 'forms.html', {})


def product_create_view(request, *args, **kwargs):
    form = ProductModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        # do some staff
        obj.save()

        # print(form.cleaned_data)
        # data = form.cleaned_data
        # Product.objects.create(**data)
        form = ProductModelForm()
    return render(request, 'forms.html', {"form": form})


def product_detail_view(request, id):
    try:
        obj = Product.objects.get(id=id)
    except Product.DoesNotExist:
        raise Http404
    # return HttpResponse(f"<h1>Product id: {obj.id}</h1>")
    return render(request, 'products/detail.html', {'object': obj})


def product_api_detail_view(request, id):
    try:
        obj = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return JsonResponse({'message': 'Not Found'}, status=404)
    return JsonResponse({"id": obj.id})


def product_list_view(request, *args, **kwargs):
    products_all = Product.objects.all()
    return render(request, 'products/list.html', {'object_list': products_all})
