from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.data.orm import start_mappers
from src.domain import model

start_mappers()
connecting_string = f'mysql+mysqldb://root:sekret@127.0.0.1:52000/lunch_and_learn'


@pytest.fixture
def session():
    engine = create_engine(connecting_string, echo=False)
    engine.connect()

    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(model.Schedule).delete()
    session.query(model.InvoiceProfileLine).delete()
    session.query(model.InvoiceProfile).delete()

    session.commit()

    return session


def test_orm_save(session):
    profile_line_1 = model.InvoiceProfileLine(name='name',
                                              description='description',
                                              type=model.InvoiceProfileLineType.Simple.value,
                                              quantity=3,
                                              unit_cost=Decimal('4.0'))

    profile_line_2 = model.InvoiceProfileLine(name='name_2',
                                              description='description_2',
                                              type=model.InvoiceProfileLineType.TimeEntry.value,
                                              quantity=5,
                                              unit_cost=Decimal('8.0'))

    schedule = model.Schedule(start_date=date.today(),
                              last_occurrence_date=None,
                              schedule_type=1,
                              schedule_multiplier=1)

    profile = model.InvoiceProfile([profile_line_1, profile_line_2], 3, schedule)

    session.add(profile)
    session.commit()


def test_orm_get(session):
    test_orm_save(session)

    profiles = session.query(model.InvoiceProfile).all()

    assert len(profiles)
