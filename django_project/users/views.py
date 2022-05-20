from multiprocessing import context
from django.shortcuts import render,redirect
from users.forms import NewUserForm
from django.contrib.auth.decorators import login_required
from users.models import Profile
from django.contrib.auth.models import User
from productapp import cart
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('productapp:home')
                    
    form = NewUserForm()
    context = {
        'form':form,
    }
    return render(request,'users/register.html',context)

@login_required
def profile(request):
    cart_item_count = cart.item_count(request)
    return render(request,'users/profile.html',{'cart_item_count':cart_item_count})

def update_profile(request):
    cart_item_count = cart.item_count(request)
    if request.method == 'POST':
        user = request.user
        profile = Profile.objects.get(user=user)
        if request.FILES.get('upload'):
            profile.image = request.FILES['upload']
        else:
            profile.image = None
        profile.fname = request.POST.get('fname')
        profile.lname = request.POST.get('lname')
        profile.contact_number = request.POST.get('contact_number')
        profile.email = request.POST.get('email')
        profile.address = request.POST.get('address')
        profile.save()
        return redirect('users:profile')
    return render(request,'users/updateprofile.html',{'cart_item_count':cart_item_count})

@login_required
def seller_profile(request,id):
    seller = User.objects.get(id=id)
    context = {
        'seller':seller,
    }
    return render(request,'users/sellerprofile.html',context)