from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from circulation import views
from circulation.views import (
    BorrowerListView, BorrowerCreateView, BorrowerUpdateView, BorrowerDeleteView,
)

urlpatterns = [
    path('', views.public_search, name='home'),

    path('admin/', admin.site.urls),

    path('reception/login/', views.reception_login, name='reception_login'),
    path('reception/', views.reception_dashboard, name='reception_dashboard'),
    path('manager/login/', views.manager_login, name='manager_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    path('reception/borrow/', views.borrow_item, name='borrow_item'),
    path('reception/return/', views.return_item, name='return_item'),
    path('reception/add-item/', views.add_item, name='add_item'),
    path('reception/fines/', views.manage_fines, name='manage_fines'),
    path('reception/item-lookup/', views.item_lookup, name='item_lookup'),
    path('reception/borrower-lookup/', views.borrower_lookup, name='borrower_lookup'),
    path('reception/borrowers/', BorrowerListView.as_view(), name='borrower_list'),
    path('reception/borrowers/add/', BorrowerCreateView.as_view(), name='borrower_add'),
    path('reception/borrowers/<int:pk>/edit/', BorrowerUpdateView.as_view(), name='borrower_edit'),
    path('reception/borrowers/<int:pk>/delete/', BorrowerDeleteView.as_view(), name='borrower_delete'),

    path('manager/stats/borrowing/', views.stats_borrowing, name='stats_borrowing'),
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/create-reception/', views.create_reception_account, name='create_reception_account'),
    path('manager/stats/items/', views.stats_items, name='stats_items'),
    path('manager/stats/fines/', views.stats_fines, name='stats_fines'),

    path('account/password-change/', views.MyPasswordChangeView.as_view(), name='password_change'),
    path('account/password-change/done/', views.MyPasswordChangeDoneView.as_view(), name='password_change_done'),

    path('search/', views.public_search, name='public_search'),
]