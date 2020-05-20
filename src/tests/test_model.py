from datetime import date
from decimal import Decimal

from src.domain.model import InvoiceProfileLine, InvoiceProfileLineType, InvoiceProfile, Schedule, ScheduleType


def test_line_item_amount_without_taxes():
    line: InvoiceProfileLine = InvoiceProfileLine(name='Fake name',
                                                  description='Fake Description',
                                                  unit_cost=Decimal(4.0),
                                                  quantity=6,
                                                  type=InvoiceProfileLineType.Simple)

    assert 24 == line.amount


def test_line_item_amount_wit_taxes():
    line: InvoiceProfileLine = InvoiceProfileLine(name='Fake name',
                                                  description='Fake Description',
                                                  unit_cost=Decimal(100.0),
                                                  quantity=1,
                                                  type=InvoiceProfileLineType.Simple,
                                                  tax_name='HST',
                                                  tax_amount=Decimal('0.13'))

    assert Decimal(113) == line.amount


def test_profile_amount():
    line_1: InvoiceProfileLine = InvoiceProfileLine(name='Fake name',
                                                    description='Fake Description',
                                                    unit_cost=Decimal(5.0),
                                                    quantity=6,
                                                    type=InvoiceProfileLineType.Simple)

    line_2: InvoiceProfileLine = InvoiceProfileLine(name='Fake name',
                                                    description='Fake Description',
                                                    unit_cost=Decimal(4.0),
                                                    quantity=3,
                                                    type=InvoiceProfileLineType.Simple)

    profile = InvoiceProfile(lines=[line_1, line_2], client_id=3, schedule=None)

    assert 42 == profile.amount


def test_schedule_next_date():
    schedule = Schedule(
        start_date=date(2020, 1, 1),
        last_occurrence_date=date(2020, 1, 1),
        schedule_type=ScheduleType.Weekly,
        schedule_multiplier=2)

    assert schedule.next_occurrence_date == date(2020, 1, 15)
