from src.domain.errors import CloningProfileWithRecurringTimeEntries, CloningProfileWithRecurringExpenses
from src.domain.model import InvoiceProfile, InvoiceProfileLineType


def copy_profile(profile: InvoiceProfile):
    profile_item_types = set(line.type for line in profile.lines)

    if InvoiceProfileLineType.UnbilledTimeEntry.value in profile_item_types:
        raise CloningProfileWithRecurringTimeEntries()

    if InvoiceProfileLineType.UnbilledExpense.value in profile_item_types:
        raise CloningProfileWithRecurringExpenses()

    return InvoiceProfile(profile.lines, profile.client_id, None)
