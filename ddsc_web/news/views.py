from django.shortcuts import render
from .models import NewsSubscriber


def subscribe_to_news(request):
    if request.method == "POST":
        subscriber = NewsSubscriber(email=request.POST.get("email"))
        subscriber.save()

        return render(
            request,
            "news/subscribe_success.html",
            {
                "section": "news",
                "footer_class": "fixed-bottom",
                "subscriber": subscriber,
            },
        )
    else:
        return render(request, "home.html")
