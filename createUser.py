import requests
from bs4 import BeautifulSoup as bs
from bs4 import Comment


class UseSupersetApi:
    def __init__(self, username=None, password=None):
        self.s = requests.Session()
        self.base_url = "http://localhost:8088/"
        print('CSRFFFFFFFFFFFFFFFFF')
        self._csrf = self._getCSRF(self.url('login/'))
        print('CSRFFFFFFFFFFFFFFFFF', self._csrf)
        self.headers = {'X-CSRFToken': self._csrf,
                        'Referer': self.url('login/')}
        # note: does not use headers because of flask_wtf.csrf.validate_csrf
        # if data is dict it is used as form and ends up empty but flask_wtf checks if data ...
        self.s.post(self.url('login/'),
                    data={'username': username, 'password': password, 'csrf_token': self._csrf})

    def url(self, url_path):
        return self.base_url + url_path

    def get(self, url_path):
        return self.s.get(self.url(url_path), headers=self.headers, allow_redirects=False)

    def post(self, url_path, data=None, json_data=None, **kwargs):
        kwargs.update({'url': self.url(url_path), 'headers': self.headers})
        if data:
            data['csrf_token'] = self._csrf
            kwargs['data'] = data
        if json_data:
            kwargs['json'] = json_data
        return self.s.post(**kwargs)

    def _getCSRF(self, url_path):
        response = self.s.get(url_path, allow_redirects=False)
        print('ressssssssssssssssssssss', response, url_path)
        soup = bs(response.content, "html.parser")
        for tag in soup.find_all('input', id='csrf_token'):
            csrf_token = tag['value']
        return csrf_token


superset = UseSupersetApi('admin', 'passoword')
users = []  # some user dicts inside

print(superset)
# for user in users:
#     payload = {'first_name': user['first_name'],
#                'last_name': user['last_name'],
#                'username': user['username'],
#                'email': user['email'],
#                'active': True,
#                'conf_password': user['password'],
#                'password': user['password'],
#                'roles': user['roles']}
#     print(superset.post(url_path='users/api/create', json=payload))
