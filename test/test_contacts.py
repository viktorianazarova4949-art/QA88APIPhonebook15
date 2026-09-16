from dataclasses import asdict
from faker import Faker
import random

fake = Faker()

class TestContacts:
    def test_add_contact_positive(self, session, add_contact_url, auth_header, random_contact):
        response = session.post(
            add_contact_url,
            headers=auth_header,
            json=asdict(random_contact)
        )
        print(response.json()["message"])
        assert response.status_code == 200
        assert "Contact was added!" in response.json()["message"]

    def test_get_all_contacts_positive(self, session, add_contact_url, auth_header):
        response = session.get(add_contact_url, headers=auth_header)
        print(response.json())
        assert response.status_code == 200
        assert isinstance(response.json()["contacts"], list)

    def test_get_all_contacts_negative_wrong_token(self, session, add_contact_url):
        headers = {"Authorization": "vbghtuyi bnhyui "}
        response = session.get(add_contact_url, headers=headers)
        print(response.json())
        assert response.status_code == 401
        assert response.json()["error"] == "Unauthorized"

    def test_update_contact_positive(self, session, add_contact_url, auth_header, create_contact):
        contact_id = create_contact
        #print("Contact ID:", contact_id)
        res1 = session.get(add_contact_url, headers=auth_header)
        #print(res1.json())
        updated_contact = {
            "id": contact_id,
            "name": fake.name(),
            "lastName":fake.last_name(),
            "email":fake.email(),
            "phone":fake.numerify("#" * random.randint(10, 15)),
            "address":"address",
            "description":"text",
        }
        response = session.put(add_contact_url, headers=auth_header, json=updated_contact)
       # print(response.json())
        assert response.status_code == 200
        assert "Contact was updated" in response.json()["message"]
        res = session.get(add_contact_url, headers=auth_header)
        #print(res.json())
        assert res.json()["contacts"][0]["address"] == "address"
        assert res.json()["contacts"][0]["phone"] == updated_contact["phone"]

