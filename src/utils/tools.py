from datetime import date

from faker import Faker
from pydantic import BaseModel


class UserRandom(BaseModel):
    name: str
    address: str
    email: str
    phone: str
    birth_date: date
    company: str
    job: str


class RandomData:
    faker_ = Faker("ru_RU")

    @property
    def random_user(self) -> UserRandom:
        f = self.__class__.faker_
        return UserRandom(
            name=f.name(),
            address=f.address(),
            email=f.email(),
            phone=f.phone_number(),
            birth_date=f.date_of_birth(),
            company=f.company(),
            job=f.job(),
        )


random_data: RandomData = RandomData()
