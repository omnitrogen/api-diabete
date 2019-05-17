from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
import requests
import random


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
