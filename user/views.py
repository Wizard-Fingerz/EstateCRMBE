from django.shortcuts import render
from .serializers import *
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.authentication import TokenAuthentication
from .models import User
from rest_framework import generics, filters, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import *
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import MarketerSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate, login
# Create your views here.


class MarketerViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    # Use the appropriate authentication class
    authentication_classes = (TokenAuthentication,)
    queryset = User.objects.filter(is_marketer=True)
    serializer_class = MarketerSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    # Use the appropriate authentication class
    authentication_classes = (TokenAuthentication,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateMarketerView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        request.data['is_marketer'] = True  # Set the user as a marketer
        request.data['password'] = 'Password'  # Set the default password

        print(request.data)

        serializer = MarketerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateAccountantView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['is_accountant'] = True  # Set the user as an accountant
        data['password'] = 'Password'  # Set the default password

        serializer = AccountantSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)

        if user:
            # Check if password change is required
            change_password_required = False  # Replace this with your logic
            if change_password_required:
                return Response({'change_password_required': True, 'user_type': None})

            # Get or create a token for the user
            token, created = Token.objects.get_or_create(user=user)

            # Determine user type based on your user model
            user_type = None
            if user.is_marketer:
                user_type = 'marketer'
            elif user.is_accountant:
                user_type = 'accountant'
            else:
                user_type = 'admin'
            # Add more conditions for other user types if needed

            return Response({'token': token.key, 'user_type': user_type})
        else:
            return Response({'error': 'Invalid credentials'}, status=401)


class PasswordChangeCheckView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # Check if the user has changed their password
        user = self.request.user

        # Replace 'default_password' with the actual default password you are using
        is_default_password = user.check_password('default_password')

        return Response({'change_password_required': is_default_password})


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication,]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Get the current user
            user = request.user

            # Check if the old password is correct
            old_password = serializer.validated_data['old_password']
            if not user.check_password(old_password):
                return Response({'detail': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

            # Update the password
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()

            # Re-authenticate the user with the new password
            user = authenticate(username=user.username, password=new_password)
            if user:
                login(request, user)

            return Response({'detail': 'Password changed successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MarketerCountView(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, *args, **kwargs):
        try:
            count = User.objects.filter(is_marketer=True).count()
            serializer = MarketerCountSerializer({'count': count})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MarketerDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = MarketerSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

class GetMarketerDetails(APIView):
    def get(self, request, marketer_id):
        # Get the marketer instance or return 404 if not found
        marketer = get_object_or_404(User, id=marketer_id, is_marketer=True)

        # Serialize the marketer data
        serializer = UserSerializer(marketer)

        return Response(serializer.data, status=status.HTTP_200_OK)

class UserDetailsView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Retrieve the currently authenticated user
        return self.request.user