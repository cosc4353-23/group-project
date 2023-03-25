from website.models import User, Transaction

def test_home(client):
    response = client.get("/login")
    assert b"<title>Login</title>" in response.data  

def test_registration(client, app):
    response = client.post("/sign-up", data={"email": "test@test.com", "password1": "testpassword", "password2": "testpassword"})
    with app.app_context():
        assert User.query.count() == 1
        assert User.query.first().email == "test@test.com"

def test_profile(client, app):
    client.post("/sign-up", data={"email": "test@test.com", "password1": "testpassword", "password2": "testpassword"})
    client.post("/login", data={"email": "test@test.com", "password": "testpassword"})

    response = client.post("/profile", data={"fullName": "John Smith", "address1": "123 Main", "address2": "appt 1", "city": "houston", "state": "Tx", "zipcode": "77001"})
    with app.app_context():
        assert User.query.first().fullName == "John Smith"
        assert User.query.first().address1 == "123 Main"
        assert User.query.first().address2 == "appt 1"
        assert User.query.first().city == "houston"
        assert User.query.first().state == "Tx"
        assert User.query.first().zipcode == "77001"

def test_pricing(client, app):
    client.post("/sign-up", data={"email": "test@test.com", "password1": "testpassword", "password2": "testpassword"})
    client.post("/login", data={"email": "test@test.com", "password": "testpassword"})
    client.post("/profile", data={"fullName": "John Smith", "address1": "123 Main", "address2": "appt 1", "city": "houston", "state": "Tx", "zipcode": "77001"})
    client.post("/price_module", data={"gallons":"5", "date":"2024-11-23"})
    with app.app_context():
        assert Transaction.query.first().total == 25