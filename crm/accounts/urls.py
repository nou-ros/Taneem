from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('about/', views.about, name='about'),
    path('contact', views.contact, name='contact'),

    path('products/', views.products, name='products'),
    path('orders/', views.orders, name='orders'),
    path('all_customers/', views.allCustomers, name='all_customers'),
    path('customer/<slug:pk>/', views.customer, name='customer'),

    path('user/', views.userPage, name='user'),
    path('account/', views.accountSettings, name='account'),

    path('create_order/<slug:pk>/', views.createOrder, name='create_order'),
    path('update_order/<slug:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<slug:pk>/', views.deleteOrder, name='delete_order'),

    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    # from django auth views
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name = 'reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'), name = 'password_reset_done'),
    # uidb64: The user’s id encoded in base 64.
    # token: Token to check that the password is valid.   
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'), name = 'password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name = 'password_reset_complete'),
]

"""
1 - Submit email form  // PasswordResetView.as_view()
2 - Email sent success message  // PasswordResetDoneView.as_view()
3 - Link to password resest form in email  // PasswordResetConfirmView.as_view()
4 - Password successfully changed message // PasswordResetCompleteView.as_view()

"""