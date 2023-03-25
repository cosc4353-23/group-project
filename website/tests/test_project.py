def test_home(client):
    response = client.get("/login?next=%2F")
    assert b"<title>Home</title>" in response.data  

