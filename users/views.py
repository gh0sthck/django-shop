from django.http import HttpResponse
from django.shortcuts import render

from users.forms import RegisterClientForm
from users.models import ShopClient


def user_register(request) -> HttpResponse:
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = RegisterClientForm(request.POST, request.FILES)
            if form.is_valid():
                clean_data: dict = form.cleaned_data
                new_user = form.save(commit=False)
                new_user.set_password(clean_data["password"])
                new_user.save()
                new_client = ShopClient(user=new_user, avatar=clean_data["avatar"],
                                        gender=clean_data["gender"],
                                        balance=0)
                new_client.save()

                return render(request, "user_register_done.html", {"new_client": new_client})
        else:
            form = RegisterClientForm()

        return render(request, "user_register.html", {"form": form})
    else:
        return HttpResponse("You're authenticated")