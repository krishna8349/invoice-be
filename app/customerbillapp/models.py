from django.db import models
from .constants import BILL_STATUS_TYPE, ProductStatus, BillState,BILL_STATE_TYPE, CUSTOMER_BILL_RUN_TYPE, CustomerBillRunType

# Create your models here.

#Get api models of Customer bill resources
class BaseModel(models.Model):
    """
    Base model with baseType, type and schemaLocation. Will be inherited in all other models if required.
    """

    base_type = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    schema_location = models.CharField(max_length=100)

    class Meta:
        abstract = True


#Post Api model for Customet Bill On Demand
#Model of Billing Account Ref Table
class BillingAccountRef(BaseModel):
    """
    Billing Account Ref tabe stores the name and href of the Billing Account
    """
    # id = models.CharField(max_length=100,blank=True, primary_key=True)
    href = models.CharField(max_length=200,blank=True, null=True)
    name = models.CharField(max_length=100,blank=True, null=True)
    base_type = models.CharField(max_length=100,blank=True, null=True)
    type = models.CharField(max_length=100)
    schema_location = models.CharField(max_length=100)
    referred_type = models.CharField(max_length=100,blank=True, null=True)

    class Meta:
        verbose_name_plural = "billing_account_ref"
        db_table = "billing_account_ref"

    def __str__(self):
        return self.name

#Model of Related Party Ref Table
class RelatedPartyRef(BaseModel):
    """
    Related Party Ref Table stores the Name of the related party
    """
    customer_bill = models.ForeignKey(
        'CustomerBill', on_delete=models.SET_NULL, related_name='related_parties', blank=True, null=True
    )
    id = models.CharField(max_length=100,blank=True, primary_key=True)
    href = models.CharField(max_length=100,blank=True, null=True)
    name = models.CharField(max_length=100,blank=True, null=True)
    role = models.CharField(max_length=100,blank=True, null=True)
    base_type = models.CharField(max_length=100,blank=True, null=True)
    schema_location = models.CharField(max_length=100,blank=True, null=True)
    type = models.CharField(max_length=100,blank=True, null=True)
    referred_type = models.CharField(max_length=100,blank=True, null=True)

    class Meta:
        verbose_name_plural = "related_party_ref"
        db_table = "related_party_ref"

    def __str__(self):
        return self.name

#Model of Bill Ref Table
class BillRef(BaseModel):
    """
    Bill Ref stores the URL serving as reference for the resource
    """
    href = models.CharField(max_length=100,blank=True, null=True)
    base_type = models.CharField(max_length=100,blank=True, null=True)
    schema_location = models.CharField(max_length=100,blank=True, null=True)
    type = models.CharField(max_length=100,blank=True, null=True)
    referred_type = models.CharField(max_length=100,blank=True, null=True)

    class Meta:
        verbose_name_plural = "Bill Ref"
        db_table = "customer_bill_ref"

#Model of Customer Bill On Demand
class CustomerBillOnDemand(BaseModel):
    """
    Customer Bill On Demand Model Stores the all values given by user
    and also aad the add of Billing Account Ref model, Bill Ref model and
    Related Party Ref model as ForeignKey.
    """
    id = models.CharField(max_length=100, blank=True, primary_key=True, unique=True)
    href = models.CharField(max_length=100,blank=True, null=True)
    description = models.CharField(max_length=100,blank=True, null=True)
    lastUpdate = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    name = models.CharField(max_length=100,blank=True, null=True)
    billingAccount = models.ForeignKey(
        BillingAccountRef,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="billing_account",
    )
    customerBill = models.ForeignKey(
        BillRef,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="customer_Ref",
    )
    relatedParty = models.ForeignKey(
        RelatedPartyRef,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="related_party_ref",
    )
    state = models.CharField(
        max_length=100,
        choices=BILL_STATUS_TYPE,
        default=ProductStatus,
        blank=True,
        null=True,
    )
    base_type = models.CharField(max_length=100,blank=True, null=True)
    schema_location = models.CharField(max_length=100,blank=True, null=True)
    type = models.CharField(max_length=100,blank=True, null=True)
    referred_type = models.CharField(max_length=100,blank=True, null=True)

    def __str__(self):
        return self.name

