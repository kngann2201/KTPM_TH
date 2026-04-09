from eapp.test.test_base import test_app, test_client

def test_add_to_cart(test_client):
    res = test_client.post("/api/carts", json = {
        "id": 1,
        "name": "aaaa",
        "price": 123
    })

    assert res.status_code == 200

    data = res.get_json()
    assert data['total_quantity'] == 1
    assert data['total_amount'] == 123

def test_add_increase_item(test_client):
    test_client.post("/api/carts", json = {
        "id": 1,
        "name": "aaaa",
        "price": 100
    })
    test_client.post("/api/carts", json={
        "id": 1,
        "name": "aaaa",
        "price": 100
    })
    res = test_client.post("/api/carts", json={
        "id": 2,
        "name": "aaaa",
        "price": 100
    })

    assert res.status_code == 200

    data = res.get_json()
    assert data['total_quantity'] == 3
    assert data['total_amount'] == 300

    with test_client.session_transaction() as sess:
        assert 'cart' in sess
        assert len(sess['cart']) == 2
        assert sess['cart']['1']['quantity'] == 2

def test_add_existing(test_client):
    with test_client.session_transaction() as sess:
        sess['cart'] = {
             "1" : {
                "id": 1,
                "name": "aaaa",
                "price": 100,
                "quantity": 2
            }
        }

    res = test_client.post("/api/carts", json={
        "id": 1,
        "name": "aaaa",
        "price": 100
    })

    data = res.get_json()
    assert data['total_quantity'] == 3
    assert data['total_amount'] == 300

    with test_client.session_transaction() as sess:
        assert 'cart' in sess
        assert len(sess['cart']) == 1
        assert sess['cart']['1']['quantity'] == 3

def test_empty_rq(test_client):
    with test_client.session_transaction() as sess:
        sess['cart'] = {
             "1" : {
                "id": 1,
                "name": "aaaa",
                "price": 100,
                "quantity": 2
            }
        }

    test_client.post("/api/carts", json={

    })

    with test_client.session_transaction() as sess:
        assert 'cart' in sess
        assert 'None' in sess['cart']
        assert len(sess['cart']) == 2
        assert sess['cart']['1']['quantity'] == 2










