from django.urls import path
from . import views

urlpatterns = [
    path("get_product_value/<int:id_product>", views.get_product_value),
    path("get_food_idea/", views.get_food_idea),
]
