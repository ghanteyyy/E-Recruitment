from rest_framework import serializers
from .models import CustomUser, User_Name, User_Address, User_Contact


class User_Name_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User_Name
        fields = ['first_name', 'middle_name', 'last_name']


class User_Address_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User_Address
        fields = ['address_line1', 'address_line2', 'city', 'state', 'country']


class User_Contact_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User_Contact
        fields = ['phone_number', 'status']


class UserSerializer(serializers.ModelSerializer):
    name = User_Name_Serializer(source='user_name', many=True, read_only=True)
    address = User_Address_Serializer(source='user_address', many=True, read_only=True)
    contact = User_Contact_Serializer(source='user_contact', many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'gender', 'dob', 'name', 'address', 'contact']
        extra_kwargs = {
            'password': {'write_only': True},  # Hide password in response
        }

    def create(self, validated_data):
        # Extract nested data from the request (not validated_data)
        name_data = self.initial_data.get('name', [])
        address_data = self.initial_data.get('address', [])
        contact_data = self.initial_data.get('contact', [])

        print(name_data, '\n\n', address_data, '\n\n', contact_data)

        # Create the main user instance
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)  # Use set_password for hashing
        user.save()

        # Create related models (for each item in the lists)
        User_Name.objects.create(user_id=user, **name_data)
        User_Address.objects.create(user_id=user, **address_data)
        User_Contact.objects.create(user_id=user, **contact_data)

        return user
