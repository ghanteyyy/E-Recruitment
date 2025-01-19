from rest_framework import serializers
from . import models as models


class User_Name_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.User_Name
        fields = ['first_name', 'middle_name', 'last_name']


class User_Address_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.User_Address
        fields = ['address_line1', 'address_line2', 'city', 'state', 'country']


class User_Contact_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.User_Contact
        fields = ['phone_number', 'status']


class UserSerializer(serializers.ModelSerializer):
    name = User_Name_Serializer(source='user_name', many=True, read_only=True)
    address = User_Address_Serializer(source='user_address', many=True, read_only=True)
    contact = User_Contact_Serializer(source='user_contact', many=True, read_only=True)

    class Meta:
        model = models.CustomUser
        fields = ['email', 'password', 'gender', 'dob', 'name', 'address', 'contact']
        extra_kwargs = {
            'password': {'write_only': True},  # Hide password in response
        }

    def create(self, validated_data):
        # Extract nested data from the request (not validated_data)
        name_data = self.initial_data.get('name', [])
        address_data = self.initial_data.get('address', [])
        contact_data = self.initial_data.get('contact', [])

        # Create the main user instance
        password = validated_data.pop('password')
        user = models.CustomUser(**validated_data)
        user.set_password(password)  # Use set_password for hashing
        user.save()

        # Create related models (for each item in the lists)
        models.User_Name.objects.create(user_id=user, **name_data)
        models.User_Address.objects.create(user_id=user, **address_data)
        models.User_Contact.objects.create(user_id=user, **contact_data)

        return user


class User_Profiles_Image_Serializers(serializers.ModelSerializer):
    class Meta:
        model = models.User_Profile_Images
        fields = ['image']

    def create(self, validated_data):
        user = self.context['user']

        try:
            current_profile_images = models.User_Profile_Images.objects.filter(user_id=user, status='CPP')

            for current_profile_image in current_profile_images:
                current_profile_image.status = "PPP"
                current_profile_image.save()

        except models.User_Profile_Images.DoesNotExist:
            pass

        new_profile_image = models.User_Profile_Images.objects.create(
                                user_id=user,
                                image=validated_data.get('image')
                            )

        return new_profile_image


class User_Documents_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.User_Documents
        fields = ['title', 'file']

    def create(self, validated_data):
        user = self.context['user']
        user_document = models.User_Documents.objects.create(
            user_id=user,
            title=validated_data.get('title'),
            file=validated_data.get('file')
        )

        return user_document
