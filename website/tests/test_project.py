from website.models import User, Transaction

def test_home(client):
    response = client.get("/login")
    assert b"<title>Login</title>" in response.data  

def test_registration(client, app):
    client.post("/sign-up", data={"email": "test@test.com", "password1": "testpassword", "password2": "testpassword"})
    client.post("/sign-up", data={"email": "test@test.com", "password1": "testpassword", "password2": "testpassword"})
    with app.app_context():
        assert User.query.count() == 1
        assert User.query.first().email == "test@test.com"

def test_registration_duplicate(client):
    client.post("/sign-up", data={"email": "test@test.com", "password1": "testpassword", "password2": "testpassword"})
    response = client.post("/sign-up", data={"email": "test@test.com", "password1": "testpassword", "password2": "testpassword"})
    assert b'Email already exists.' in response.data

def test_registration_not_email(client):
    response = client.post("/sign-up", data={"email": "not an email", "password1": "testpassword", "password2": "testpassword"})
    assert b'Please enter a valid email address' in response.data

def test_registration_no_match(client):
    response = client.post("/sign-up", data={"email": "test@test.com", "password1": "testpassword", "password2": "wrongpassword"})
    assert b"Passwords don't match." in response.data

def test_registration_bad_password(client):
    response = client.post("/sign-up", data={"email": "test@test.com", "password1": "short", "password2": "short"})
    assert b'Password must be at least 7 characters.' in response.data


def test_login_wrong_password(client):
    client.post("/sign-up", data={"email": "test@test.com", "password1": "testpassword", "password2": "testpassword"})
    response = client.post("/login", data = {"email": "test@test.com", "password": "incorrect"})
    assert b'Incorrect password, try again.' in response.data

def test_login_not_present(client):
    client.post("/sign-up", data={"email": "test@test.com", "password1": "testpassword", "password2": "testpassword"})
    response = client.post("/login", data = {"email": "not@present.com", "password": "testpassword"})
    assert b'Email does not exist.' in response.data

def test_logout(client):
    client.post("/sign-up", data={"email": "test@test.com", "password1": "testpassword", "password2": "testpassword"})
    response = client.get("/logout", follow_redirects=True)
    assert b'Logged out' in response.data

def test_profile(client, app):
    client.post("/sign-up", data={"email": "test@test.com", "password1": "testpassword", "password2": "testpassword"})
    client.post("/login", data={"email": "test@test.com", "password": "testpassword"})

    client.post("/profile", data={"fullName": "John Smith", "address1": "123 Main", "address2": "appt 1", "city": "houston", "state": "Tx", "zipcode": "77001"})
    with app.app_context():
        assert User.query.first().fullName == "John Smith"
        assert User.query.first().address1 == "123 Main"
        assert User.query.first().address2 == "appt 1"
        assert User.query.first().city == "houston"
        assert User.query.first().state == "Tx"
        assert User.query.first().zipcode == "77001"
    profile = client.get("/profile")    
    assert b"<title>Profile</title>" in profile.data

    response = client.get("/")
    assert b"<title>Home</title>" in response.data

def test_pricing(client, app):
    client.post("/sign-up", data={"email": "test@test.com", "password1": "testpassword", "password2": "testpassword"})
    client.post("/login", data={"email": "test@test.com", "password": "testpassword"})
    client.post("/profile", data={"fullName": "John Smith", "address1": "123 Main", "address2": "appt 1", "city": "houston", "state": "Tx", "zipcode": "77001"})
    client.post("/price_module", data={"gallons":"5", "date":"2024-11-23"})
    with app.app_context():
        assert Transaction.query.first().total == 25

def test_history(client):
    client.post("/sign-up", data={"email": "test@test.com", "password1": "testpassword", "password2": "testpassword"})
    client.post("/login", data={"email": "test@test.com", "password": "testpassword"})
    response = client.get("/history", follow_redirects=True)
    assert b"<title>Transaction History</title>" in response.data