from django.urls import path
from recipes import views

urlpatterns = [
	path('add_product_to_recipe/', views.add_product_to_recipe),
	path('cook_dish/', views.cook_recipe),
	path('show_recipes_without_product/', views.show_recipes_without_product),
]


