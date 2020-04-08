from app.shopping_cart import send_email

def test_send_email():
    content = "test"
    email = "dan.cagney@gmail.com"
    assert send_email(content,email) == True