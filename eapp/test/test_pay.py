from eapp.test.test_base import test_client, test_app, test_session
from eapp.models import User, Receipt, ReceiptDetails, Product

def test_pay_success(test_client, mocker):
    class FakeUser:
        is_authenticated = True

    with test_client.session_transaction() as sess:
        sess['cart'] = {
            "1": {
                "id": 1,
                "name": "aaaa",
                "price": 100,
                "quantity": 2
            }
        }

    mocker.patch("flask_login.utils._get_user", return_value=FakeUser)

    mock_add = mocker.patch("eapp.dao.add_receipt")

    res = test_client.post("/api/pay")
    data = res.get_json()

    assert data['status'] == 200

    with test_client.session_transaction() as sess:
        assert 'cart' not in sess

    mock_add.assert_called_once()

def test_pay_without_login(test_client, mocker):
    with test_client.session_transaction() as sess:
        sess['cart'] = {
            "1": {
                "id": 1,
                "name": "aaaa",
                "price": 100,
                "quantity": 2
            }
        }

    res = test_client.post("/api/pay")
    assert (res.status_code == 401 or res.status_code == 500)

def test_pay_exception(test_client, mocker):
    pass
    class FakeUser:
        is_authenticated = True

    with test_client.session_transaction() as sess:
        sess['cart'] = {
            "1": {
                "id": 1,
                "name": "aaaa",
                "price": 100,
                "quantity": 2
            }
        }

    mocker.patch("flask_login.utils._get_user", return_value=FakeUser)

    mock_add = mocker.patch("eapp.dao.add_receipt", side_effect=Exception("DB Error"))

    res = test_client.post("/api/pay")
    data = res.get_json()

    assert data['status'] == 400
    assert data['err_msg'] == "DB Error"

    with test_client.session_transaction() as sess:
        assert 'cart' in sess

    mock_add.assert_called_once()


# def test_all(test_client, test_session):
#     u = User(name="hehe", username="abc", password="123")
#     test_session().add(u)
#
#     p1 = Product(name=)

