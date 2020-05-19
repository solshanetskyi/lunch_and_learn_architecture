from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.adapters.sql_alchemy_repository import SqlAlchemyRepository
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


def test_repository_save(session):
    profile_line = model.InvoiceProfileLine(name='name_2',
                                            description='description_2',
                                            type=model.InvoiceProfileLineType.TimeEntry.value,
                                            quantity=5,
                                            unit_cost=Decimal('8.0'))

    schedule = model.Schedule(start_date=date.today(),
                              last_occurrence_date=None,
                              schedule_type=1,
                              schedule_multiplier=1)

    profile = model.InvoiceProfile([profile_line], 3, schedule)

    repository = SqlAlchemyRepository(session)

    repository.add(profile)
    session.commit()
