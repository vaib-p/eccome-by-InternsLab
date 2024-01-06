from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .Serializers import  UserRegistrationSerializer,UserLoginSerialzer,UserProfileSerializer,UserChangePasswordSerializer,SendpasswordResetEmailSerializer,UserPasswordResetSerializer,CategorySerializer, SpecificationSerializer, ProductsSerializer, ProductSpecificationsSerializer,ProductImageSerializer
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


from .models import Category, Specification, Products, Product_Specifications, ProductImage

#generate manual tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
# Create your views here.
class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response({ "token": token , "msg":"Registration succesfull!"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserLoginSerialzer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({ "token": token , "msg":"user login sucessfully!"},status=status.HTTP_201_CREATED)
            else:
                return Response({"errors":{"non_field_errors":['email or password not match']}},status=status.HTTP_404_NOT_FOUND)
            
class UserProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        serilalizer=UserProfileSerializer(request.user)
        return Response(serilalizer.data,status=status.HTTP_200_OK)
    

class UserChangePasswordView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializer=UserChangePasswordSerializer(data=request.data,context={'user':request.user})

        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"password change succesfully"},status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class SendpasswordResetEmailView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=SendpasswordResetEmailSerializer(data=request.data) 
        if serializer.is_valid(raise_exception=True):
             return Response({"msg":"Reset Link Sent please Check your Email."},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class UserPasswordResetView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,uid,token,format=None):
        serializer=UserPasswordResetSerializer(data=request.data,context={'uid':uid,'token':token})

        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"password reset succesfully!"},status=status.HTTP_200_OK)
        

#now for prodcut 
class CategoryAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SpecificationAPIView(APIView):
    def get(self, request):
        specifications = Specification.objects.all()
        serializer = SpecificationSerializer(specifications, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SpecificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductImageAPIView(APIView):
    queryset=ProductImage.objects.all()
    def get(self, request):
        product_images = ProductImage.objects.all()
        serializer = ProductImageSerializer(product_images, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductsAPIView(APIView):
    def get(self, request):
        products = Products.objects.all()
        serializer = ProductsSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductSpecificationsAPIView(APIView):
    def get(self, request):
        product_specifications = Product_Specifications.objects.all()
        serializer = ProductSpecificationsSerializer(product_specifications, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSpecificationsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







        
