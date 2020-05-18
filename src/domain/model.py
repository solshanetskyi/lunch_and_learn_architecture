from dataclasses import dataclass
from datetime import timedelta
from decimal import Decimal
from enum import Enum
from typing import Iterable


class ScheduleType(Enum):
    Weekly = 1,
    Monthly = 2,
    Annually = 3,


class InvoiceProfileLineType(Enum):
    Simple = 1,
    TimeEntry = 2,
    UnbilledTimeEntry = 3,
    UnbilledExpense = 4


@dataclass
class InvoiceProfileLine:
    name: str
    description: str
    type: InvoiceProfileLineType
    quantity: int
    unit_cost: Decimal
    tax_name: str = None
    tax_amount: Decimal = 0

    @property
    def amount(self):
        amount_without_taxes = Decimal(self.unit_cost) * Decimal(self.quantity)
        taxes = amount_without_taxes * self.tax_amount

        return amount_without_taxes + taxes


class Schedule:
    def __init__(self, start_date, last_occurrence_date, schedule_type, schedule_multiplier):
        self.start_date = start_date
        self.last_occurrence_date = last_occurrence_date
        self.schedule_type = schedule_type
        self.schedule_multiplier = schedule_multiplier
        self._next_occurrence_date = self._calculate_next_occurrence_date()

    @property
    def next_occurrence_date(self):
        return self._calculate_next_occurrence_date()

    def _calculate_next_occurrence_date(self):
        if not self.last_occurrence_date:
            return self.start_date

        return self.last_occurrence_date + timedelta(weeks=1 * self.schedule_multiplier)


class InvoiceProfile:
    def __init__(self, lines: Iterable[InvoiceProfileLine], client_id, schedule):
        self.client_id = client_id
        self.schedule = schedule
        self.lines = lines
        self._amount = self._calculate_amount()
        self.schedule = schedule

    def update_schedule(self, schedule):
        self.schedule = schedule

    @property
    def amount(self):
        return self._amount

    def _calculate_amount(self):
        return sum(item.amount for item in self.lines)
