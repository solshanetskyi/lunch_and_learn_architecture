from datetime import date

from src.domain import model
from src.domain.repository import AbstractRepository


def copy_profile(profile_id: int, repository: AbstractRepository, session):
    profile = repository.get(profile_id)
    copied_profile = model.copy_profile(profile)

    repository.add(copied_profile)
    session.commit()

    return copied_profile.id


def update_profile_schedule(profile_id: int, start_date: date, schedule_type, schedule_multiplier: int):
    pass
