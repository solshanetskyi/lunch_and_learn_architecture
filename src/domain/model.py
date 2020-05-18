from dataclasses import dataclass
from datetime import date
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


@dataclass(frozen=True)
class InvoiceProfileLine:
    name: str
    type: InvoiceProfileLineType
    description: str
    quantity: int
    unit_cost: Decimal
    tax_name: str
    tax_amount: Decimal


@dataclass(frozen=True)
class Schedule:
    start_date: date
    last_occurrence_date: date
    schedule_type: ScheduleType
    schedule_multiplier: int
    next_occurrence_date: date


class InvoiceProfile:
    def __init__(self, lines: Iterable[InvoiceProfileLine], schedule, client_id):
        self.client_id = client_id
        self.schedule = schedule
        self.lines = lines
