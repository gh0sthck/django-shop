from decimal import Decimal
from django.conf import settings
from django.http import HttpRequest

from purchases.models import Product


class Cart:
    """
    Shop cart manage class.
    :request: HttpRequest - django http request from view.
    """
    def __init__(self, request: HttpRequest):
        self.session = request.session

        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product: Product, count: int = 1, override_count: bool = False):
        """Add product to cart."""
        product_id: str = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"count": 0, "price": str(product.price)}

        if override_count:
            self.cart[product_id]["count"] = count
        else:
            self.cart[product_id]["count"] += count

        self.save()

    def save(self):
        """Saving current session."""
        self.session.modified = True

    def remove(self, product: Product):
        """Remove a specific product from a cart."""
        product_id: str = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        """Get price of all cart."""
        return sum(Decimal(item["price"]) * item["count"] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def __iter__(self):
        products_ids = self.cart.keys()
        specific_products = Product.objects.filter(id__in=products_ids)
        cart = self.cart.copy()

        for product in specific_products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["count"]
            yield item

    def __len__(self):
        """Count of all products."""
        return sum(item["count"] for item in self.cart.values())