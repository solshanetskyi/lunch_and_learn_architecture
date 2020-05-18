from decimal import Decimal

from src.domain.model import InvoiceProfileLine, InvoiceProfileLineType


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


