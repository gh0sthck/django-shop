from typing import Optional

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.db.models import QuerySet
from django.http import HttpResponse, HttpRequest

from cart.forms import CartAddProductForm
from .forms import CategoryForm, CreateProductForm, CommentsForm
from .models import Product, Category, Comments, Rating


def home(request: HttpRequest, category_slug=None) -> HttpResponse:
    categories: Optional[QuerySet[Category]] = Category.objects.all()
    category = None
    product_list: QuerySet[Product] = Product.available_products.all()
    ratings = Rating.objects.all()
    form = CategoryForm()

    if category_slug or "select_category" in request.GET:
        if "select_category" in request.GET:
            category = Category.objects.get(name=request.GET["select_category"])
        elif category_slug:
            category = Category.objects.get(slug=category_slug)
        product_list = Product.available_products.filter(category=category)
        categories = None

    paginator = Paginator(product_list, 4)
    page_number = request.GET.get("page", 1)

    try:
        product_list = paginator.page(page_number)
    except PageNotAnInteger:
        product_list = paginator.page(1)
    except EmptyPage:
        product_list = paginator.page(paginator.num_pages)

    return render(request, "home.html", {"products": product_list, "categories": categories,
                                         "form": form, "category": category, "ratings": ratings})


def current_product(request: HttpRequest, slug) -> HttpResponse:
    product: Product = Product.available_products.get(slug=slug)
    cart_form = CartAddProductForm()
    comments: Comments = Comments.objects.filter(product=product)
    product_rate = Comments.get_product_rating(product)
    user_comment = Comments.objects.filter(product=product, client=request.user.shopclient)

    if request.method == "POST":
        comments_form = CommentsForm(request.POST, instance=user_comment[0] if user_comment else None)
        if comments_form.is_valid() and comments_form.has_changed():
            comment: Comments = comments_form.save(commit=False)
            comment.client = request.user.shopclient
            comment.product = product
            comment.save()
            Rating.objects.filter(product=product).update(product_rating=Comments.get_product_rating(product))
            return redirect("product", slug=slug)
    else:
        if user_comment:
            comments_form = CommentsForm(instance=user_comment[0])
        else:
            comments_form = CommentsForm

    return render(request, "current_product.html", {"product": product, "cart_form": cart_form,
                                                    "comments_form": comments_form, "comments": comments,
                                                    "product_rate": product_rate})


@login_required
def create_product(request: HttpRequest) -> HttpResponse:
    if request.user.has_perms(["purchases.change_product", "purchases.add_product",
                               "purchases.delete_product"]):
        if request.method == "POST":
            form = CreateProductForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save()
                Rating.objects.create(product=product, product_rating=0.0)
                return redirect("home")
        else:
            form = CreateProductForm()

        return render(request, "create_product.html", {"form": form})
    else:
        return HttpResponse("You haven't permissions to that operation")


@login_required
def edit_product(request: HttpRequest, slug) -> HttpResponse:
    if request.user.has_perms(["purchases.change_product", "purchases.add_product",
                               "purchases.delete_product"]):
        product: Product = Product.objects.get(slug=slug)
        if request.method == "POST":
            form = CreateProductForm(request.POST, request.FILES, instance=product)
            if form.has_changed():
                form.save()
                return redirect("home")
        else:
            form = CreateProductForm(instance=product)

        return render(request, "create_product.html", {"form": form})
    else:
        return HttpResponse("You haven't permissions to that operation")
