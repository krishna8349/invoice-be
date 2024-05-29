from rest_framework import serializers
from rest_framework.validators import UniqueValidator
import re

from app.customerbillapp.models import (
    CustomerBillOnDemand,
    BillingAccountRef,
    BillRef, 
    RelatedPartyRef, 
    Money,
    PaymentRef,
    AppliedPayment,
    Quantity,
    TimePeriod,
    AttachmentRefOrValue,
    AccountBalance,
    FinancialAccountRef,
    PaymentMethodRef,
    TaxItem,
    BaseModel,
    CustomerBill,
    Contact,
    ContactMedium, 
    MediumCharacteristic, 
    GeographicAddress, 
    GeographicSubAddress,
    RelatedGeographicLocationRefOrValue, 
    BillCycleRef,
    Characteristic,
    AppliedCustomerBillingRate, 
    AppliedBillingTaxRate, 
    AppliedCustomerBillingRateCharacteristic, 
    ProductRef,
    ProductOffering,
    ProductOfferingPrice,
    ProductOfferingPriceTax,
    TaxMaster
    )
# from app.customerbillapp.models import *

word_regex = re.compile(r'[a-zA-Z]+')

class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseModel
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["@baseType"] = serializers.CharField(source="base_type", required=False)
        self.fields["@type"] = serializers.CharField(source="type", required=False)
        self.fields["@schemaLocation"] = serializers.CharField(source="schema_location", required=False)


