from decimal import Decimal

from src.domain import repository
from src.domain.model import InvoiceProfileLine, InvoiceProfileLineType, ScheduleType, InvoiceProfile
from src.service_layer import services, unit_of_work


class FakeRepository(repository.AbstractRepository):
    def __init__(self, profiles):
        self._profiles = profiles

    def add(self, profile):
        self._profiles.append(profile)

    def get(self, profile_id):
        return next(p for p in self._profiles if p.id == profile_id)

    def list(self):
        return list(self._profiles)


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):

    def __init__(self):
        self.products = FakeRepository([])
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


def test_copy_profile():
    line = InvoiceProfileLine(name='Fake name',
                              description='Fake Description',
                              unit_cost=Decimal(100.0),
                              quantity=1,
                              type=InvoiceProfileLineType.Simple.value,
                              tax_name='HST',
                              tax_amount=Decimal('0.13'))

    profile = InvoiceProfile(lines=[line], client_id=5, schedule=None, profile_id=7)

    repository, session = FakeRepository([profile]), FakeSession()

    services.copy_profile(profile_id=7, repository=repository, session=session)

    assert len(repository.list())

    assert session.committed
