from rest_framework import serializers

from .models import User,Category,Specification,Product_Specifications,Products
from .utils import Util
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import Category, Specification, Products, Product_Specifications, ProductImage


#USER Operatrions

class UserRegistrationSerializer(serializers.ModelSerializer):

    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['email','name','password','password2']
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def validate(self, attrs):

        password=attrs.get('password')
        password2=attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError('password and confirm password does not match')

        return attrs
  
    
    def create(self, validated_data):
        # Remove the super().create(**validated_data) line
        # Instead, create an instance of the User model using the validated_data
        user = User(
            email=validated_data['email'],
            name=validated_data['name'],
        )

        # Set the password using the set_password method for proper hashing
        user.set_password(validated_data['password'])
        user.save()

        return user
    
class UserLoginSerialzer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email','name','password']

class UserChangePasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255, style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=255, style={'input_type':'password'},write_only=True)

    class Meta:
        fields=['password','password2']
    
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        user=self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("password and confirm password not match")
        user.set_password(password)
        user.save()

        return super().validate(attrs)


class MyTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.is_active)

class SendpasswordResetEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        fields=['email']
    def validate(self, attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            print("Uid: ",uid)
             # Instantiate your custom token generator
            token_generator = MyTokenGenerator()

            # Generate token using the instance of the token generator
            token = token_generator.make_token(user)
           # print("Password token generated: ", token)
          #  print("password token generater: ",token)

            link='http://localhost:8000/api/user/reset-password/'+uid+'/'+token
            #print("password link : ",link)
            body="Click Following Link to Reset your Password\n"+link
            data={
                "subject":"Password Reset Email!",
                "body":body,
                "to_email":user.email
            }
            Util.sent_email(data)

            return attrs
        else:
              raise serializers.ValidationError('Email is Not Registered with us!')


        return super().validate(attrs)
    
class UserPasswordResetSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255, style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=255, style={'input_type':'password'},write_only=True)

    class Meta:
        fields=['password','password2']
    
    def validate(self, attrs):
        try:
            password=attrs.get('password')
            password2=attrs.get('password2')
            uid=self.context.get('uid')
            token=self.context.get('token')

            if password != password2:
              raise serializers.ValidationError("password and confirm password not match")
            id=smart_str(urlsafe_base64_decode(uid))
            user=User.objects.get(id=id)

            if PasswordResetTokenGenerator().check_token(user,token):
              raise serializers.ValidationError('Token is not valid or Exprired!')
            user.set_password(password)
            user.save()

            return super().validate(attrs)
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise serializers.ValidationError('Token is not valid or Expired!')

#USER Operatrions END
        

#all product operations
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['Category_id', 'Category_name']

class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ['name', 'description']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']

class ProductsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # Nested serializer for the ForeignKey relationship
    product_images = ProductImageSerializer(many=True)  # Nested serializer for the ManyToManyField
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Products
        fields = ['product_id', 'product_name', 'product_price', 'stock_quantity', 'category', 'product_images', 'created_at', 'updated_at']

class ProductSpecificationsSerializer(serializers.ModelSerializer):
    product = ProductsSerializer()  # Nested serializer for the ForeignKey relationship
    specification = SpecificationSerializer()  # Nested serializer for the ForeignKey relationship

    class Meta:
        model = Product_Specifications
        fields = ['product', 'specification', 'value']