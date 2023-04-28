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

def test_registration_passwords_dont_match(client):
    response = client.post("/sign-up", data={"email": "test@test.com", "password1": "testpassword", "password2": "testpassword2"})
    assert b'Passwords dont match' in response.data

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
    
def test_pricing_no_date(client):
    client.post("/sign-up", data={"email": "test@test.com", "password1": "testpassword", "password2": "testpassword"})
    client.post("/login", data={"email": "test@test.com", "password": "testpassword"})
    client.post("/profile", data={"fullName": "John Smith", "address1": "123 Main", "address2": "appt 1", "city": "houston", "state": "Tx", "zipcode": "77001"})
    response = client.post("/price_module", data={"gallons":"5", "date": ""})
    assert b'Please enter a date for delivery' in response.data

def test_pricing_bad_gallons(client):
    client.post("/sign-up", data={"email": "test@test.com", "password1": "testpassword", "password2": "testpassword"})
    client.post("/login", data={"email": "test@test.com", "password": "testpassword"})
    client.post("/profile", data={"fullName": "John Smith", "address1": "123 Main", "address2": "appt 1", "city": "houston", "state": "Tx", "zipcode": "77001"})
    response = client.post("/price_module", data={"gallons":"", "date":"2024-11-23"})
    assert b'Please enter a numeric value for gallons requested' in response.data
    response = client.post("/price_module", data={"gallons":"a", "date":"2024-11-23"})
    assert b'Please enter a numeric value for gallons requested' in response.data
    response = client.post("/price_module", data={"gallons":"-1", "date":"2024-11-23"})
    assert b'Please enter a valid numerical value for gallons requested' in response.data

def test_pricing_texas(client, app):
    client.post("/sign-up", data={"email": "test@test.com", "password1": "testpassword", "password2": "testpassword"})
    client.post("/login", data={"email": "test@test.com", "password": "testpassword"})
    client.post("/profile", data={"fullName": "John Smith", "address1": "123 Main", "address2": "appt 1", "city": "houston", "state": "TX", "zipcode": "77001"})
    client.post("/price_module", data={"gallons":"5", "date":"2024-11-23"})
    with app.app_context():
        total = 5*(1.5+(1.5*((0.02) + (.03 + 0.1))))
        total = Math.round((total + Number.EPSILON) * 100) / 100;
        assert Transaction.query.first().total == 5*(1.5+(1.5*((0.02) + (.03 + 0.1))))
    # client.post("/price_module", data={"gallons":"20", "date":"2024-11-23"})
    # with app.app_context():
    #     assert Transaction.query.second().total == 20*(1.5+(1.5*((0.02-.01) + (.03 + 0.1)))) 


def test_history_load(client):
    client.post("/sign-up", data={"email": "test@test.com", "password1": "testpassword", "password2": "testpassword"})
    client.post("/login", data={"email": "test@test.com", "password": "testpassword"})
    response = client.get("/history", follow_redirects=True)
    assert b"<title>Transaction History</title>" in response.data