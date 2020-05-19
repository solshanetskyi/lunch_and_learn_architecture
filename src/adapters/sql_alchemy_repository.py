from src.domain import model
from src.domain.repository import AbstractRepository


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, profile: model.InvoiceProfile):
        self.session.add(profile)

    def get(self, profile_id):
        return self.session.query(model.InvoiceProfile).filter_by(model.InvoiceProfile.id == profile_id).one_or_none()
