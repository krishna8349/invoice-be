from django.urls import include, path,re_path
from rest_framework import routers
from .views import (
    CustomerBillOnDemandViewSet,
    testModelViewSet,
    contactViewSet,
    CustomerBillAPIViewset, 
    AppliedCustomerBillingRateAPIViewset,
    ProductOfferingAPIViewset
)

class OptionalSlashRouter(routers.SimpleRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'

router = OptionalSlashRouter()

router.register(r"api/customerBillOnDemand",CustomerBillOnDemandViewSet, basename="customer_bill_on_demand")
router.register(r"api/address",testModelViewSet, basename="address")
router.register(r"api/contact",contactViewSet, basename="contact")
router.register(r"api/customerBill",CustomerBillAPIViewset, basename="customer_bills")
router.register(r"api/appliedCustomerBillingRate",AppliedCustomerBillingRateAPIViewset, basename="applied_customer_billing_rate")
router.register(r"api/productOffering", ProductOfferingAPIViewset, basename="prroduct_offering")

urlpatterns1 = []
urlpatterns1 += router.urls

urlpatterns = urlpatterns1 + [
    
]