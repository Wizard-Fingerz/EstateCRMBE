from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from .models import *
from .serializers import *

# @method_decorator(csrf_exempt, name='dispatch')
class CreatePropertyView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)  # Use the appropriate authentication class
    
    def post(self, request, *args, **kwargs):
        property_name = request.data.get('property_name')
        property_address = request.data.get('property_address')
        property_description = request.data.get('property_description')
        property_value = request.data.get('property_value')
        property_type = request.data.get('property_type')
        other_property_type = request.data.get('property_other_type')
        property_media1 = request.data.get('property_media1')
        property_media2 = request.data.get('property_media2')
        property_media3 = request.data.get('property_media3')
        property_media4 = request.data.get('property_media4')

        print(property_name)
        print(property_media1)

        # Save the property data to the database
        property_obj = Property.objects.create(
            name=property_name,
            address=property_address,
            description=property_description,
            value=property_value,
            type=property_type,
            other_property_type=other_property_type,
            media1=property_media1,
            media2=property_media2,
            media3=property_media3,
            media4=property_media4,
        )

        return JsonResponse({'message': 'Property created successfully'}, status=201)


class PropertyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


class PropertyMarketerViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)  # Use the appropriate authentication class
    queryset = User.objects.filter(is_marketer=True)
    serializer_class = PropertyMarketerSerializer

class CreateProspectView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        prefix = request.data.get('prospect_prefix')
        full_name = request.data.get('prospect_name')
        address = request.data.get('prospect_address')
        email = request.data.get('prospect_email')
        phone_number = request.data.get('prospect_phone_number')
        whatsapp = request.data.get('prospect_whatsapp_phone_number')
        property_id = request.data.get('property')
        marketer_id = request.data.get('marketer')

        if marketer_id == '':
            marketer_instance = None
        else:
            marketer_instance = get_object_or_404(User, id=marketer_id)


        if property_id == '':
            property_instance = None
        else:
        # Fetch the corresponding Property and Marketer instances
            property_instance = get_object_or_404(Property, id=property_id)

        prospect_obj = Prospect.objects.create(
            prefix=prefix,
            full_name=full_name,
            address=address,
            email=email,
            phone_number=phone_number,
            whatsapp=whatsapp,
            property=property_instance,
            follow_up_marketer=marketer_instance,
        )

        return Response({'message': 'Prospect created successfully'}, status=status.HTTP_201_CREATED)
    
class PropertyCountView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def get(self, request, *args, **kwargs):
        try:
            # Get the count of properties
            count = Property.objects.count()

            # Serialize the count
            serializer = PropertyCountSerializer({'count': count})

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProspectCountView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, *args, **kwargs):
        try:
            # Get the count of properties
            count = Prospect.objects.count()
            closed_won_count = Prospect.objects.filter(status='closed_won').count()
            closed_lost_count = Prospect.objects.filter(status='closed_lost').count()

            # Serialize the count
            data = {
                'count': count,
                'closed_won': closed_won_count,
                'closed_lost': closed_lost_count
            }
            serializer = ProspectCountSerializer(data)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProspectListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = Prospect.objects.all()
    serializer_class = ProspectSerializer

class PropertyDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]