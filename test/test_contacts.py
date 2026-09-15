from dataclasses import asdict


class TestContacts:
    def test_add_contact(self, session, add_contact_url, auth_header, random_contact):
        response=session.post(
            add_contact_url,
            headers=auth_header,
            json=asdict(random_contact)
        )
        print(response.json())
        assert response.status_code == 200