# #Model of Money table in Customer bill resources
class Money(models.Model):
    """
    Money table to store unit(to define currency) and value of the unit
    """
    unit = models.CharField(max_length=50,blank=True, null=True)
    value = models.DecimalField(default=0, max_digits=50, decimal_places=2)
    
    class Meta:
        verbose_name_plural = "Money"
        db_table = "money"

#Model of PaymentRef in Customer bill resources
class PaymentRef(BaseModel):
    href = models.CharField(max_length=100, blank=True, null=True)
    id = models.CharField(max_length=100,blank=True,primary_key=True)
    name = models.CharField(max_length=100,blank=True, null=True)
    referred_type = models.CharField(max_length=100,blank=True, null=True)
        
    class Meta:
        verbose_name_plural = "payment_ref"
        db_table = "payment_ref"

#Model of Quantity in Customer bill resources
class Quantity(BaseModel):
    amount = models.DecimalField(default=1, max_digits=50, decimal_places=2)
    units = models.CharField(max_length=50,blank=True,null=True)
    
    class Meta:
        verbose_name_plural = "quantity"
        db_table = "quantity"

# #Model of TimePeriod in Customer bill resources
class TimePeriod(BaseModel):
    end_date_time = models.DateTimeField(blank=True,null=True)
    start_date_time = models.DateTimeField(blank=True,null=True)
    
    class Meta:
        verbose_name_plural = "time_period"
        db_table = "time_period"

