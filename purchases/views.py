from typing import Optional

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.db.models import QuerySet
from django.http import HttpResponse, HttpRequest
from django.views.generic import CreateView, UpdateView

from cart.forms import CartAddProductForm
from .forms import CategoryForm, CreateCategoryForm, CreateProductForm, CommentsForm
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

    return render(
        request,
        "home.html",
        {
            "products": product_list,
            "categories": categories,
            "form": form,
            "category": category,
            "ratings": ratings,
        },
    )


def current_product(request: HttpRequest, slug) -> HttpResponse:
    product: Product = Product.available_products.get(slug=slug)
    cart_form = CartAddProductForm()
    comments: Comments = Comments.objects.filter(product=product)
    product_rate = Comments.get_product_rating(product)

    if request.user.is_authenticated:
        user_comment = Comments.objects.filter(product=product, client=request.user)
    else:
        user_comment = None

    if request.method == "POST":
        if user_comment:
            comments_form = CommentsForm(
                request.POST, instance=user_comment[0] if user_comment else None
            )
            if comments_form.is_valid() and comments_form.has_changed():
                comment: Comments = comments_form.save(commit=False)
                comment.client = request.user
                comment.product = product
                comment.save()
                Rating.objects.filter(product=product).update(
                    product_rating=Comments.get_product_rating(product)
                )
        return redirect("product", slug=slug)
    else:
        if user_comment:
            comments_form = CommentsForm(instance=user_comment[0])
        else:
            comments_form = CommentsForm()

    return render(
        request,
        "current_product.html",
        {
            "product": product,
            "cart_form": cart_form,
            "comments_form": comments_form,
            "comments": comments,
            "product_rate": product_rate,
        },
    )


class CreateProduct(CreateView):
    model = Product
    form_class = CreateProductForm
    template_name = "create_product.html"

    def get(self, request, *args, **kwargs):
        if request.user.has_perms(Product.get_permissions()):
            return super(CreateProduct, self).get(request, *args, **kwargs)
        else:
            return redirect("home")


class CreateCategory(CreateView):
    model = Category
    form_class = CreateCategoryForm
    template_name = "create_category.html"
    
    def get(self, request, *args, **kwargs):
        if request.user.has_perms(Category.get_permissions()):
            return super(CreateCategory, self).get(request, *args, **kwargs)
        else:
            return redirect("home")


class EditProduct(UpdateView):
    model = Product
    form_class = CreateProductForm
    template_name = "create_product.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        if request.user.has_perms(Product.get_permissions()):
            return super(EditProduct, self).get(request, *args, **kwargs)
        else:
            return redirect("home")
