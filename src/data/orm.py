# coding: utf-8
from sqlalchemy import Column, DECIMAL, ForeignKey, MetaData, Table, Text, text, Date
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import mapper, relationship

from src.domain import model

metadata = MetaData()

t_invoice_profile = Table(
    'invoice_profile', metadata,
    Column('id', INTEGER(11), primary_key=True),
    Column('amount', DECIMAL(10, 0)),
    Column('clientid', INTEGER(11), nullable=False)
)

t_invoice_profile_line_item = Table(
    'invoice_profile_line_item', metadata,
    Column('name', Text),
    Column('description', Text),
    Column('unit_cost', DECIMAL(10, 0)),
    Column('quantity', DECIMAL(10, 0)),
    Column('tax_name', Text),
    Column('tax_amount', DECIMAL(10, 0)),
    Column('type', INTEGER(11)),
    Column('profile_id', ForeignKey('invoice_profile.id'), nullable=False, index=True),
    Column('id', INTEGER(11), primary_key=True)
)

t_schedule = Table(
    'schedule', metadata,
    Column('id', INTEGER(11), primary_key=True),
    Column('start_date', Date),
    Column('last_occurrence_date', Date),
    Column('schedule_type', INTEGER(11), nullable=False),
    Column('schedule_multiplier', INTEGER(11), nullable=False),
    Column('next_occurrence_date', Date, nullable=False),
    Column('profileid', ForeignKey('invoice_profile.id'), nullable=False, index=True)
)


def start_mappers():
    mapper(model.InvoiceProfileLine, t_invoice_profile_line_item)
    mapper(model.Schedule, t_schedule, properties=
    {
        '_next_occurrence_date': t_schedule.c.next_occurrence_date
    })
    mapper(model.InvoiceProfile, t_invoice_profile, properties={
        '_amount': t_invoice_profile.c.amount,
        'client_id': t_invoice_profile.c.clientid,
        'schedule': relationship(model.Schedule, uselist=False),
        'lines': relationship(model.InvoiceProfileLine),
    })

