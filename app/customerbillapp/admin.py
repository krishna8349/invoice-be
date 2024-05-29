from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import (
    AccountBalance,
    AppliedPayment,
    AttachmentRefOrValue,
    BillingAccountRef,
    CustomerBill,
    FinancialAccountRef,
    Money,
    PaymentMethodRef,
    PaymentRef,
    Quantity,
    RelatedPartyRef,
    TaxItem,
    TimePeriod,
    GeographicAddress,
    GeographicSubAddress,
    RelatedGeographicLocationRefOrValue,
    Contact,
    ContactMedium,
    MediumCharacteristic,
    
    AppliedBillingTaxRate,
    AppliedCustomerBillingRateCharacteristic,
    ProductRef,
    AppliedCustomerBillingRate,
    BillRef,

    ProductOffering,
    ProductOfferingPrice,
    ProductOfferingPriceTax,
    TaxMaster
)

admin.site.register(CustomerBill)
admin.site.register(Money)
admin.site.register(AppliedPayment)
admin.site.register(AttachmentRefOrValue)
admin.site.register(BillingAccountRef)
admin.site.register(TimePeriod)
admin.site.register(FinancialAccountRef)
admin.site.register(PaymentMethodRef)
admin.site.register(PaymentRef)
admin.site.register(TaxItem)
admin.site.register(Quantity)
admin.site.register(AccountBalance)
admin.site.register(RelatedPartyRef)
admin.site.register(GeographicAddress)
admin.site.register(GeographicSubAddress)
admin.site.register(RelatedGeographicLocationRefOrValue)
admin.site.register(Contact)
admin.site.register(ContactMedium)
admin.site.register(MediumCharacteristic)

admin.site.register(AppliedBillingTaxRate)
admin.site.register(AppliedCustomerBillingRateCharacteristic)
admin.site.register(ProductRef)
admin.site.register(AppliedCustomerBillingRate)
admin.site.register(BillRef)

admin.site.register(ProductOffering)
admin.site.register(ProductOfferingPrice)
admin.site.register(ProductOfferingPriceTax)
admin.site.register(TaxMaster)
