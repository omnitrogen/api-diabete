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
    return JsonResponse({"error": "not a POST"})


@csrf_exempt
def log_in(request):
    if request.method == "POST":
        answer = json.loads(request.body)
        if User.objects.filter(email=answer["email"], password=answer["password"]):
            user = User.objects.get(email=answer["email"], password=answer["password"])
            return JsonResponse(
                {
                    "userId": user.id,
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
            "weight": "",
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
        answer = json.loads(request.body)
        exam_type = ExamType(examType=answer["examType"])
        exam_type.save()
        user = User.objects.get(pk=answer["userId"])
        exam_report = ExamReport(user=user, timestamp=answer["timestamp"])
        exam_report.save()
        for elt in answer["measurements"]:
            measures = Measures(
                measuredQuantity=elt["measuredQuantity"],
                value=elt["value"],
                examType=exam_type,
            )
            measures.save()
            exam_report.measures.add(measures)

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


@csrf_exempt
def get_all_users(request):
    users = User.objects.all()
    userList = []
    for elt in users:
        userList.append(
            {
                "userId": elt.id,
                "email": elt.email,
                "password": elt.password,
                "firstName": elt.firstName,
                "lastName": elt.lastName,
                "userType": elt.userType,
                "birthDate": elt.birthDate,
                "gender": elt.gender,
                "weight": elt.weight,
                "height": elt.height,
            }
        )

    return JsonResponse({"users": userList})
