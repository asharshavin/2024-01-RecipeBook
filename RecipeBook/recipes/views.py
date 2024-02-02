from django.db import transaction
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from recipes.models import Product, Dish, Composition


@transaction.atomic
def add_product_to_recipe(request):
    if request.method == 'GET':
        dish_id = request.GET.get('dish_id')
        product_id = request.GET.get('product_id')
        volume = request.GET.get('volume')

        if dish_id and product_id and volume:
            dish = get_object_or_404(Dish, id=dish_id)
            product = get_object_or_404(Product, id=product_id)

            dish_product, created = Composition.objects.get_or_create(dish=dish, product=product)
            dish_product.volume = volume
            dish_product.save()

            return HttpResponse(f"Product {product.title} added to dish {dish.title} with weight {volume} grams.")
        else:
            return HttpResponse("Invalid parameters.")

    return HttpResponse("Invalid method.")


@transaction.atomic
def cook_recipe(request):
    if request.method == 'GET':
        dish_id = request.GET.get('dish_id')

        if dish_id:

            dish = get_object_or_404(Dish, id=dish_id)

            Product.objects.select_for_update().filter(dish=dish).update(quantity=F('quantity') + 1)

            return HttpResponse(f"Dish {dish.title} cooked successfully.")
        else:
            return HttpResponse("Invalid parameters.")

    return HttpResponse("Invalid method.")


def show_recipes_without_product(request):
    if request.method == 'GET':
        product_id = request.GET.get('product_id')

        if product_id:
            product = get_object_or_404(Product, id=product_id)

            dishes_without_product = Dish.objects.exclude(product=product)
            dishes_too_few_product = Dish.objects.filter(product=product, composition__volume__lt=10)
            dishes =  dishes_without_product.union(dishes_too_few_product).order_by("title")
            context = {'dishes': dishes, 'product': product}
            return render(request, 'recipes\show_recipes_without_product.html', context)
        else:
            return HttpResponse("Invalid parameters.")

    return HttpResponse("Invalid method.")


"""
SELECT "recipes_dish"."id", "recipes_dish"."title" FROM "recipes_dish" WHERE NOT (EXISTS(SELECT 1 AS "a" FROM "recipes_сomposition" U1 WHERE (U1."product_id" = 1 AND U1."dish_id" = ("recipes_dish"."id")) LIMIT 1))
"""
