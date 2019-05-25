"""cafe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as resetviews
from user.views import auth, profile
from home.views import basic, manage


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', basic.index, name='index'),

    path('signup/', auth.signup, name='signup'),
    path('signin/', auth.signin, name='signin'),
    path('signout/', auth.signout, name='signout'),

    path('profile/verify/<token>/', auth.verify, name='profile-verify'),
    path('profile/', profile.view, name='profile-view'),
    path('profile/update/', profile.update, name='profile-update'),
    path('profile/add-money/', profile.add_money, name='profile-add-money'),
    path('profile/change-password/', auth.change_password , name='change-password'),

    path('branch/<uid>/<name>/', basic.branch, name='branch'),

    path('cart/', basic.cart, name='cart'),
    path('cart/add/', basic.add_cart, name='add-to-cart'),
    path('cart/update/', basic.update_cart, name='update-cart'),
    path('cart/checkout/', basic.cart_checkout, name='cart-checkout'),

    path('my-orders/', basic.my_orders, name='my-orders'),

    path('dashboard/', manage.dashboard, name='dashboard'),
    path('dashboard/order/<cart_number>/', manage.order, name='order'),
    path('branch/<uid>/<name>/update/time/', manage.branch_time_update, name='branch-time-update'),
    path('branch/<uid>/<name>/update/food/', manage.branch_food_update, name='branch-food-update'),

    path('password-reset/', resetviews.PasswordResetView.as_view(
        template_name='user/password/reset.html'),name='password_reset'),
    path('password-reset/done/', resetviews.PasswordResetDoneView.as_view(
        template_name='user/password/reset-done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', resetviews.PasswordResetConfirmView.as_view(
        template_name='user/password/reset-confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', resetviews.PasswordResetCompleteView.as_view(
        template_name='user/password/reset-complete.html'), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)