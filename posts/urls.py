from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_post, name="create_post"),
    path("", views.post_list, name="post_list"),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('utils/date_ajax_get/', views.date_ajax_get, name='date_ajax_get'),
    path('utils/date_check_past/', views.date_check_past, name='date_check_past'),

    path('update/<slug:slug>/', views.update_post, name='update_post'),
    path('category/lists/', views.category_list, name='category_list'),
    path('category/delete/<slug:slug>/', views.delete_category, name='delete_category'),

    path('delete/<slug:slug>/', views.delete_post, name='delete_post'),
    path('unpublish_post/<slug:slug>/', views.unpublish_post, name='unpublish_post'),
    path('publish_post/<slug:slug>/', views.publish_post, name='publish_post'),

]