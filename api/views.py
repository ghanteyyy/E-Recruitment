import django.contrib.auth as auth
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *


jwt_tokens = dict()


def login_and_generate_tokens(request, email, password):
    global jwt_tokens

    user = auth.authenticate(request, email=email, password=password)

    if user:
        auth.login(request, user)  # Log the user in
        refresh = RefreshToken.for_user(user)  # Generate tokens

        jwt_tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

        return jwt_tokens

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
        tokens = login_and_generate_tokens(request, request.data.get('email'), request.data.get('password'))

        if tokens:
            user = models.CustomUser.objects.get(email=request.data.get('email'))
            user_data = UserSerializer(user).data

            response = user_data | {'token': tokens}
            return Response(response, status=status.HTTP_200_OK)

        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        auth.logout(request)

        return Response({'message': 'User logout successfully'}, status=status.HTTP_200_OK)


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

            if not objects:
                return Response({'error': 'User document(s) not found'}, status=status.HTTP_200_OK)

            serialized = User_Documents_Serializer(objects, many=True)

            return Response(serialized.data, status=status.HTTP_200_OK)

        except models.User_Documents.DoesNotExist:
            return Response(
                {"error": "No user's documents found."},
                 status=status.HTTP_404_NOT_FOUND
            )


class Recruiter_view(APIView):
    def get_permission(self):
        if self.request.method == 'GET' or (self.request.method == 'POST' and self.request.user):
            self.permission_classes = [IsAuthenticated]

        else:
            self.permission_classes = [AllowAny]

        return super().get_permissions()

    def get(self, request):
        user_data = UserSerializer(request.user).data

        recruiter = models.Recruiter.objects.get(user_id=request.user)
        recruiter_data = Recruiter_Serializer(recruiter).data

        reponse_data = recruiter_data | user_data | {'token': jwt_tokens}

        return Response(reponse_data, status=status.HTTP_200_OK)

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


class Job_view(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_staff:
            recruiter = models.Recruiter.objects.get(user_id=request.user)

            jobs = models.Jobs.objects.filter(recruiter_id=recruiter)
            job_serialized = Jobs_Serializer(jobs, many=True)

        else:
            jobs = models.Jobs.objects.filter(status='OP')
            job_serialized = Jobs_Serializer(jobs, many=True)

        return Response(job_serialized.data, status=status.HTTP_200_OK)

    def post(self, request):
        recruiter = models.Recruiter.objects.get(user_id=request.user)

        job_serialized = Jobs_Serializer(data=request.data, context={'recruiter': recruiter})
        job_serialized.is_valid(raise_exception=True)
        job = job_serialized.save()

        job_data = Jobs_Serializer(job)

        return Response(job_data.data, status=status.HTTP_200_OK)

    def delete(self, request):
        try:
            job_to_delete = models.Jobs.objects.get(id=request.data.get('job_id'))
            job_to_delete.delete()

            return Response({'message': 'Job has been deleted'}, status=status.HTTP_200_OK)

        except models.Jobs.DoesNotExist:
            return Response({'message': 'Job does not exist'}, status=status.HTTP_200_OK)