class BillingAccountRefSerializer(BaseModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["@referredType"] = serializers.CharField(source='referred_type', required=False) 
        
    class Meta:
        model = BillingAccountRef
        fields =('id','href','name')

class BillRefSerializer(BaseModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["@referredType"] = serializers.CharField(source='referred_type', required=False)

    class Meta:
        model = BillRef
        fields =('id','href')

class RelatedPartyRefSerializer(BaseModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["@referredType"] = serializers.CharField(source='referred_type', required=False)     
    
    class Meta:
        model = RelatedPartyRef
        fields = ('id', 'href', 'name','role')

class CustomerBillOnDemandSerilizer(BaseModelSerializer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["@referredType"] = serializers.CharField(source='referred_type', required=False)   
        
    billingAccount = BillingAccountRefSerializer(read_only=True)
    customerBill = BillRefSerializer(read_only=True)
    relatedParty = RelatedPartyRefSerializer(read_only=True)
    class Meta:
        model = CustomerBillOnDemand
        fields =('id','href','description','lastUpdate','name','billingAccount','customerBill','relatedParty','state')

class MediumCharacteristicSerializer(BaseModelSerializer):
    emailAddress = serializers.CharField(source="email_address", required=False)
    faxNumber = serializers.CharField(source="fax_number", required=False)
    phoneNumber = serializers.CharField(source="phone_number", required=False)
    postCode = serializers.CharField(source="post_code", required=False)
    socialNetworkId = serializers.CharField(source="social_network_id", required=False)
    stateOrProvince = serializers.CharField(source="state_or_province", required=False)
    
    class Meta:
        model = MediumCharacteristic
        fields =('city','contact','country','emailAddress','faxNumber','phoneNumber','postCode','socialNetworkId','stateOrProvince','street1','street2')
        
class ContactMediumSerializer(BaseModelSerializer):
    mediumCharacteristic = MediumCharacteristicSerializer(read_only=True, many=False, source="medium_characteristics", required=False)
    mediumType = serializers.CharField(source="medium_type", required=False)
    validFor = serializers.CharField(source="valid_for", required=False)
    
    class Meta:
        model = ContactMedium
        fields =('mediumType','preferred','validFor','mediumCharacteristic')

class ContactSerializer(BaseModelSerializer):
    contactMedium = ContactMediumSerializer(read_only=True, many=True, source="contact_mediums", required=False)
    contactName = serializers.CharField(read_only=True,source="contact_name", required=False)
    contactType = serializers.CharField(read_only=True,source="contact_type", required=False)
    partyRoleType = serializers.CharField(read_only=True,source="party_role_type", required=False)
    validFor = serializers.CharField(read_only=True,source="valid_for", required=False)
    
    class Meta:
        model = Contact
        fields = ('contactName','contactType','partyRoleType','validFor','contactMedium')
        
class RelatedGeographicLocationRefOrValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedGeographicLocationRefOrValue
        fields = ('id','href','name')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["@baseType"] = serializers.CharField(source="base_type", required=False)
        self.fields["@schemaLocation"] = serializers.CharField(source="schema_location", required=False)
        self.fields["@type"] = serializers.CharField(source="type", required=False)
        self.fields["@referredType"] = serializers.CharField(source="referred_type", required=False)
        

class GeographicSubAddressSerializer(serializers.ModelSerializer):
    # Renaming Fields according to tha requirement of tmforum
    buildingName = serializers.CharField(source="building_name", required=False)
    levelNumber = serializers.CharField(source="level_number", required=False)
    levelType = serializers.CharField(source="level_type", required=False)
    privateStreetName = serializers.CharField(source="private_street_name", required=False)
    privateStreetNumber = serializers.CharField(source="private_street_number", required=False)
    subAddressType = serializers.CharField(source="sub_address_type", required=False)
    subUnitNumber = serializers.CharField(source="sub_unit_number", required=False)
    subUnitType = serializers.CharField(source="sub_unit_type", required=False)

    # Add @ in the Fileds 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["@baseType"] = serializers.CharField(source="base_type", required=False)
        self.fields["@schemaLocation"] = serializers.CharField(source="schema_location", required=False)
        self.fields["@type"] = serializers.CharField(source="type", required=False)

    class Meta:
        model = GeographicSubAddress
        fields = ('id','href','buildingName','levelNumber','levelType','name','privateStreetName','privateStreetNumber','subAddressType','subUnitNumber','subUnitType')
        
class GeographicAddressSerializer(serializers.ModelSerializer):
    
    geographicLocation = RelatedGeographicLocationRefOrValueSerializer(many=False, read_only=False, source="geographic_location",required=False)
    geographicSubAddress = GeographicSubAddressSerializer(many=True, source='geo_address')

    # Renaming Fields according to tha requirement of tmforum
    postCode = serializers.CharField(source="post_code", required=False)
    stateOnProvince = serializers.CharField(source="state_on_province", required=False)
    streetName = serializers.CharField(source="street_name", required=False)
    streetNr = serializers.CharField(source="street_nr", required=False)
    streetNrLast = serializers.CharField(source="street_nr_last", required=False)
    streetNrLastSuffix = serializers.CharField(source="street_nr_last_suffix", required=False)
    streetType = serializers.CharField(source="Street_type", required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["@baseType"] = serializers.CharField(source="base_type", required=False)
        self.fields["@schemaLocation"] = serializers.CharField(source="schema_location", required=False)
        self.fields["@type"] = serializers.CharField(source="type", required=False)
    
    class Meta:
        model = GeographicAddress
        fields = ('id','href','city','country','locality','name','postCode','stateOnProvince','streetName','streetNr','streetNrLast','streetNrLastSuffix','streetType',"geographicLocation","geographicSubAddress")

            
class BillCycleRefSerializer(serializers.ModelSerializer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["@baseType"] = serializers.CharField(source="base_type", required=False)
        self.fields["@schemaLocation"] = serializers.CharField(source="schema_location", required=False)
        self.fields["@type"] = serializers.CharField(source="type", required=False)
        self.fields["@referredType"] = serializers.CharField(source="referredType", required=False)
        
    class Meta:
        model = BillCycleRef
        fields = ('id','name','name')
        
class CharacteristicSerializer(serializers.ModelSerializer):
    valueType = serializers.CharField(source="value_type", required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["@baseType"] = serializers.CharField(source="base_type", required=False)
        self.fields["@schemaLocation"] = serializers.CharField(source="schema_location", required=False)
        self.fields["@type"] = serializers.CharField(source="type", required=False)
        
    class Meta:
        model = Characteristic
        fields = ('id','name','valueType','value')

class MoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Money
        exclude = ['id']


class PaymentRefSerializer(BaseModelSerializer):
    class Meta:
        model = PaymentRef
        exclude = ['type', 'base_type', 'schema_location', 'referred_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["@referredType"] = serializers.CharField(source='referred_type', required=False)


class AppliedPaymentSerializer(BaseModelSerializer):
    appliedAmount = MoneySerializer(
        many=False, read_only=False, required=False, allow_null=True, source='applied_amount'
    )
    payment = PaymentRefSerializer(many=False, read_only=False, required=False, allow_null=True, source='payment_ref')

    class Meta:
        model = AppliedPayment
        exclude = ['id', 'type', 'base_type', 'schema_location', 'customer_bill', 'applied_amount','payment_ref']


class QuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Quantity
        fields = ['amount', 'units']


class TimePeriodSerializer(serializers.ModelSerializer):
    endDateTime = serializers.DateTimeField(source='end_date_time', allow_null=True, required=False)
    startDateTime = serializers.DateTimeField(source='start_date_time', allow_null=True, required=False)

    class Meta:
        model = TimePeriod
        fields = ['endDateTime', 'startDateTime']


class AttachmentRefOrValueSerializer(BaseModelSerializer):
    id = serializers.CharField(required=False)
    size = QuantitySerializer(many=False, read_only=False, required=False, allow_null=True)
    validFor = TimePeriodSerializer(many=False, read_only=False, required=False, allow_null=True, source='valid_for')
    attachmentType = serializers.CharField(source='attachment_type', required=False)
    mimeType = serializers.CharField(source='mime_type', required=False)

    class Meta:
        model = AttachmentRefOrValue
        exclude = [
            'type',
            'base_type',
            'schema_location',
            'referred_type',
            'customer_bill',
            'attachment_type',
            'mime_type',
            'valid_for',
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["@referredType"] = serializers.CharField(source='referred_type', required=False)


class BillingAccountRefSerializer(BaseModelSerializer):
    class Meta:
        model = BillingAccountRef
        fields = ['id', 'href', 'name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["@referredType"] = serializers.CharField(source='referred_type', required=False)


class AccountBalanceSerializer(BaseModelSerializer):
    amount = MoneySerializer(many=False, read_only=False, required=False, allow_null=True)
    validFor = TimePeriodSerializer(many=False, read_only=False, required=False, allow_null=True, source='valid_for')
    balanceType = serializers.CharField(source='balance_type', required=False)

    class Meta:
        model = AccountBalance
        fields = ['balanceType', 'amount', 'validFor']


class FinancialAccountRefSerializer(BaseModelSerializer):
    accountBalance = AccountBalanceSerializer(many=True)

    class Meta:
        model = FinancialAccountRef
        fields = ['id', 'href', 'name', 'accountBalance']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["@referredType"] = serializers.CharField(source='referred_type', required=False)


class PaymentMethodRefSerializer(BaseModelSerializer):
    class Meta:
        model = PaymentMethodRef
        fields = ['id', 'href', 'name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["@referredType"] = serializers.CharField(source='referred_type', required=False)

class TaxItemSerializer(BaseModelSerializer):
    taxCategory = serializers.CharField(source='tax_category', allow_null=True, required=False)
    taxAmount = MoneySerializer(allow_null=True, many=False, read_only=False, required=False, source='tax_amount')
    taxRate = serializers.DecimalField(max_digits=50, decimal_places=2, source='tax_rate')

    class Meta:
        model = TaxItem
        fields = ['taxCategory', 'taxRate', 'taxAmount']

class CustomerBillSerializer(BaseModelSerializer):
    id = serializers.CharField(required=False)
    billDate = serializers.DateTimeField(source='bill_date', allow_null=True, required=False)
    billNo = serializers.CharField(source='bill_no', required=False)
    lastUpdate = serializers.DateTimeField(source='last_update', allow_null=True, required=False)
    nextBillDate = serializers.DateTimeField(source='next_bill_date', allow_null=True, required=False)
    paymentDueDate = serializers.DateTimeField(source='payment_due_date', allow_null=True, required=False)
    runType = serializers.CharField(source='run_type', required=False)
    amountDue = MoneySerializer(many=False, read_only=False, required=False, allow_null=True, source='amount_due')
    remainingAmount = MoneySerializer(
        many=False, read_only=False, required=False, allow_null=True, source='remaining_amount'
    )
    taxExcludedAmount = MoneySerializer(many=False, read_only=True, source='tax_excluded_amount')
    taxIncludedAmount = MoneySerializer(many=False, read_only=True, source='tax_included_amount')
    appliedPayment = AppliedPaymentSerializer(many=True, source = "applied_payments")
    billDocument = AttachmentRefOrValueSerializer(many=True, source = "bill_documents")
    billingAccount = BillingAccountRefSerializer(many=False, read_only=True, source='billing_account')
    billingPeriod = TimePeriodSerializer(many=False, read_only=True, source='billing_period')
    financialAccount = FinancialAccountRefSerializer(many=False, read_only=True, source='financial_account')
    paymentMethod = PaymentMethodRefSerializer(many=False, read_only=True, source='payment_method')
    geographicAddress = GeographicAddressSerializer(many=False, read_only=True, source='geographic_address')
    contacts = ContactSerializer(many=True, read_only=True, source='customer_bill_contact')
    relatedParty = RelatedPartyRefSerializer(many=True, source = "related_parties")
    taxItem = TaxItemSerializer(many=True, source = "tax_items")

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = None
        try:
            field_queries = kwargs['context']['request'].query_params.get('fields')
            fields = word_regex.findall(field_queries)
        except Exception:
            pass

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def update(self, instance, validated_data):
        amount_due_data = validated_data.pop('amount_due', None)
        remaining_amount_data = validated_data.pop('remaining_amount', None)
        tax_excluded_amount_data = validated_data.pop('tax_excluded_amount', None)
        tax_included_amount_data = validated_data.pop('tax_included_amount', None)
        billing_period_data = validated_data.pop('billing_period', None)
        related_parties_data = validated_data.pop('related_parties', None)
        applied_payments_data = validated_data.pop('applied_payments', None)
        bill_documents_data = validated_data.pop('bill_documents', None)
        tax_items_data = validated_data.pop('tax_items', None)

        # Update the instance fields
        instance = super().update(instance, validated_data)

        # Update the nested fields
        if amount_due_data:
            amount_due_instance = instance.amount_due
            for field, value in amount_due_data.items():
                setattr(amount_due_instance, field, value)
            amount_due_instance.save()

        if remaining_amount_data:
            remaining_amount_instance = instance.remaining_amount
            for field, value in remaining_amount_data.items():
                setattr(remaining_amount_instance, field, value)
            remaining_amount_instance.save()

        if tax_excluded_amount_data:
            tax_excluded_amount_instance = instance.tax_excluded_amount
            for field, value in tax_excluded_amount_data.items():
                setattr(tax_excluded_amount_instance, field, value)
            tax_excluded_amount_instance.save()

        if tax_included_amount_data:
            tax_included_amount_instance = instance.tax_included_amount
            for field, value in tax_included_amount_data.items():
                setattr(tax_included_amount_instance, field, value)
            tax_included_amount_instance.save()

        if billing_period_data:
            billing_period_instance = instance.billing_period
            for field, value in billing_period_data.items():
                setattr(billing_period_instance, field, value)
            billing_period_instance.save()

        if related_parties_data:
            self.update_nested_related_parties(instance, related_parties_data)

        if applied_payments_data:
            self.update_nested_applied_payments(instance, applied_payments_data)

        if bill_documents_data:
            self.update_nested_bill_documents(instance, bill_documents_data)

        if tax_items_data:
            self.update_nested_tax_items(instance, tax_items_data)

        return instance

    def update_nested_related_parties(self, instance, related_parties_data):
        pass

    def update_nested_applied_payments(self, instance, applied_payments_data):
        pass

    def update_nested_bill_documents(self, instance, bill_documents_data):
        pass

    def update_nested_tax_items(self, instance, tax_items_data):
        pass

    class Meta:
        model = CustomerBill
        fields = [
            'id',
            'href',
            'billDate',
            'billNo',
            'category',
            'lastUpdate',
            'nextBillDate',
            'paymentDueDate',
            'runType',
            'amountDue',
            'appliedPayment',
            'billDocument',
            'billingAccount',
            'billingPeriod',
            'financialAccount',
            'paymentMethod',
            'geographicAddress',
            'contacts',
            'relatedParty',
            'remainingAmount',
            'state',
            'taxExcludedAmount',
            'taxIncludedAmount',
            'taxItem',
        ]

# AppliedCustomerBillingRate Serilizer
class ProductRefSerializer(BaseModelSerializer):
    class Meta:
        model = ProductRef
        fields = ['href', 'name']

class AppliedBillingTaxRateSerializer(BaseModelSerializer):
    taxAmount = MoneySerializer(
        many=False, read_only=False, required=False, source="tax_amount"
    )

    class Meta:
        model = AppliedBillingTaxRate
        fields = ['tax_category', 'tax_rate', 'taxAmount']

class AppliedCustomerBillingRateCharacteristicSerializer(BaseModelSerializer):
    
    class Meta:
        model = AppliedCustomerBillingRateCharacteristic
        fields = ['name', 'value_type', 'value']

class AppliedCustomerBillingRateSerializer(BaseModelSerializer):
    appliedTax = AppliedBillingTaxRateSerializer(
        many=True, read_only=False, required=False, allow_null=True,source="applied_customer_billing_tax_rate"
    )
    bill = BillRefSerializer(
        many=False, read_only=False, required=False
    )
    billingAccount = BillingAccountRefSerializer(
        many=False, read_only=False, required=False, source="billing_account"
    )
    characteristic = AppliedCustomerBillingRateCharacteristicSerializer(
        many=True, read_only=False, required=False, source="applied_customer_billing_rate_characteristic"
    )
    periodCoverage = TimePeriodSerializer(
        many=False, read_only=False, required=False, source="period_coverage"
    )
    product = ProductRefSerializer(
        many=False, read_only=False, required=False
    )
    taxExcludedAmount = MoneySerializer(
        many=False, read_only=False, required=False,source="tax_excluded_amount"
    )
    taxIncludedAmount = MoneySerializer(
        many=False, read_only=False, required=False,source="tax_included_amount"
    )

    class Meta:
        model = AppliedCustomerBillingRate
        fields = [
            'id',
            'href',
            'date',
            'description',
            'is_billed',
            'name',
            'type',
            'appliedTax',
            'bill',
            'billingAccount',
            'characteristic',
            'periodCoverage',
            'product',
            'taxExcludedAmount',
            'taxIncludedAmount'
            ]


class ProductOfferingPriceSerializer(serializers.ModelSerializer):
    isBundle = serializers.CharField(source='is_bundle', required=False)
    lastUpdate = serializers.CharField(source='last_update', required=False)
    lifeCycleStatus = serializers.CharField(source='life_cycle_status', required=False)
    priceType = serializers.CharField(source='price_type', required=False)
    recurringChargePeriodLength = serializers.CharField(source='recurring_charge_period_length', required=False)
    recurringChargePeriodType = serializers.CharField(source='recurring_charge_period_type', required=False)
    startDate = serializers.DateTimeField(source='start_date', required=False)
    endDate = serializers.DateTimeField(source='end_date', required=False)
    bundlePopRelationship = serializers.CharField(source='bundle_pop_relationship', required=False)
    popRelationship = serializers.CharField(source='pop_relationship', required=False)
    pricingLogicAlgorithm = serializers.CharField(source='pricing_logic_algorithm', required=False)
    prodSpeccharValueUse = serializers.CharField(source='prod_specchar_value_use', required=False)
    productOfferingTerm = serializers.CharField(source='product_offering_term', required=False)
    unitOfMeasure = serializers.CharField(source='unit_of_measure', required=False)
    validFor = serializers.CharField(source='valid_for', required=False)

    class Meta:
        model = ProductOfferingPrice
        fields = [
            'id',
            'href',
            'description',
            'isBundle',
            'lastUpdate',
            'lifeCycleStatus',
            'name',
            'percentage',
            'priceType',
            'recurringChargePeriodLength',
            'recurringChargePeriodType',
            'version',
            'startDate',
            'endDate',
            'type',
            'bundlePopRelationship',
            'constraint',
            'place',
            'popRelationship',
            'price',
            'pricingLogicAlgorithm',
            'prodSpeccharValueUse',
            'productOfferingTerm',
            'unitOfMeasure',
            'validFor'
        ]

class ProductOfferingPriceTaxSerializer(serializers.ModelSerializer):
    taxcategory = serializers.CharField(source='tax_category', required=False)
    taxRate = serializers.DecimalField(source='tax_rate', required=False,max_digits=50, decimal_places=2)
    taxAmount = serializers.IntegerField(source='tax_amount', required=False)
    startDate = serializers.DateTimeField(source='start_date', required=False)
    endDate = serializers.DateTimeField(source='end_date', required=False)

    class Meta:
        model = ProductOfferingPriceTax
        fields = [
            'id',
            'href',
            'taxcategory',
            'taxRate',
            'taxAmount',
            'type',
            'startDate',
            'endDate',
        ]

class TaxMasterSerializer(serializers.ModelSerializer):
    taxcategory = serializers.CharField(source='tax_category', required=False)
    taxRate = serializers.DecimalField(source='tax_rate', required=False,max_digits=50, decimal_places=2)
    taxDescription = serializers.CharField(source='tax_description', required=False)
    startDate = serializers.DateTimeField(source='start_date', required=False)
    endDate = serializers.DateTimeField(source='end_date', required=False)

    class Meta:
        model = TaxMaster
        fields = [
            'id',
            'taxcategory',
            'taxRate',
            'taxDescription',
            'startDate',
            'endDate',
        ]

class ProductOfferingSerializer(serializers.ModelSerializer):
    isBundle = serializers.CharField(source='is_bundle', required=False)
    isSellable = serializers.CharField(source='is_sellable', required=False)
    lastUpdate = serializers.DateTimeField(source='last_update', required=False)
    lifeCycleStatus = serializers.CharField(source='life_cycle_status', required=False)
    statusReason = serializers.CharField(source='status_reason', required=False)
    bundledProductOffering = serializers.CharField(source='bundled_product_offering', required=False)
    marketSegment = serializers.CharField(source='market_segment', required=False)
    prodSpeccharValueUse = serializers.CharField(source='prod_specchar_value_use', required=False)
    productOfferingRelationship = serializers.CharField(source='product_offering_relationship', required=False)
    productSpecification = serializers.CharField(source='product_specification', required=False)
    resourceCandidate = serializers.CharField(source='resource_candidate', required=False)
    serviceCandidate = serializers.CharField(source='service_candidate', required=False)
    serviceLevelAgreement = serializers.CharField(source='service_level_agreement', required=False)
    validFor = serializers.CharField(source='valid_for', required=False)
    productOfferingPrice = ProductOfferingPriceSerializer(
        source='product_offering_price', many=False, read_only=False, required=False)
    productOfferingPriceTax = ProductOfferingPriceTaxSerializer(
        source='product_offering_price_tax', many=False, read_only=False, required=False
    )
    taxMaster = TaxMasterSerializer(
        many=False, read_only=True, required=False, source='tax_master'
    )

    class Meta:
        model = ProductOffering
        fields = [
            'id',
            'href',
            'description',
            'isBundle',
            'isSellable',
            'lastUpdate',
            'lifeCycleStatus',
            'name',
            'statusReason',
            'version',
            'type',
            'agreement',
            'attachment',
            'bundledProductOffering',
            'category',
            'channel',
            'marketSegment',
            'place',
            'prodSpeccharValueUse',
            'productOfferingRelationship',
            'productSpecification',
            'resourceCandidate',
            'serviceCandidate',
            'serviceLevelAgreement',
            'validFor',
            'productOfferingPrice',
            'productOfferingPriceTax',
            'taxMaster'
        ]