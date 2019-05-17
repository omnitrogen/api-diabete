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
        if User.objects.filter(email=answer["email"]):
            return JsonResponse({"error": "email already in use"})
        user = User(
            email=answer["email"],
            password=answer["password"],
            firstName=answer["firstName"],
            lastName=answer["lastName"],
            userType=answer["userType"],
            birthDate=answer["birthDate"],
            gender=answer["gender"],
            weight=answer["weight"],
            height=answer["height"],
        )
        user.save()
        return JsonResponse(
            {
                "userId": user.id,
                "email": answer["email"],
                "password": answer["password"],
                "firstName": answer["firstName"],
                "lastName": answer["lastName"],
                "userType": answer["userType"],
                "birthDate": answer["birthDate"],
                "gender": answer["gender"],
                "weight": answer["weight"],
                "height": answer["height"],
            }
        )


@csrf_exempt
def log_in(request):
    if request.method == "POST":
        answer = json.loads(request.body)
        if User.objects.filter(email=answer["email"], password=answer["password"]):
            user = User.objects.get(email=answer["email"], password=answer["password"])
            return JsonResponse(
                {
                    "userId": user.id,
                    "email": answer["email"],
                    "password": answer["password"],
                    "firstName": answer["firstName"],
                    "lastName": answer["lastName"],
                    "userType": answer["userType"],
                    "birthDate": answer["birthDate"],
                    "gender": answer["gender"],
                    "weight": answer["weight"],
                    "height": answer["height"],
                }
            )
        return JsonResponse({"error": "Username or password is wrong"})


@csrf_exempt
def add_patient_measures(request):
    if request.method == "POST":
        a = json.loads(request.body)
        user = User.objects.get(pk=a["userId"])
        answer = {
            "glycemia": "",
            "ldl": "",
            "hdl": "",
            "trygliceride": "",
            "bloodPressure": "",
            "eight": "",
            "heartbeat": "",
            "timestamp": "",
        }
        answer.update(a)
        measure = PatientMeasures(
            user=user,
            glycemia=answer["glycemia"],
            ldl=answer["ldl"],
            hdl=answer["hdl"],
            trygliceride=answer["trygliceride"],
            blood_pressure=answer["bloodPressure"],
            weight=answer["weight"],
            heartbeat=answer["heartbeat"],
            timestamp=answer["timestamp"],
        )
        measure.save()
        return JsonResponse({"measureId": measure.id, "userId": user.id})


@csrf_exempt
def add_doctor_measures(request):
    if request.method == "POST":
        a = json.loads(request.body)
        answer = {"examType": "", "value": "", "userId": "", "timestamp": ""}
        answer.update(a)
        exam_type = ExamType(exam_type=answer["examType"])
        exam_type.save()
        measures = Measures(value=answer["value"], exam_type=exam_type)
        measures.save()
        user = User.objects.get(pk=answer["userId"])
        exam_report = ExamReport(
            user=user, timestamp=answer["timestamp"], measures=measures
        )
        exam_report.save()
        return JsonResponse({"examReportId": exam_report.id, "userId": user.id})


@csrf_exempt
def get_user_info(request, id_user):
    user = User.objects.get(pk=id_user)
    return JsonResponse(
        {
            "email": user.email,
            "password": user.password,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "userType": user.userType,
            "birthDate": user.birthDate,
            "gender": user.gender,
            "weight": user.weight,
            "height": user.height,
        }
    )
