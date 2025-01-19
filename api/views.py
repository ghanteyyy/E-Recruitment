from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *


def login_and_generate_tokens(request, email, password):
    user = authenticate(request, email=email, password=password)

    if user:
        login(request, user)  # Log the user in
        refresh = RefreshToken.for_user(user)  # Generate tokens

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    return None


class Register(APIView):
    def post(self, request):
        serialized = UserSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        user = serialized.save()  # Save the user and related models

        # Serialize the created user instance
        response_serializer = UserSerializer(user)

        # Automaically make the user login
        user_login = login_and_generate_tokens(request, request.data['email'], request.data['password'])

        # Response data
        response = {'user': response_serializer.data}
        response.update({'token': user_login})

        return Response(response, status=status.HTTP_200_OK)


class Login(APIView):
    def post(self, request, *args, **kwargs):
        user = login_and_generate_tokens(request, request.data.get('email'), request.data.get('password'))

        if user:
            return Response(user, status=status.HTTP_200_OK)

        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UpdateProfileImage(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        seriazlied = User_Profiles_Image_Serializers(data=request.data, context={'user': request.user})
        seriazlied.is_valid(raise_exception=True)

        profile_image = seriazlied.save()

        return Response(
            {"message": "Profile image updated successfully!", "data": User_Profiles_Image_Serializers(profile_image).data},
            status=status.HTTP_200_OK
        )

    def get(self, request):
        try:
            profile_image = models.User_Profile_Images.objects.get(user_id=request.user, status="CPP")

            serialized = User_Profiles_Image_Serializers(profile_image)

            return Response(serialized.data, status=status.HTTP_200_OK)

        except models.User_Profile_Images.DoesNotExist:
            return Response(
                {"error": "No current profile image found."},
                status=status.HTTP_404_NOT_FOUND
            )


class User_Document_view(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serialized = User_Documents_Serializer(data=request.data, context={'user': request.user})
        serialized.is_valid(raise_exception=True)

        user_document = serialized.save()

        return Response(User_Documents_Serializer(user_document).data, status=status.HTTP_200_OK)

    def get(self, request):
        try:
            objects = models.User_Documents.objects.filter(user_id=request.user, status='CD')

            serialized = User_Documents_Serializer(objects, many=True)

            return Response(serialized.data, status=status.HTTP_200_OK)

        except models.User_Documents.DoesNotExist:
            return Response(
                {"error": "No user's documents found."},
                 status=status.HTTP_404_NOT_FOUND
            )


class Recruiter_view(APIView):
    def post(self, request):
        user_serialized = UserSerializer(data=request.data)
        user_serialized.is_valid(raise_exception=True)

        user = user_serialized.save()
        user_data = UserSerializer(user).data

        recruiter_serialized = Recruiter_Serializer(data=request.data, context={"user": user})
        recruiter_serialized.is_valid(raise_exception=True)

        recruiter = recruiter_serialized.save()
        recruiter_data = Recruiter_Serializer(recruiter).data

        response = user_data | recruiter_data

        return Response(response, status=status.HTTP_200_OK)
