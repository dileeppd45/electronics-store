from . import views
from django.urls import path

urlpatterns = [
    path('',views.login_home,name="loginhome"),
    path('login', views.login, name="login"),
    path('loginhome',views.login_home,name="loginhome"),
    path('adminindex',views.admin_home,name="adminindex"),
    path('add_category', views.add_category, name="add_category"),
    path('view_category', views.view_category, name="view_category"),
    path('add_items/<str:id>', views.add_items, name='add_items'),
    path('view_items/<str:id>', views.view_items, name='view_items'),
    path('edit_items/<str:id>', views.edit_items, name='edit_items'),
    path('delete_items/<str:id>', views.delete_items, name='delete_items'),
    path('payed_orders',views.payed_orders, name='payed_orders'),
    path('ship_item/<str:id>', views.ship_item, name='ship_item'),
    path('shipped_orders', views.shipped_orders, name='shipped_orders'),
    path('view_orders/<str:id>', views.view_orders, name='view_orders'),
    path('return_requests',views.return_requests, name='return_requests'),
    path('approve_return/<str:id>', views.approve_return, name='approve_return'),
    path('cancel_return/<str:id>', views.cancel_return, name='cancel_return'),
    path('return_approved', views.return_approved, name='return_approved'),
    path('return_canceled', views.return_cancelled, name='return_canceled'),
    path('collect_return/<str:id>', views.collect_return, name='collect_return'),
    path('adminlogout', views.admin_logout, name='adminlogout'),
    path('view_feedback', views.view_feedback, name='view_feedback'),
    path('reply_feed/<str:id>', views.reply_feed, name='reply_feed'),
]