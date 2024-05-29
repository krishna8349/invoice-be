from django.shortcuts import render
from rest_framework import status
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from app.customerbillapp.models import *
from app.customerbillapp.serializers import *
# from app.customerbillapp.serializers import CustomerBillOnDemandSerilizer,CustomerBill,BillingAccountRefSerializer, BillRefSerializer,RelatedPartyRefSerializer
# MoneySerializer, PaymentRefSerializer,AppliedPaymentSerializer,QuantitySerializer,TimePeriodSerializer, AttachmentRefOrValueSerializer,AccountBalanceSerializer, PaymentMethodRefSerializer, TaxItemSerializer, FinancialAccountRefSerializer, ContactSerializer, ContactMediumSerializer, MediumCharacteristicSerializer, GeographicAddressSerializer, GeographicSubAddressSerializer, RelatedGeographicLocationRefOrValueSerializer, BillCycleRefSerializer, CharacteristicSerializer, CustomerBillSerializer, AppliedCustomerBillingRateSerializer
from rest_framework import viewsets

# # Create your views here.
class CustomerBillOnDemandViewSet(viewsets.ModelViewSet):
    """
    In this class we can use create function for post data in table, get function to get the list and detail by using id.
    """
    # filter_backends = (DynamicSearchFilter,)
    serializer_class = CustomerBillOnDemandSerilizer
    queryset = (CustomerBillOnDemand.objects.all())

    #Post method
    def create(self, request):
        post_data = request.data

        #Create billing account ref
        billing_account_ref_instance=self.create_billing_account_ref(
            post_data.get('billingAccount',{})
        )

        #Create bill ref
        bill_ref_instance=self.create_bill_ref(
            post_data.get('customerBill',{})
        )

        #create related party ref
        related_party_ref_instance=self.create_related_party_ref(
            post_data.get('relatedParty',{})
        )

        #For save data
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(billingAccount=billing_account_ref_instance,
                            customerBill=bill_ref_instance,
                            relatedParty=related_party_ref_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response("Please provide valid details", status=status.HTTP_400_BAD_REQUEST)

        # Get method
    def get(self):
        return self.queryset

    #Post data in Billing Acoount Ref model
    def create_billing_account_ref(self, billing_account_ref_data):
        billing_account_serializer = BillingAccountRefSerializer(data=billing_account_ref_data)
        billing_account_obj = None
        if billing_account_serializer.is_valid():
            billing_account_obj = billing_account_serializer.save()
            return billing_account_obj
        return billing_account_obj

    # Post data in Bill Ref model
    def create_bill_ref(self, billing_ref_data):
        billing_ref_info = BillRefSerializer(data=billing_ref_data)
        billing_ref_obj  = None
        if billing_ref_info.is_valid():
            billing_ref_obj = billing_ref_info.save()
            return billing_ref_obj
        return billing_ref_obj

    #Post data in Related Party Ref model
    def create_related_party_ref(self, related_rarty_ref_info):
        related_rarty_ref_serializer = RelatedPartyRefSerializer(data=related_rarty_ref_info)
        related_rarty_ref_obj = None
        if related_rarty_ref_serializer.is_valid():
            related_rarty_ref_obj = related_rarty_ref_serializer.save()
            return related_rarty_ref_obj
        return related_rarty_ref_obj
    
class testModelViewSet(viewsets.ModelViewSet):
    
    # post Api
    serializer_class = GeographicAddressSerializer
    queryset = (GeographicAddress.objects.all())
    
    #Post method
    def create(self, request):
        post_data = request.data
        
        geo_location = self.create_geo_location(
            post_data.get('geographicLocation',{})
        )
    
        #For save data
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        instance = serializer.save(geographic_location = geo_location)
        self.create_geographic_sub_address(
            post_data.get('geographicSubAddress',[]),instance
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED) 

            
    # Post data in GeographicAddress Model
    def create_geographic_address(self, geographic_address_info):
        geographic_address_serializer = GeographicAddressSerializer(data = geographic_address_info)
        geographic_address_obj = None
        if geographic_address_serializer.is_valid():
            geographic_address_obj = geographic_address_serializer.save()
            return geographic_address_obj
        return geographic_address_obj
    
    # Post data in RelatedGeographicLocationRefOrValue Model
    def create_geo_location(self, related_geographic_location_ref_or_value_info):
        related_geographic_location_ref_or_value_serializer = RelatedGeographicLocationRefOrValueSerializer(data=related_geographic_location_ref_or_value_info)
        related_geographic_location_ref_or_value_obj = None
        if related_geographic_location_ref_or_value_serializer.is_valid():
            related_geographic_location_ref_or_value_obj = related_geographic_location_ref_or_value_serializer.save()
            return related_geographic_location_ref_or_value_obj
        return related_geographic_location_ref_or_value_obj
    
    #  Post data in GeographicSubAddress Model
    def create_geographic_sub_address(self,geographic_sub_address_data,instance):
        geographic_sub_address_objs = []
        for geographic_sub_add in geographic_sub_address_data:
            geographic_sub_address_serializer = GeographicSubAddressSerializer(data=geographic_sub_add)
            geographic_sub_address_obj = None
            if geographic_sub_address_serializer.is_valid():
                geographic_sub_address_obj = geographic_sub_address_serializer.save(geographic_address=instance)
                return geographic_sub_address_obj
            geographic_sub_address_objs.append(geographic_sub_address_obj)
        return geographic_sub_address_obj
        
    # Get method
    def get(self):
        return self.queryset
     
class contactViewSet(viewsets.ModelViewSet):
    #  Post API
    serializer_class = ContactSerializer
    
    #Post method
    def create(self, request):
        post_data = request.data
        serializer = self.serializer_class(data=request.data)
        # import pdb;pdb.set_trace()

        self.create_contact(
            post_data.get("contact",[])
        )
        contact_medium_data = self.create_contact_medium(
            post_data.get("contactMedium",[])
        )

        if serializer.is_valid():
            serializer.save(contact_medium=contact_medium_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.data, status=status.HTTP_201_CREATED) 
    
    def create_contact(self,contact_data):
        for contact_details in contact_data:
            contact_details_serializer = ContactSerializer(data=contact_details)
            contact_details_obj = None
            if contact_details_serializer.is_valid():
                contact_details_obj = contact_details_serializer.save()
                return contact_details_obj
            return contact_details_obj
     
    def create_contact_medium(self, contact_medium_data):
        contact_medium_objs = []
        for contact_medium_datas in contact_medium_data:
            contact_medium_obj = None
            medium_characteristic_obj= self.create_characteristic(
                contact_medium_datas.get("mediumCharacteristic",{})
            )
            contact_medium_serializer = ContactMediumSerializer(data=contact_medium_datas)
            if contact_medium_serializer.is_valid():
                contact_medium_obj = contact_medium_serializer.save(contact_medium_characteristic=medium_characteristic_obj)
            contact_medium_objs.append(contact_medium_obj)
        return contact_medium_obj
     
    def create_characteristic(self, characteristic_data):
        characteristic_data_serializer = MediumCharacteristicSerializer(data=characteristic_data)
        characteristic_obj = None
        if characteristic_data_serializer.is_valid():
            characteristic_obj = characteristic_data_serializer.save()
            return characteristic_obj
        return characteristic_obj
     
def session_headers(self, request):
    correlation_id = request.META.get("HTTP_CORRELATION_ID", None)
    x_correlation_id = request.META.get("HTTP_X_CORRELATION_ID", None)
    login_name = request.META.get("HTTP_LOGIN_NAME", None)
    email = request.META.get("HTTP_EMAIL", None)
    full_name = request.META.get("HTTP_FULL_NAME", None)

    # Create json data session with the headers data
    session = {
        "attribute": {
            "additionalProp1": "String",
            "additionalProp2": "String",
            "additionalProp3": "String",
        },
        "correlationId": correlation_id,
        "xcorrelationId": x_correlation_id,
        "xCorrelationId": x_correlation_id,
        "loginName": login_name,
        "email": email,
        "fullName": full_name,
    }
    if not (correlation_id and x_correlation_id and login_name and email and full_name):
        return True

    return session     
     
# # Customer Bill Apis
class CustomerBillAPIViewset(viewsets.ModelViewSet):
    queryset = (
        CustomerBill.objects.select_related(
            'amount_due',
            'billing_account',
            'billing_period',
            'financial_account',
            'payment_method',
            'remaining_amount',
            'tax_excluded_amount',
            'tax_included_amount',
            'geographic_address',
        )
        .prefetch_related('applied_payments', 'bill_documents', 'related_parties', 'tax_items','customer_bill_contact')
        .all()
        .order_by('id')
    )
    serializer_class = CustomerBillSerializer
    http_method_names = ["post", "get", "patch", "delete","list"]
    
    def get(self):
        return self.queryset.all()

    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        amount_due = request.data.pop('amount_due', None)
        remaining_amount = request.data.pop('remaining_amount', None)
        tax_excluded_amount = request.data.pop('tax_excluded_amount', None)
        tax_included_amount = request.data.pop('tax_included_amount', None)
        billing_period = request.data.pop('billing_period', None)
        related_parties = request.data.pop('relatedParty', None)
        applied_payments = request.data.pop('appliedPayment', None)
        bill_documents = request.data.pop('billDocument', None)
        tax_items = request.data.pop('taxItem', None)

        if amount_due:
            amount_due_instance = Money.objects.create(**amount_due)
            instance.amount_due = amount_due_instance

        if remaining_amount:
            remaining_amount_instance = Money.objects.create(**remaining_amount)
            instance.remaining_amount = remaining_amount_instance

        if tax_excluded_amount:
            tax_excluded_amount_instance = Money.objects.create(**tax_excluded_amount)
            instance.tax_excluded_amount = tax_excluded_amount_instance

        if tax_included_amount:
            tax_included_amount_instance = Money.objects.create(**tax_included_amount)
            instance.tax_included_amount = tax_included_amount_instance

        if billing_period:
            billing_period_instance = TimePeriod.objects.create(**billing_period)
            instance.billing_period = billing_period_instance

        if related_parties:
            self.create_related_parties(related_parties, instance)

        if applied_payments:
            self.create_applied_payments(applied_payments, instance)

        if bill_documents:
            self.create_bill_documents(bill_documents, instance)

        if tax_items:
            self.create_tax_items(tax_items, instance)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
        
# AppliedCustomerBillingRate API
class AppliedCustomerBillingRateAPIViewset(viewsets.ModelViewSet):
    queryset = AppliedCustomerBillingRate.objects.all()
    serializer_class = AppliedCustomerBillingRateSerializer
    http_method_names = ["post", "get", "patch", "delete","list"]
    
    def get(self):
        return self.queryset.all()

# Product Offering API
class ProductOfferingAPIViewset(viewsets.ModelViewSet):
    queryset = ProductOffering.objects.all()
    serializer_class = ProductOfferingSerializer
    http_method_names = ["post", "get", "patch", "delete","list"]
    
    def get(self):
        return self.queryset.all()
    