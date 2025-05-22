import os
from main import create_app
from flask import url_for

# Set up environment variables for tests
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['REDIS_URL'] = 'redis://localhost/0'

app = create_app()
app.testing = True

with app.test_client() as client:
    resp = client.get('/logout')
    assert resp.status_code == 302, resp.status_code
    # The Location header may include http://localhost or similar; we just check path
    target = url_for('web.user_login', _external=False)
    assert resp.headers['Location'].endswith(target), resp.headers['Location']
print('redirects to', resp.headers['Location'])
