from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.clickjacking import xframe_options_exempt


from api.models import (
    User,
    PatientMeasures,
    ExamType,
    Measures,
    ExamReport,
    DiseaseRisk,
)

from django.views.decorators.csrf import csrf_exempt

import json
import requests
import random

from pprint import pprint


@xframe_options_exempt
def graph(request, graph_id):
    return render_to_response("Sample" + str(graph_id) + ".html")


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
                    "xp": user.xp,
                }
            )
        return JsonResponse({"error": "Username or password is wrong"})


@csrf_exempt
def add_patient_measures(request):
    if request.method == "POST":
        a = json.loads(request.body)
        user = User.objects.get(pk=a["userId"])
        answer = {
            "glycemia": None,
            "ldl": None,
            "hdl": None,
            "trygliceride": None,
            "bloodPressure": None,
            "weight": None,
            "heartbeat": None,
            "timestamp": "",
        }
        answer.update(a)
        measure = PatientMeasures(
            user=user,
            glycemia=answer["glycemia"],
            ldl=answer["ldl"],
            hdl=answer["hdl"],
            trygliceride=answer["trygliceride"],
            bloodPressure=answer["bloodPressure"],
            weight=answer["weight"],
            heartbeat=answer["heartbeat"],
            timestamp=answer["timestamp"],
        )
        measure.save()
        user.xp += 1
        user.save()
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
            dicValue = {"value": None}
            dicValue.update(elt)
            measures = Measures(
                measuredQuantity=elt["measuredQuantity"],
                value=dicValue["value"],
                examType=exam_type,
            )
            measures.save()
            exam_report.measures.add(measures)

        exam_report.save()
        return JsonResponse({"examReportId": exam_report.id, "userId": user.id})


@csrf_exempt
def get_user_info(request, id_user):
    user = User.objects.get(pk=id_user)
    diseases = serializers.serialize(
        "json", DiseaseRisk.objects.filter(user__id=user.id)
    )
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
            "xp": user.xp,
            "diseases": diseases,
        }
    )


@csrf_exempt
def get_user_measures(request, id_user):
    if PatientMeasures.objects.filter(user__id=id_user):
        measures = list(PatientMeasures.objects.filter(user__id=id_user).values())[0]
        return JsonResponse({"measures": measures})
    return JsonResponse({"error": "patient do not have measures"})


@csrf_exempt
def get_doctor_measures(request, id_user):
    if ExamReport.objects.filter(user__id=1)[0]:
        exam_report = serializers.serialize("json", ExamReport.objects.get(pk=id_user))
        return JsonResponse(measures)
    return JsonResponse({"error": "patient do not have measures"})


@csrf_exempt
def get_exam_types(request):
    examTypes = list(ExamType.objects.values("examType"))
    return JsonResponse({"examTypes": examTypes})


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
                "xp": elt.xp,
            }
        )

    return JsonResponse({"users": userList})
