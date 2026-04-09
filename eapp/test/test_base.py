from flask import Flask
from eapp import db
import pytest
from eapp.models import Product
from eapp.index import register_app


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["PAGE_SIZE"] = 8
    app.config["Testing"] = True
    app.secret_key = "dsvfysgr65345n$^$xdnjfj"

    db.init_app(app)
    register_app(app=app)

    return app

@pytest.fixture
def test_app():
    app = create_app()

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def test_client(test_app):
    return test_app.test_client()

@pytest.fixture
def test_session(test_app):
    yield db.session
    db.session.rollback()

@pytest.fixture
def sample_products(test_session):
    products = [{
        "name": "iPhone 7 Plus",
        "description": "Apple, 32GB, RAM: 3GB, iOS13",
        "price": 17000000,
        "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg",
        "category_id": 1
    }, {
        "name": "iPad Pro 2020",
        "description": "Apple, 128GB, RAM: 6GB",
        "price": 37000000,
        "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729533/zuur9gzztcekmyfenkfr.jpg",
        "category_id": 2
    }, {
        "name": "Galaxy Note 10 Plus",
        "description": "Samsung, 64GB, RAML: 6GB",
        "price": 24000000,
        "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg",
        "category_id": 1
    }, {
        "name": "iPhone 7 Plus",
        "description": "Apple, 32GB, RAM: 3GB, iOS13",
        "price": 17000000,
        "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg",
        "category_id": 1
    }, {
        "name": "iPad Pro 2020",
        "description": "Apple, 128GB, RAM: 6GB",
        "price": 37000000,
        "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729533/zuur9gzztcekmyfenkfr.jpg",
        "category_id": 2
    }, {
        "name": "Galaxy Note 10 Plus",
        "description": "Samsung, 64GB, RAML: 6GB",
        "price": 24000000,
        "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg",
        "category_id": 1
    }, {
        "name": "iPhone 7 Plus",
        "description": "Apple, 32GB, RAM: 3GB, iOS13",
        "price": 17000000,
        "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg",
        "category_id": 1
    }, {
        "name": "iPad Pro 2020",
        "description": "Apple, 128GB, RAM: 6GB",
        "price": 37000000,
        "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729533/zuur9gzztcekmyfenkfr.jpg",
        "category_id": 2
    }, {
        "name": "Galaxy Note 10 Plus",
        "description": "Samsung, 64GB, RAML: 6GB",
        "price": 24000000,
        "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg",
        "category_id": 1
    }]

    for p in products:
        pro = Product(**p)
        test_session.add(pro)

    test_session.commit()
    return products
