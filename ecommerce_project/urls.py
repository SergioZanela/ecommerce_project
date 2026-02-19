"""
URL configuration for ecommerce_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.shortcuts import render


def home_view(request):
    """
    Display the application's home page.

    This view acts as a safe landing page for:
    - successful login/registration redirects
    - permission-denied redirects (vendor_required/buyer_required)

    Returns:
        Rendered home page template.
    """
    return render(request, "shop/home.html")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view, name="home"),
    path("shop/", include("shop.urls")),
]
