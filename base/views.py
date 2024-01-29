from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.http import JsonResponse
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product
from base.models import Product
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from base.models import Product

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)


        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        
        # ...


        return token




class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
# register
@api_view(['POST'])
def register(request):
    user = User.objects.create_user(
                username=request.data['username'],
                email=request.data['email'],
                password=request.data['password']
            )
    user.is_active = True
    user.is_staff = True
    user.save()
    return Response("new user born")
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def private(request):
    return Response('private')

def index(req):
    return JsonResponse('hello', safe=False)


# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Product
        fields = ['id', 'desc', 'price', 'image']

    def create(self, validated_data):
        image = validated_data.pop('image', None)
        product = Product.objects.create(**validated_data)
        if image:
            product.image.save(image.name, image)
        return product
        
def myProducts(req):
    all_books = ProductSerializer(Product.objects.all(), many=True).data
    return JsonResponse(all_books, safe=False)

@api_view(['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def products(request, id=None):
    if request.method == 'GET':
        if id is not None:
            product = get_object_or_404(Product, id=id, user=request.user)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        else:
            products = Product.objects.filter(user=request.user)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Assign the current user to the product
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product = get_object_or_404(Product, id=id)
        product.delete()
        return Response({"message": "Product deleted successfully"}, status=204)

    elif request.method in ['PUT', 'PATCH']:
        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(product, data=request.data, partial=request.method == 'PATCH')
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

