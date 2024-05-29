from enum import Enum
from django.utils.translation import gettext_lazy as _

class StrEnum(str, Enum):
    """Enum where members are also (and must be) strs"""

    def __str__(self):
        return self.value

class ProductStatus(StrEnum):
    """Product Status"""

    INPROGRESS = _("in_progress")
    REJECTED = _("rejected")
    DONE = _("done")
    TERMINATEDWITHERROR = _("terminated with error")

BILL_STATUS_TYPE = (
    (ProductStatus.INPROGRESS, "in_progress"),
    (ProductStatus.REJECTED, "rejected"),
    (ProductStatus.DONE, "done"),
    (ProductStatus.TERMINATEDWITHERROR, "terminated_with_error"),
)

class BillState(StrEnum):
    """Bill Status"""

    NEW = _("new")
    ONHOLD = _("on_Hold")
    VALIDATED = _("validated")
    SENT = _("sent")
    PARTIALLYPAID = _("partially_paid")
    SETTLED = _("settled")

BILL_STATE_TYPE = (
    (BillState.NEW, "new"),
    (BillState.ONHOLD ,"on_Hold"),
    (BillState.VALIDATED , "validated"),
    (BillState.SENT ,"sent"),
    (BillState.PARTIALLYPAID ,"partially_paid"),
    (BillState.SETTLED, "settled")
)

class CustomerBillRunType(StrEnum):
    """Customer Bill run time"""

    ON_CYCLE = "onCycle"
    OFF_CYCLE = "offCycle"

CUSTOMER_BILL_RUN_TYPE = (
    (CustomerBillRunType.ON_CYCLE, "On Cycle"),
    (CustomerBillRunType.OFF_CYCLE, "Off Cycle")
)