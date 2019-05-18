from django.urls import path
from . import views

urlpatterns = [
    path("create_user/", views.create_user),
    path("log_in/", views.log_in),
    path("add_patient_measures/", views.add_patient_measures),
    path("add_doctor_measures/", views.add_doctor_measures),
    path("get_product_value/<int:id_product>", views.get_product_value),
    path("get_food_idea/", views.get_food_idea),
    path("get_user_info/<int:id_user>", views.get_user_info),
    path("get_user_measures/<int:id_user>", views.get_user_measures),
    path("get_doctor_measures/<int:id_user>", views.get_doctor_measures),
    path("get_exam_types/", views.get_exam_types),
    path("get_all_users/", views.get_all_users),
]
