from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse

from api.models import User, PatientMeasures, ExamType, Measures, ExamReport

from django.views.decorators.csrf import csrf_exempt

import json
import requests
import random

from pprint import pprint


@csrf_exempt
def get_product_value(request, id_product):
    answer = requests.get(
        "https://world.openfoodfacts.org/api/v0/product/" + str(id_product) + ".json"
    ).json()
    return JsonResponse(
        {
            "nutrition_score_debug": str(
                answer["product"]["nutrition_score_debug"].split()
            ),
            "nutritions_score": answer["product"]["nutriments"]["nutrition-score-fr"],
            "nova": answer["product"]["nova_group"],
        }
    )


@csrf_exempt
def get_food_idea(request):
    foodList = [
        "poissons gras",
        "légumes verts à feuilles",
        "légumes verts à feuilles",
        "œufs",
        "graines de Chia",
        "curcuma",
        "yaourt grec",
        "noix",
        "brocoli",
        "huile d’olive extra-vierge",
        "graines de lin",
        "vinaigre de cidre de pomme",
        "fraises",
        "ail",
        "courge",
        "nouilles Shirataki",
    ]
    return JsonResponse({"super_cool_food": random.choice(foodList)})


@csrf_exempt
def create_user(request):
    if request.method == "POST":
        answer = json.loads(request.body)
        user = User(
            email=answer["email"],
            password=answer["password"],
            first_name=answer["first_name"],
            last_name=answer["last_name"],
            user_type=answer["user_type"],
            age=answer["age"],
            gender=answer["gender"],
            weight=answer["weight"],
            height=answer["height"],
        )
        user.save()
        return JsonResponse({"user_id": user.id})


@csrf_exempt
def log_in(request):
    if request.method == "POST":
        answer = json.loads(request.body)
        if User.objects.filter(email=answer["email"], password=answer["password"]):
            user = User.objects.get(email=answer["email"], password=answer["password"])
            return JsonResponse({"user_id": user.id})
        return JsonResponse({"error": "Username or password is wrong"})


@csrf_exempt
def add_patient_measures(request):
    if request.method == "POST":
        answer = json.loads(request.body)
        user = User.objects.get(pk=answer["user_id"])
        measure = PatientMeasures(
            user=user,
            glycemia=answer["glycemia"],
            ldl=answer["ldl"],
            hdl=answer["hdl"],
            trygliceride=answer["trygliceride"],
            blood_pressure=answer["blood_pressure"],
            weight=answer["weight"],
            heartbeat=answer["heartbeat"],
            timestamp=answer["timestamp"],
        )
        measure.save()
        return JsonResponse({"measure_id": measure.id, "user_id": user.id})


@csrf_exempt
def add_doctor_measures(request):
    if request.method == "POST":
        answer = json.loads(request.body)
        exam_type = ExamType(exam_type=answer["exam_type"])
        exam_type.save()
        measures = Measures(value=answer["value"], exam_type=exam_type)
        measures.save()
        user = User.objects.get(pk=answer["user_id"])
        exam_report = ExamReport(
            user=user, timestamp=answer["timestamp"], measures=measures
        )
        exam_report.save()
        return JsonResponse({"exam_report_id": exam_report.id, "user_id": user.id})
