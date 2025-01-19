from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class Register(APIView):
    def post(self, request):
        serialized = UserSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        user = serialized.save()  # Save the user and related models

        # Serialize the created user instance
        response_serializer = UserSerializer(user)
        return Response(response_serializer.data)


class Login(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'accress': str(refresh.access_token)
            }, status=status.HTTP_200_OK)

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
