from typing import Any

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView

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
            return redirect("user_page", request.user.slug)

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


class EditUser(UpdateView):
    model = ShopClient
    form_class = RegisterClientForm
    template_name = "user_register.html"
    
    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        ctx = super().get_context_data(*args, **kwargs)
        ctx["edit"] = True
        return ctx
    
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user.slug == self.get_object().slug or request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        else:
            return redirect("user_page", request.user.slug)
    
    def get_success_url(self, request) -> str:
        return reverse_lazy("user_page", request.user.slug)
