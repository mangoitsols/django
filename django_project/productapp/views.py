from difflib import context_diff
from django.shortcuts import render, redirect,get_object_or_404
from productapp.models import Product,Contact
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView,TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.urls import reverse,reverse_lazy
from django.conf import settings
from productapp.models import Product, Order, LineItem
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from .forms import CartForm, CheckoutForm
from . import cart
import random

def index(request):
    cart_item_count = cart.item_count(request)
    return render(request,'productapp/home.html',{'cart_item_count':cart_item_count})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        return redirect('productapp:products')
    return render(request,'productapp/contact.html')

def about(request):
    cart_item_count = cart.item_count(request)
    return render(request,'productapp/about.html',{'cart_item_count':cart_item_count})

def privacy(request):
    cart_item_count = cart.item_count(request)
    return render(request,'productapp/privacy.html',{'cart_item_count':cart_item_count})

def products(request):
    page_obj = products = Product.objects.all()
    cart_item_count = cart.item_count(request)
    
    product_name = request.GET.get('product_name')
    if product_name != '' and product_name is not None:
        page_obj = products.filter(name__icontains = product_name)
    
    paginator = Paginator(page_obj,4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj' : page_obj,
        'cart_item_count' : cart_item_count
    }
    return render(request,'productapp/index.html',context)

def product_detail(request,id):
    cart_item_count = cart.item_count(request)
    try:
        product = Product.objects.get(id=id)
        
        if request.method == 'POST':
            form = CartForm(request, request.POST)
            if form.is_valid():
                request.form_data = form.cleaned_data
                check = cart.add_item_to_cart(request)
                return redirect('productapp:show_cart')

        form = CartForm(request, initial={'product_id': product.id})
        context = {
            'product' : product,
            'form': form,
            'cart_item_count' : cart_item_count
        }
    except Product.DoesNotExist:
        return render(request,'productapp/product_not_exist.html',context)
    return render(request,'productapp/detail.html',context)

class ProductCreateView(CreateView):
    model = Product
    fields = ['name','price','desc','image','seller_name']

class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name','price','desc','image']
    template_name_suffix = '_update_form'

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('productapp:products')

@login_required
def my_listing(request):
    products = Product.objects.filter(seller_name=request.user)
    context = {
        'products':products,
        }
    return render(request,'productapp/mylisting.html',context)

def show_cart(request):
    if request.method == 'POST':
        if request.POST.get('submit') == 'Update':
            cart.update_item(request)
        if request.POST.get('submit') == 'Remove':
            cart.remove_item(request)

    cart_items = cart.get_all_cart_items(request)
    cart_item_count = cart.item_count(request)
    cart_subtotal = cart.subtotal(request)
    context = {
        'cart_items': cart_items,
        'cart_subtotal': cart_subtotal,
        'cart_item_count': cart_item_count,
        }
    return render(request, 'productapp/cart.html',context)

@login_required
def checkout(request):
    cart_subtotal = cart.subtotal(request)
    if cart_subtotal > 0:
        cart_items = cart.get_all_cart_items(request)
        if request.method == 'POST':
            form = CheckoutForm(request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                ordrdtls = Order(
                    name = cleaned_data.get('name'),
                    email = cleaned_data.get('email'),
                    postal_code = cleaned_data.get('postal_code'),
                    address = cleaned_data.get('address'),
                )
                ordrdtls.save()

                all_items = cart.get_all_cart_items(request)
                for cart_item in all_items:
                    li = LineItem(
                        product_id = cart_item.product_id,
                        price = cart_item.price,
                        quantity = cart_item.quantity,
                        order_id = ordrdtls.id
                    )
                    li.save()

                cart.clear(request)

                request.session['order_id'] = ordrdtls.id
                return redirect('productapp:process_payment')
        else:
            form = CheckoutForm()
            context = {
                'form': form,
                'cart_subtotal': cart_subtotal,
                'cart_items': cart_items,
                }
            return render(request, 'productapp/checkout.html', context)
    else:
        return redirect('productapp:show_cart')

@login_required
def process_payment(request):
    order_id = request.session.get('order_id')
    order = Order.objects.get(id=order_id)
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % order.total_cost().quantize(Decimal('.01')),
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id)+str(random.randint(100,999)),
        'currency_code': 'USD',
        'notify_url': 'http://192.168.168.31:8000/paypal/',
        'return_url': 'http://{}{}'.format(host,reverse('productapp:payment_success')),
        'cancel_return': 'http://{}{}'.format(host,reverse('productapp:payment_failed')),
        }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'productapp/process_payment.html', {'order': order, 'form': form})

