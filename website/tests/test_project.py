from website.models import User

def test_home(client):
    response = client.get("/login")
    assert b"<title>Login</title>" in response.data  

def test_registration(client, app):
    response = client.post("/sign-up", data={"email": "test@test.com", "password1": "testpassword", "password2": "testpassword"})
    print(response.data)
    with app.app_context():
        assert User.query.count() == 1
        assert User.query.first().email == "test@test.com"