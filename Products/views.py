import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Category


@api_view(['POST']) # API_VIEW ES UN DECORADOR QUE INDICA QUE TODAS LAS SOLICITUDES HTTP SERÁN TIPO POST
def createCategory(request):

    data = request.data #Request.data transforma los datos enviados por el usuario a Diccionario
    image = request.FILES.get('image') #De esta manera obtenemos la imagen del request

    category = Category.objects.create( # Esta línea está usando el modelo Category para crear un nuevo objeto

        name = data['categoryName'],# name es el nombre del atributo del modelo, data es la información que estamos recibiendo del request y categoryName es lo que se envió 
        image = image

    )

    return JsonResponse({'id': category.id, 'name': category.name, 'image_url': category.image.url if category.image else None})


@api_view(['GET'])
def showCategories(request):

    categories = Category.objects.all().values() #Obtenemos todas las categorias y con el .values  trasnformamos la consulta en un diccionario

    return JsonResponse(list(categories), safe=False)


@api_view(['DELETE'])
def deleteCategory(request):

    try:
        data = request.data
        categoryId = data['id']
        category = get_object_or_404(Category, pk = categoryId)

        category.delete()

        return JsonResponse({'message' : 'Category named ' + category.name + " was deleted succesfully!"}, status = 204)
    
    except (ValueError, KeyError):
        return JsonResponse({"message" : 'Category wasn´t deleted'}, status = 400)
    

@api_view(['PUT']) #PUT ACTUALIZAR
def updateCategory(request):

    try:
        data = request.data
        categoryId = data['id']
        category = get_object_or_404(Category, pk = categoryId)

        image = request.FILES.get('image')

        category.name = data.get('categoryName', category.name)
        
        if image:
            category.image = image

        category.save()

        return JsonResponse({'id' : category.id, 'name' : category.name}, status = 200)
    
    except(ValueError, KeyError):

        return JsonResponse({"error": 'Id Category wasn´t found'})
    
# holiiiiiiiiiiiiiiiiiiiiiii

