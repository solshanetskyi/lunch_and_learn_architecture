from datetime import date
from decimal import Decimal

import pytest

from src.domain.errors import CloningProfileWithRecurringTimeEntries
from src.domain.model import InvoiceProfileLine, InvoiceProfileLineType, Schedule, ScheduleType, InvoiceProfile
from src.domain.service import copy_profile


def test_amount_without_taxes():
    line: InvoiceProfileLine = InvoiceProfileLine(name='Fake name',
                                                  description='Fake Description',
                                                  unit_cost=Decimal(4.0),
                                                  quantity=6,
                                                  type=InvoiceProfileLineType.Simple)

    assert 24 == line.amount


def test_amount_wit_taxes():
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
        schedule_type=ScheduleType.Weekly.value,
        schedule_multiplier=2)

    assert schedule.next_occurrence_date == date(2020, 1, 15)
def test_copy_invoice_profile__copies_line_items_and_client():
    profile = _create_invoice_profile()

    copied_profile = copy_profile(profile)

    assert copied_profile.client_id == profile.client_id

    assert copied_profile.lines
    assert len(copied_profile.lines) == 1

    original_line = profile.lines[0]
    copied_line = copied_profile.lines[0]

    assert copied_line.name == original_line.name
    assert copied_line.description == original_line.description
    assert copied_line.unit_cost == original_line.unit_cost
    assert copied_line.quantity == original_line.quantity


def test_copy_invoice_profile__does_not_copy_schedule():
    profile = _create_invoice_profile()

    copied_profile = copy_profile(profile)

    assert not copied_profile.schedule


def test_copy_invoice_profile__returns_error_when_copying_recurring_time_entries():
    line = InvoiceProfileLine(name='Fake name',
                              description='Fake Description',
                              unit_cost=Decimal(100.0),
                              quantity=1,
                              type=InvoiceProfileLineType.UnbilledTimeEntry.value,
                              tax_name='HST',
                              tax_amount=Decimal('0.13'))

    profile = InvoiceProfile(lines=[line], client_id=5, schedule=None)

    with pytest.raises(CloningProfileWithRecurringTimeEntries):
        copy_profile(profile)


def _create_invoice_profile():
    line = InvoiceProfileLine(name='Fake name',
                              description='Fake Description',
                              unit_cost=Decimal(100.0),
                              quantity=1,
                              type=InvoiceProfileLineType.Simple.value,
                              tax_name='HST',
                              tax_amount=Decimal('0.13'))

    schedule = Schedule(start_date=date.today(), last_occurrence_date=None, schedule_type=ScheduleType.Weekly.value,
                        schedule_multiplier=2)

    profile = InvoiceProfile(lines=[line], client_id=5, schedule=schedule)
    return profile