#Model of AccountBalance in Customer bill resources
class AccountBalance(BaseModel):
    account_ref = models.ForeignKey(
        'FinancialAccountRef', on_delete=models.SET_NULL, related_name='account_balances', blank=True, null=True
    )
    balance_type = models.CharField(max_length=50)
    valid_for = models.ForeignKey('TimePeriod', on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.ForeignKey('Money', on_delete=models.SET_NULL, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "account_balance"
        db_table = "account_balance"

#Model of PaymentMethodRef in Customer bill resources
class PaymentMethodRef(BaseModel):
    id = models.CharField(max_length=100, blank=True, primary_key=True)
    href = models.CharField(max_length=200,blank=True, null=True)
    name = models.CharField(max_length=100,blank=True, null=True)
    referred_type = models.CharField(max_length=100,blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "payment_method_ref"
        db_table = "payment_method_ref"

#Model of Finanace Account Ref in Customer bill resources
class FinancialAccountRef(BaseModel):
    id = models.CharField(max_length=100, primary_key=True, unique=True)
    href = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    referred_type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'financial_account_ref'
        db_table = 'financial_account_ref'

    def accountBalance(self):
        return self.account_balances

# Model of contact in Customer bill resources
class Contact(models.Model):
    contact_name = models.CharField(max_length=100,blank=True, null=True)
    contact_type = models.CharField(max_length=100,blank=True, null=True)
    party_role_type = models.CharField(max_length=100,blank=True,null=True)
    valid_for = models.DateTimeField(blank=True,null=True)
    base_type = models.CharField(max_length=100,blank=True, null=True)
    schema_location = models.CharField(max_length=100,blank=True, null=True)
    type = models.CharField(max_length=100,blank=True, null=True)
    customer_bill = models.ForeignKey(
        "CustomerBill",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="customer_bill_contact"
    )

# Model of Medium Characteristic in Customer bill resources
class MediumCharacteristic(models.Model):
    city = models.CharField(max_length=100,blank=True, null=True)
    contact = models.CharField(max_length=100,blank=True,null=True)
    country = models.CharField(max_length=100,blank=True,null=True)
    email_address = models.CharField(max_length=100,blank=True,null=True)
    fax_number = models.CharField(max_length=100,blank=True,null=True)
    phone_number = models.CharField(max_length=100,blank=True,null=True)
    post_code = models.CharField(max_length=100,blank=True,null=True)
    social_network_id = models.CharField(max_length=100,blank=True,null=True)
    state_or_province = models.CharField(max_length=100,blank=True,null=True)
    street1 = models.CharField(max_length=100,blank=True,null=True)
    street2 = models.CharField(max_length=100,blank=True,null=True)
    base_type = models.CharField(max_length=100,blank=True, null=True)
    schema_location = models.CharField(max_length=100,blank=True, null=True)
    type = models.CharField(max_length=100,blank=True, null=True)
    # characteristic = models.ForeignKey(
    #     "ContactMedium",
    #     on_delete=models.SET_NULL,
    #     blank=True,
    #     null=True,
    #     related_name="characteristic"
    # )
    
    
# Model of contact medium in Customer bill resources
class ContactMedium(models.Model):
    medium_type = models.CharField(max_length=100, blank=True, null=True)
    preferred = models.BooleanField(default=False)
    valid_for = models.DateTimeField(blank=True,null=True)
    base_type = models.CharField(max_length=100,blank=True, null=True)
    schema_location = models.CharField(max_length=100,blank=True, null=True)
    type = models.CharField(max_length=100,blank=True, null=True)
    medium_characteristics = models.ForeignKey(
        MediumCharacteristic,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="medium_characteristics"
    )
    contact = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="contact_mediums"
    )
    
    
# Model of Related Geographic Location Ref or Value in Customer bill resources
class RelatedGeographicLocationRefOrValue(BaseModel):
    href = models.CharField(max_length=100,blank=True, null=True)
    name = models.CharField(max_length=100,blank=True, null=True)
    base_type = models.CharField(max_length=100,blank=True, null=True)
    schema_location = models.CharField(max_length=100,blank=True, null=True)
    type = models.CharField(max_length=100,blank=True, null=True)
    referred_type = models.CharField(max_length=100,blank=True, null=True)
    
    
# Model of Geographic Sub Address in Customer bill resources
class GeographicSubAddress(BaseModel):
    href = models.CharField(max_length=100,blank=True, null=True)
    building_name = models.CharField(max_length=100,blank=True, null=True)
    level_number = models.CharField(max_length=100,blank=True, null=True)
    level_type = models.CharField(max_length=100,blank=True, null=True)
    name = models.CharField(max_length=100,blank=True, null=True)
    private_street_name = models.CharField(max_length=100,blank=True, null=True)
    private_street_number = models.CharField(max_length=100,blank=True, null=True)
    sub_address_type = models.CharField(max_length=100,blank=True, null=True)
    sub_unit_number = models.CharField(max_length=100,blank=True,null=True)
    sub_unit_type = models.CharField(max_length=100,blank=True, null=True)
    base_type = models.CharField(max_length=100,blank=True, null=True)
    schema_location = models.CharField(max_length=100,blank=True, null=True)
    type = models.CharField(max_length=100,blank=True, null=True)
    geographic_address = models.ForeignKey(
        "GeographicAddress",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='geo_address'
    )
    
# Model of Geographic Address in Customer bill resources
class GeographicAddress(BaseModel):
    # id = models.CharField(max_length=100,primary_key=True)
    href = models.CharField(max_length=100,blank=True, null=True)
    city = models.CharField(max_length=100,blank=True, null=True)
    country = models.CharField(max_length=100,blank=True,null=True)
    locality = models.CharField(max_length=100,blank=True, null=True)
    name = models.CharField(max_length=100,blank=True, null=True)
    post_code = models.CharField(max_length=100,blank=True, null=True)
    state_on_province = models.CharField(max_length=100,blank=True, null=True)
    street_name = models.CharField(max_length=100,blank=True, null=True)
    street_nr = models.CharField(max_length=100,blank=True, null=True)
    street_nr_last = models.CharField(max_length=100,blank=True, null=True)
    street_nr_last_suffix = models.CharField(max_length=100,blank=True, null=True)
    Street_type = models.CharField(max_length=100,blank=True, null=True)
    base_type = models.CharField(max_length=100,blank=True, null=True)
    schema_location = models.CharField(max_length=100,blank=True, null=True)
    type = models.CharField(max_length=100,blank=True, null=True)
    geographic_location = models.ForeignKey(
        RelatedGeographicLocationRefOrValue,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    
#Model of BillCycleRef in Customer bill resources
class BillCycleRef(models.Model):
    href = models.CharField(max_length=100, blank=True, null=True)
    id = models.CharField(max_length=100, blank=True, primary_key=True)
    name = models.CharField(max_length=100, blank=True,null=True)
    base_type = models.CharField(max_length=100,blank=True,null=True)
    referred_type = models.CharField(max_length=100,blank=True, null=True)
    schema_location = models.CharField(max_length=100,blank=True,null=True)
    type = models.CharField(max_length=100,blank=True,null=True)
    
    class Meta:
        verbose_name_plural = "Bill Cycle Ref"
        db_table = "bill_cycle_ref"

# Model of CustomerBill in customer bill resource
class CustomerBill(BaseModel):
    href = models.CharField(max_length=100, unique=True)
    bill_date = models.DateTimeField(max_length=100, blank=True, null=True)
    bill_no = models.CharField(max_length=100,blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    last_update = models.DateTimeField(blank=True, null=True)
    next_bill_date = models.DateTimeField(blank=True,null=True)
    payment_due_date = models.DateTimeField(blank=True, null=True)
    run_type = models.CharField(
        max_length=100,
        choices=CUSTOMER_BILL_RUN_TYPE, 
        default=CustomerBillRunType,
        blank=True, 
        null=True)
    amount_due = models.ForeignKey(
        Money,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="customerbill_amountdue"
    )
    billing_account = models.ForeignKey(
        BillingAccountRef,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    billing_period = models.ForeignKey(
        TimePeriod,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    # The above code is defining a class called "financial_account".
    financial_account = models.ForeignKey(
        "FinancialAccountRef",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    payment_method = models.ForeignKey(
        PaymentMethodRef,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    remaining_amount = models.ForeignKey(
        Money,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="customerbill_remaining_amount"
    )
    state = models.CharField(
        max_length=100,
        choices=BILL_STATE_TYPE,
        default=BillState.NEW,
        blank=True,
        null=True,
    )
    geographic_address = models.ForeignKey(
        GeographicAddress,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    contacts = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    tax_excluded_amount = models.ForeignKey(
        Money,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="customerbill_tax_excluded" 
    )
    tax_included_amount = models.ForeignKey(
        Money,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="customerbill_tax_included"
    )
    
    class Meta:
        verbose_name_plural = "customer_bill"
        db_table = "customer_bill"
    
#Model of AppliedPayment in Customer bill resource
class AppliedPayment(BaseModel):
    """
    In AppliedPayment table we store Money table foreign key and PaymentRef table foreign key
    """
    customer_bill = models.ForeignKey(
        CustomerBill,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="applied_payments",
    )
    applied_amount = models.ForeignKey(
        Money,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    payment_ref = models.ForeignKey(
        PaymentRef,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    
    class Meta:
        verbose_name_plural = "applied_payment"
        db_table = "applied_payment"

#Model of AttachmentRefOnValue in Customer bill resources
class AttachmentRefOrValue(BaseModel):
    customer_bill = models.ForeignKey(
        CustomerBill,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="bill_documents"
    )
    href = models.CharField(max_length=100, blank=True, null=True)
    attachment_type = models.CharField(max_length=100, blank=True, null=True)
    content = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True,null=True)
    mime_type = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100,blank=True, null=True)
    url = models.CharField(max_length=100,blank=True,null=True)
    size = models.ForeignKey(
        Quantity,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    valid_for = models.ForeignKey(
        TimePeriod,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    referred_type = models.CharField(max_length=100,blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "attachment_ref_or_value"
        db_table = "attachment_ref_or_value"

#Model of TaxItem in Customer bill resources
class TaxItem(BaseModel):
    customer_bill = models.ForeignKey(
        CustomerBill,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="tax_items",
    )
    tax_category = models.CharField(max_length=100,blank=True,null=True)
    tax_rate = models.DecimalField(max_digits=50,decimal_places=2)
    tax_amount = models.ForeignKey(
        Money,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
        
    class Meta:
        verbose_name_plural = "Tax Item"
        db_table = "tax_item"

# # Model of Characteristic in Customer Bill
class Characteristic(models.Model):
    characteristicRelationship = models.ForeignKey(
        "AppliedCustomerBillingRateCharacteristic",
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        related_name='character'
    )
    relationship_type = models.CharField(max_length=100,blank=True, null=True)

    class Meta:
        verbose_name_plural = "Characteristics"
        db_table = "characteristics"

# Models for Applied Customer Billing Rate
# Model of Applied Biling Tax Rate in Applied Customer Billing Rate
class AppliedBillingTaxRate(models.Model):
    tax_category = models.CharField(max_length=100,blank=True,null=True)
    tax_rate = models.IntegerField()
    tax_amount = models.ForeignKey(
        Money,
            on_delete=models.SET_NULL,
            blank=True,
            null=True,
    )
    appliedCustomerBillingRate = models.ForeignKey(
            "AppliedCustomerBillingRate",
            on_delete=models.SET_NULL,
            blank=True,
            null=True,
            related_name="applied_customer_billing_tax_rate"
    )

# # Model of Applied Customer Billing Rate Characteristic in Applied Customer Bill Rate
class AppliedCustomerBillingRateCharacteristic(models.Model):
    appliedCustomerBillingRate = models.ForeignKey(
        "AppliedCustomerBillingRate",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="applied_customer_billing_rate_characteristic"
    )
    name = models.CharField(max_length=100, blank=True, null=True)
    value_type = models.CharField(max_length=100, blank=True,null=True)
    value = models.CharField(max_length=100, blank=True,null=True)
    
# # Model of Product Ref in Applied Biling Tax Rate
class ProductRef(models.Model):
    href = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    referred_type = models.CharField(max_length=100,blank=True,null=True)

# # Applied Customer Billing Rate Model
class AppliedCustomerBillingRate(models.Model):
    href = models.CharField(max_length=100,blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=100,blank=True, null=True)
    is_billed = models.BooleanField(default=False)
    name = models.CharField(max_length=100,blank=True,null=True)
    type = models.CharField(max_length=100,blank=True,null=True)
    bill = models.ForeignKey(
        BillRef,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    billing_account = models.ForeignKey(
        BillingAccountRef,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    period_coverage = models.ForeignKey(
        TimePeriod,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    product = models.ForeignKey(
        ProductRef,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    tax_excluded_amount = models.ForeignKey(
        Money,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="customer_bill_rate_tax_money" 
    )
    tax_included_amount = models.ForeignKey(
        Money,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="customer_bill_rate_tax_included_amount_money"
    )
    characteristic = models.ForeignKey(
        AppliedCustomerBillingRateCharacteristic,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

# Cateloge Models
class ProductOffering(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    href = models.CharField(max_length=255,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_bundle = models.BooleanField(blank=True, null=True)
    is_sellable = models.BooleanField(blank=True, null=True)
    last_update = models.DateTimeField(auto_now_add=True)
    life_cycle_status = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255,blank=True, null=True)
    status_reason = models.CharField(max_length=255,blank=True, null=True)
    version = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=255,blank=True, null=True)
    agreement = models.CharField(max_length=255,blank=True, null=True)
    attachment = models.CharField(max_length=255,blank=True, null=True)
    bundled_product_offering = models.CharField(max_length=255,blank=True, null=True)
    category = models.CharField(max_length=255,blank=True, null=True)
    channel = models.CharField(max_length=255,blank=True, null=True)
    market_segment = models.CharField(max_length=255,blank=True, null=True)
    place = models.CharField(max_length=255,blank=True, null=True)
    prod_specchar_value_use = models.CharField(max_length=255,blank=True, null=True)
    product_offering_relationship = models.CharField(max_length=255,blank=True, null=True)
    product_specification = models.CharField(max_length=255,blank=True, null=True)
    resource_candidate = models.CharField(max_length=255,blank=True, null=True)
    service_candidate = models.CharField(max_length=255,blank=True, null=True)
    service_level_agreement = models.CharField(max_length=255,blank=True, null=True)
    valid_for = models.CharField(max_length=255,blank=True, null=True)
    product_offering_price = models.ForeignKey(
        "ProductOfferingPrice", 
        on_delete=models.CASCADE,
        blank=True, 
        null=True
    )
    product_offering_price_tax = models.ForeignKey(
        "ProductOfferingPriceTax", 
        on_delete=models.CASCADE,
        blank=True, 
        null=True
    )
    tax_master = models.ForeignKey(
        "TaxMaster", 
        on_delete=models.CASCADE,
        blank=True, 
        null=True
    )

    class Meta:
        verbose_name_plural = "Product Offering"
        db_table = "product_offering"

class ProductOfferingPrice(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    href = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    is_bundle = models.BooleanField(blank=True, null=True)
    last_update = models.DateTimeField(auto_now_add=True)
    life_cycle_status = models.CharField(max_length=255,blank=True, null=True)
    name = models.CharField(max_length=255,blank=True, null=True)
    percentage = models.FloatField()
    price_type = models.CharField(max_length=255,blank=True, null=True)
    recurring_charge_period_length = models.CharField(max_length=255,blank=True, null=True)
    recurring_charge_period_type = models.CharField(max_length=255,blank=True, null=True)
    version = models.IntegerField(blank=True, null=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)
    type = models.CharField(max_length=255,blank=True, null=True)
    bundle_pop_relationship = models.CharField(max_length=255,blank=True, null=True)
    constraint = models.CharField(max_length=255, blank=True, null=True)
    place = models.CharField(max_length=255,blank=True, null=True)
    pop_relationship = models.CharField(max_length=255,blank=True, null=True)
    price = models.CharField(max_length=255,blank=True, null=True)
    pricing_logic_algorithm = models.CharField(max_length=255,blank=True, null=True)
    prod_specchar_value_use = models.CharField(max_length=255,blank=True, null=True)
    product_offering_term = models.CharField(max_length=255,blank=True, null=True)
    unit_of_measure = models.CharField(max_length=255,blank=True, null=True)
    valid_for = models.CharField(max_length=255,blank=True, null=True)

    class Meta:
        verbose_name_plural = "Product Offering Price"
        db_table = "product_offering_pice"

class ProductOfferingPriceTax(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    href = models.CharField(max_length=255,blank=True, null=True)
    tax_category = models.CharField(max_length=255)
    tax_rate = models.FloatField()
    tax_amount = models.FloatField(blank=True, null=True)
    type = models.CharField(max_length=255,blank=True, null=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()

    class Meta:
        verbose_name_plural = "Product Offering Price Tax"
        db_table = "product_offering_pice_tax"

class TaxMaster(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    tax_category = models.CharField(max_length=255)
    tax_rate = models.FloatField()
    tax_description = models.TextField(blank=True, null=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Tax Master"
        db_table = "tax_master"