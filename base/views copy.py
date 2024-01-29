from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.http import JsonResponse
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


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    # def create(self, validated_data):
    #     user = self.context['user']
    #     print(user)
    #     return Product.objects.create(**validated_data,user=user)
        
def myProducts(req):
    all_books = ProductSerializer(Product.objects.all(), many=True).data
    return JsonResponse(all_books, safe=False)

@api_view(['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def products(request, id=None):  # Corrected parameter name
    if request.method == 'GET':
        if id is not None:
            product = get_object_or_404(Product, id=id)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        else:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

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

