from datetime import date

from src.domain import model
from src.domain.model import Schedule
from src.service_layer.unit_of_work import AbstractUnitOfWork


def copy_profile(profile_id: int, uow: AbstractUnitOfWork):
    with uow:
        profile = uow.profiles.get(profile_id)
        copied_profile = model.copy_profile(profile)

        uow.profiles.add(copied_profile)
        uow.commit()

        return copied_profile.id


def update_profile_schedule(profile_id: int, start_date: date, schedule_type, schedule_multiplier: int,
                            uow: AbstractUnitOfWork):
    with uow:
        profile = uow.profiles.get(profile_id)

        schedule = Schedule(
            start_date=start_date,
            last_occurrence_date=None,
            schedule_type=schedule_type,
            schedule_multiplier=schedule_multiplier)

        profile.update_schedule(schedule)

        uow.commit()
