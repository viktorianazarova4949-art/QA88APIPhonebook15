import random
import time

import pytest
import requests
from faker import Faker

from config import *
from models.contact_dto import Contact
from models.user_dto import User
from dataclasses import asdict
fake = Faker()


@pytest.fixture(scope="session")
def registration_url():
    return BASE_URL + API_VERSION + REGISTRATION_URL

@pytest.fixture(scope="session")
def login_url():
    return BASE_URL + API_VERSION + LOGIN_URL

@pytest.fixture(scope="session")
def add_contact_url():
    return BASE_URL + API_VERSION + ADD_CONTACT_URL

@pytest.fixture(scope="session")
def session():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    yield s
    s.close()


@pytest.fixture(scope="function")
def random_user():
    username = f"qa_{int(time.time())}_{fake.email()}"
    password = fake.password(
        length=random.randint(8, 15),
        special_chars=False,
        digits=True,
        upper_case=True,
        lower_case=True,
    )+"$"
    return User(username=username, password=password)

@pytest.fixture(scope="function")
def registered_user(session, registration_url, random_user):
    user_data = {
        "username": random_user.username,
        "password": random_user.password,
    }
    response_reg = session.post(registration_url, json=user_data)
    if response_reg.status_code == 200:
        return random_user
    return User(TEST_EMAIL, TEST_PASSWORD)

@pytest.fixture(scope="function")
def auth_token(session, registration_url, random_user):
    user_data = {
        "username": random_user.username,
        "password": random_user.password,
    }
    response= session.post(registration_url, json=user_data)
    assert response.status_code == 200, (
        f"Failed registration {response.status_code} {response.text}"
    )
    return response.json()["token"]

@pytest.fixture(scope="function")
def auth_header(auth_token):
    return {"Authorization": auth_token}


@pytest.fixture(scope="function")
def random_contact():
    return Contact(
        name=fake.name(),
        lastName=fake.last_name(),
        email=fake.email(),
        phone=fake.numerify("#" * random.randint(10, 15)),
        address=fake.address()[:50],
        description=fake.text(max_nb_chars=200),
    )

@pytest.fixture(scope="function")
def create_contact(session, random_contact,add_contact_url,auth_header):
    response= session.post(add_contact_url,
                           json=asdict(random_contact),
                           headers=auth_header)
    contact_id = response.json()["message"][23:]
    #print(contact_id)
    return contact_id