from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Product, Category, OrderItem, Order, Checkout, Company, ProductReview
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegisterForm, CheckoutForm
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from payment.models import Payment
from django.db.models import Q

# Create your views here.


def home_page(request):

    categories = Category.objects.all()

    if categories:

        for cat in categories:
            cat_products = Product.objects.filter(category=cat)[:4]
            categories.products = cat_products

    companies = Company.objects.all()

    return render(request, 'index.html', {'categories': categories,
                                          'companies': companies})

def shop(request, page):
    search_field = request.GET.get('search')

    if search_field:
        products = Product.objects.filter(Q(name__icontains=search_field))
        
    else:
        products = Product.objects.all()

    companies = Company.objects.all()
    categories = Category.objects.all()
    pag_products = Paginator(products, per_page=9)
    products = pag_products.get_page(page)

    return render(request, 'shop.html', {'products': products,
                                         'categories': categories,
                                         'companies': companies,
                                         'search': search_field})

def shop_cat(request, name, page):
    categories = Category.objects.all()
    category = get_object_or_404(Category, name=name)
    products = Product.objects.filter(category=category)
    pag_products = Paginator(products, per_page=9)
    products = pag_products.get_page(page)

    return render(request, 'shop_cat.html', {'products': products,
                                             'category': category,
                                             'categories': categories})

def company_shop(request, id, page):
    company = get_object_or_404(Company, id=id)
    user = company.user
    products = Product.objects.filter(user=user)
    pag_products = Paginator(products, per_page=9)
    products = pag_products.get_page(page)
    categories = Category.objects.all()

    return render(request, 'company_shop.html', {'products': products,
                                                 'categories': categories,
                                                 'company': company
                                                 })

def product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        comment = request.POST["comment"]
        new_review = ProductReview.objects.create(
            user = request.user,
            comment=comment,
            product=product
        )
        new_review.save()
        messages.success(request, "your review has been added")

    categories = Category.objects.all()
    order_quantity = 0

    category = product.category
    related_products = Product.objects.filter(category=category)[:4]
    reviews = ProductReview.objects.filter(product=product)

    try:
        order_qs = Order.objects.filter(user=request.user, ordered=False)

        if order_qs.exists():
            order = order_qs[0]

            if order.products.filter(product_id=id).exists():
                order = OrderItem.objects.filter(user=request.user, ordered=False, product=product)[0]
                order_quantity = order.quantity
            
            else:
                order_quantity = 0
        
        else:
            order_quantity = 0

    except ObjectDoesNotExist:
        order = False


    return render(request, 'product.html', {'product': product,
                                            'related_products': related_products,
                                            'order_qty': order_quantity,
                                            'categories': categories,
                                            'reviews': reviews
                                            })


def login_view(request):
    categories = Category.objects.all()
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            form = login(request, user)
            messages.success(request, f"Welcome {username}!")
            return redirect('shop:home')
        
        else:
            messages.info(request, "Account does not exist please sign in")

    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form,
                                          'categories': categories})

def register_view(request):
    categories = Category.objects.all()
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration Successful!")
            return redirect("shop:home")
        else:
            messages.info(request, "Please make sure to fill the details in correctly")
    
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form,
                                             'categories': categories})


@login_required
def logout_view(request):

    logout(request)
    return redirect("shop:login_page")
    
@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    order_item, created = OrderItem.objects.get_or_create(
        product = product,
        user = request.user,
        ordered = False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.products.filter(product_id = product.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Added product quantity successfully")
            return redirect("shop:product", id=id)
        
        else:
            order.products.add(order_item)
            messages.info(request, "Product added to cart succesfully")
            return redirect("shop:product", id=id)
        
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user = request.user,
            ordered_date = ordered_date
        )
        order.products.add(order_item)
        messages.info(request, "Product added to cart successfully")
        return redirect("shop:product", id=id)
    
@login_required
def reduce_order_quantity(request, id):
    product = get_object_or_404(Product, id=id)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product_id=id).exists():
            order_item =  OrderItem.objects.filter(user=request.user, ordered=False, product=product)[0]

            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            
            else:
                order_item.delete()

            messages.info(request, "Order item quantity updated!")
            return redirect("shop:cart")
        
        else:
            messages.info(request, "Product is not in your cart")
            return redirect("shop:product", id=id)
    
    else:

        messages.info(request, "You do not have an order")
        return redirect("shop:cart")
        
@login_required
def remove_from_cart(request, id):
    product = get_object_or_404(Product, id=id)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        
        if order.products.filter(product_id=id).exists():
            order_item = OrderItem.objects.filter(
                product = product,
                user = request.user,
                ordered = False
            )[0]
            order_item.delete()
            messages.info(request, "Product removed from cart successfully")
            return redirect("shop:cart")
        
        else:
            messages.info(request, "This Product is not in your cart")
            return redirect("shop: product", id=id)
        
    else:
        messages.info(request, "You do not have an order")
        return redirect("shop: product", id=id)
    
@login_required
def order_summary(request):
    categories = Category.objects.all()

    try:
        order = Order.objects.get(user=request.user, ordered=False)

        return render(request, 'cart.html', {'order': order,
                                             'categories': categories})
    
    except ObjectDoesNotExist:
        messages.info(request, "You do not have an order")
        return redirect('shop:home')

@login_required
def checkout_view(request):
    categories = Category.objects.all()
    try:
        order = Order.objects.get(user=request.user, ordered=False)

        if request.method == "POST":
            form = CheckoutForm(request.POST)

            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                city = form.cleaned_data.get('city')
                zip = form.cleaned_data.get('zip')

                checkout_address, created = Checkout.objects.get_or_create(
                    user=request.user,
                    order=order,
                    
                )

                checkout_address.street_address = street_address
                checkout_address.apartment_address = apartment_address
                checkout_address.country = country
                checkout_address.city = city
                checkout_address.zip = zip

                checkout_address.save()

                payment, created = Payment.objects.get_or_create(
                    order=order,
                    email = request.user.email,
                )

                amount = order.get_total_price()
                payment.amount = amount

                payment.save()

                request.session['payment_id'] = payment.id

                messages.success(request, "Payments Initialized Successfully.")

                return redirect(reverse("payment:process"))

            
            else:
                messages.warning(request, "Please make sure to fill the required information correctly")
                return redirect("shop:checkout")

        else:
            form = CheckoutForm()

        return render(request, 'checkout.html', {'form': form,
                                                 'order': order,
                                                 'categories': categories})
    
    except ObjectDoesNotExist:
        messages.info(request, "You do not have an order")
        return redirect("shop:home")