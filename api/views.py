from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *


class Register(APIView):
    def post(self, request):
        serialized = UserSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        user = serialized.save()  # Save the user and related models

        # Serialize the created user instance
        response_serializer = UserSerializer(user)
        return Response(response_serializer.data)
