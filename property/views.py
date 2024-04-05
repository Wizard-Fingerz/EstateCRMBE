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
from django.core.mail import EmailMessage
from django.core.mail import send_mail

# @method_decorator(csrf_exempt, name='dispatch')


class CreatePropertyView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)
    # Use the appropriate authentication class
    authentication_classes = (TokenAuthentication,)

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
    # Use the appropriate authentication class
    authentication_classes = (TokenAuthentication,)
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
        phone_number = request.data.get('prospect_phone_number1')
        phone_number2 = request.data.get('prospect_phone_number2')
        whatsapp = request.data.get('prospect_whatsapp_phone_number')
        facebook_username = request.data.get('prospect_facebook_username')
        twitter_username = request.data.get('prospect_twitter_username')
        instagram_username = request.data.get('prospect_instagram_username')
        prospect_contact_source = request.data.get('prospect_contact_source')
        prospect_other_info = request.data.get('prospect_other_info')
        planned_commitment_date = request.data.get('planned_commitment_date')
        area_of_interest = request.data.get('area_of_interest')
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
            phone_number2=phone_number2,
            whatsapp=whatsapp,
            facebook_username=facebook_username,
            twitter_username=twitter_username,
            instagram_username=instagram_username,
            contact_source=prospect_contact_source,
            other_info=prospect_other_info,
            planned_commitment_date=planned_commitment_date,
            area_of_interest=area_of_interest,
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
            closed_won_count = Prospect.objects.filter(
                status='closed_won').count()
            closed_lost_count = Prospect.objects.filter(
                status='closed_lost').count()

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


class CustomerCountView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, *args, **kwargs):
        try:
            # Get the count of properties
            count = Customer.objects.count()

            # Serialize the count
            data = {
                'count': count,
            }
            serializer = CustomerCountSerializer(data)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProspectListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = Prospect.objects.all()
    serializer_class = ProspectSerializer


class CustomerListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class PropertyDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]


class ProspectAllocationView(generics.UpdateAPIView):
    queryset = Prospect.objects.all()
    serializer_class = ProspectAllocationSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SendEmailView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, prospect_id):
        print(request.data)
        try:
            prospect = Prospect.objects.get(pk=prospect_id)
        except Prospect.DoesNotExist:
            return Response({'error': 'Prospect not found'}, status=status.HTTP_404_NOT_FOUND)
        print(request.data)
        serializer = EmailSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']
            media = serializer.validated_data.get(
                'media')  # Retrieve media file if present
            email = prospect.email  # Assuming email field is present in Prospect model

            email_message = EmailMessage(
                subject,
                message,
                'adewale.oladiti28@gmail.com',  # Replace with your email
                [email],
            )

            if media:
                email_message.attach(
                    media.name, media.read(), media.content_type)

            email_message.send(fail_silently=False)

            return Response({'success': 'Email sent successfully'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BulkEmailView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        # Extract email content from request data
        subject = request.data.get('subject')
        message = request.data.get('message')
        media = request.data.get('media')

        if not subject or not message:
            return Response({'error': 'Subject and message are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get all prospects
        prospects = Prospect.objects.all()

        # Send email to each prospect
        for prospect in prospects:
            email = EmailMessage(
                subject, message, 'your@email.com', [prospect.email])

            if media:
                email.attach(media.name, media.read(), media.content_type)

            email.send(fail_silently=False)

        return Response({'success': 'Bulk email sent successfully'}, status=status.HTTP_200_OK)


class ConvertProspectToCustomer(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        print(request.data)
        serializer = CustomerConversionSerializer(data=request.data)
        if serializer.is_valid():
            prospect_id = serializer.validated_data['prospect_id']
            try:
                prospect = Prospect.objects.get(pk=prospect_id)
            except Prospect.DoesNotExist:
                return Response({'error': 'Prospect not found'}, status=status.HTTP_404_NOT_FOUND)

            # Create a customer
            customer = serializer.save(prospect=prospect)
            return Response({'success': 'Prospect converted to customer', 'customer_id': customer.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowUpReportCreateAPIView(generics.CreateAPIView):
    serializer_class = FollowUpReportSerializer
    
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, prospect_id):

        try:
            prospect = Prospect.objects.get(pk=prospect_id)
        except Prospect.DoesNotExist:
            return Response({'message': 'Prospect not found'}, status=status.HTTP_404_NOT_FOUND)
        # Set the marketer to the authenticated user
        request.data['marketer'] = request.user.id
        # Add the prospect instance to the request data
        request.data['prospect'] = prospect.id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MarketerFollowUpReportListAPIView(generics.ListAPIView):
    serializer_class = FollowUpReportSerializer
    
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        # Filter the FollowUpReport objects based on the marketer field
        # associated with the authenticated user (request.user)
        return FollowUpReport.objects.filter(marketer=self.request.user)