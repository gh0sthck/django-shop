from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.views import View

from users.forms import RegisterClientForm
from users.models import ShopClient


class UserRegister(View):
    form = RegisterClientForm()
    template_name = "user_register.html"
    template_name_done = "user_register_done.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, self.template_name, {"form": self.form})
        else:
            return redirect("home")

    def post(self, request):
        form = RegisterClientForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            new_user = form.save(commit=False)
            new_user.set_password(cd["password"])
            new_user.save()
            return render(
                request, self.template_name_done, {"new_client": new_user}
            )
        return render(request, self.template_name_done, {"new_client": None})


def user_page(request: HttpRequest, user_slug) -> HttpResponse:
    current_user: ShopClient = ShopClient.objects.get(slug=user_slug)
    return render(request, "user_page.html", {"current_user": current_user})
