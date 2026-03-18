import pytest
import sqlite3
## Basic Fixture

@pytest.fixture
def username():
    return "admin"

@pytest.fixture
def password():
    return "admin123"

def test_username(username,password):
    assert username=='admin'
    assert password=='admin123'

## Fixtures with setup and teardown

@pytest.fixture

def resource():
    print("Code runs before test")
    yield "resource"
    print("code runs after test")

def test_resources(resource,username,password):   ## Using multiple fixture in same test function
    assert resource=="resource"
    assert username=="admin"
    assert password=="admin123"

## fixture scope

@pytest.fixture(scope='module')
def db_connection():
    print("connection db")
    conn=sqlite3.connect("fixture.db")
    yield conn
    print("closing db")
    return "DB is connected"

@pytest.fixture(scope="function")
def cur(db_connection):
    cur=db_connection.cursor()
    yield cur
    cur.close()

def test_insert(cur):
    cur.execute("create table users(id int, name varchar(120))")
    cur.execute("insert into users(id,name) values(2,'ashi')")
    cur.execute("select * from users")
    res=cur.fetchall()
    assert res==[(2,'ashi')]
