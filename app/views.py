from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import *
from .forms import CostumerRegistraionForm, CostumerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ProducView(View):
    def get(self, request):
        totalitem = 0
        kids_wear = Product.objects.filter(category='kids wear')
        foot_wear = Product.objects.filter(category='shoes')
        other_products = Product.objects.filter(id__range=(9, 19))
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html', {'kidswear':kids_wear, 'footwear':foot_wear, 'otherproduct':other_products, 'totalitem':totalitem})


class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart, 'totalitem':totalitem})


def search_product(request):
    if request.method == "POST":
        formdata = request.POST.get('formdata')
        if formdata is not None:
            lookups = Product.objects.filter(Q(title__icontains = formdata) | Q(category__icontains = formdata) | Q(brand__icontains = formdata) | Q(description__icontains = formdata))
            return render(request, 'app/search.html', {'searchdata':lookups})
        return render(request, 'app/home.html')


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart_item = Cart.objects.filter(user=user)
        cartitem = list(cart_item)
        initial_amount = 0.0
        shipping_charge = 40.0
        total_amount = 0.0
        amount = 0.0
        totalitem = 0
        if cartitem:
            for itm in cartitem:
                initial_amount = itm.quantity * itm.product.discounted_price
                amount += initial_amount
            total_amount = amount + shipping_charge
            totalitem = len(Cart.objects.filter(user=request.user))
            dict = {'cartitems':cart_item, 'shippingcharge':shipping_charge, 'amount':amount, 'total_amount':total_amount, 'totalitem':totalitem}
            return render(request, 'app/addtocart.html', dict)
        totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/emptycart.html', {'totalitem':totalitem})


def plus_cart(request):
    if request.method == "GET":
        user = request.user
        prod_id =request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity +=1
        c.save()
        shipping_charge = 40.0
        amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==user]
        for p in cart_product:
            initial_amount = (p.quantity * p.product.discounted_price)
            amount += initial_amount
        total_amount = amount + shipping_charge
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':total_amount
        }
    return JsonResponse(data)


def minus_cart(request):
    if request.method == "GET":
        user = request.user
        prod_id =request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -=1
        c.save()
        shipping_charge = 40.0
        amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==user]
        for p in cart_product:
            initial_amount = (p.quantity * p.product.discounted_price)
            amount += initial_amount
        total_amount = amount + shipping_charge
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':total_amount
        }
    return JsonResponse(data)


def remove_item(request):
    if request.method == "GET":
        user = request.user
        prod_id =request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        shipping_charge = 40.0
        amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==user]
        for p in cart_product:
            initial_amount = (p.quantity * p.product.discounted_price)
            amount += initial_amount
        total_amount = amount + shipping_charge
        data = {
            'amount':amount,
            'totalamount':total_amount
        }
    return JsonResponse(data)



def buy_now(request):
 return render(request, 'app/buynow.html')


@login_required
def address(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    address = Costumer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add':address, 'active':'btn-primary', 'totalitem':totalitem})


@login_required
def orders(request):
    op = PlacedOrder.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'orderplaced':op})


def mobile(request, data=None):
    if data == None:
        mobile = Product.objects.filter(category='smartphone')
    elif data == "apple" or "oppo" or "xiaomi" or "oneplus":
        mobile = Product.objects.filter(category='smartphone').filter(brand=data)
    elif data == "below":
        mobile = Product.objects.filter(category='smartphone').filter(discounted_price__lt=20000)
    elif data == "above":
        mobile = Product.objects.filter(category='smartphone').filter(discounted_price__gt=20000)
    return render(request, 'app/mobile.html', {'mobile':mobile})


def FootWear(request, data=None):
    if data == None:
        shoes = Product.objects.filter(category='shoes')
    elif data == "puma" or data == "addidas" or data =="nykaa":
        shoes = Product.objects.filter(category='shoes').filter(brand=data)
    elif data == "below":
        shoes = Product.objects.filter(category='shoes').filter(discounted_price__lt=2000)
    elif data == "above":
        shoes = Product.objects.filter(category='shoes').filter(discounted_price__gt=2000)
    return render(request, 'app/footwear.html', {'shoes':shoes})


class CostumeRegistrationFormView(View):
    def get(self, request):
        form = CostumerRegistraionForm()
        return render(request, 'app/customerregistration.html', {'form':form})
    def post(self, request):
        form = CostumerRegistraionForm(request.POST)
        if form.is_valid():
            messages.success(request, "Congratulations!!! Registered Successfully")
            form.save()
        return render(request, 'app/customerregistration.html', {'form':form})


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        form = CostumerProfileForm
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})

    def post(self, request):
        form = CostumerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zip = form.cleaned_data['zip']
            reg = Costumer(user=usr, name=name, locality=locality, city=city, state=state, zip=zip)
            reg.save()
            messages.success(request, 'Congratulations!, Profile Updated Successfully !!!')
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})


@login_required
def checkout(request):
    user = request.user
    add = Costumer.objects.filter(user=user)
    cart_prod = Cart.objects.filter(user=user)
    shipping_charge = 40.0
    amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user==user]
    if cart_product:
        for p in cart_product:
            initial_amount = (p.quantity * p.product.discounted_price)
            amount += initial_amount
    total_amount = amount + shipping_charge
    allvalue = {'add':add, 'cartproduct':cart_prod, 'initialamount':initial_amount, 'shippingcharge':shipping_charge, 'totalamount':total_amount}
    return render(request, 'app/checkout.html', allvalue)


@login_required
def payment_done(request):
    user = request.user
    costumerid = request.GET.get('custid')
    costumer = Costumer.objects.get(id=costumerid)
    cart = Cart.objects.filter(user=user)
    for item in cart:
        PlacedOrder(user=user, costumer=costumer, product= item.product, quantity= item.quantity).save()
        item.delete()
    return redirect("orders")