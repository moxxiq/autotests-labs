import hashlib
import os.path
from mimetypes import guess_type
import tornado.escape
import tornado.web
import tornado.httpserver
import uuid
from math import sqrt

__version__ = '0.0.1'

HTTP_PORT = 8000
BASEDIR_NAME = os.path.dirname(__file__)
BASEDIR_PATH = os.path.abspath(BASEDIR_NAME)

FILES_ROOT = os.path.join(BASEDIR_PATH, 'www')


def root_mean_square(arr):
    arr = list(filter(lambda x: x is not None, arr))
    return sqrt(sum(map(lambda x: x * x, arr)) / len(arr)) if len(arr) else None

class User(object):

    def __init__(self, user_id, display_name, email, sha_hash=None):
        self.id = user_id
        self.display_name = display_name
        self.email = email
        self.sha_hash = sha_hash

    def _make_hash(self, password_plain):
        hasher = hashlib.sha256()
        hasher.update(password_plain.encode('utf-8'))
        return hasher.digest()

    def make_hash(self, password_plain):
        self.sha_hash = self._make_hash(password_plain)

    def test_password(self, password_plain):
        return self.sha_hash == self._make_hash(password_plain)

class Comment(object):

    def __init__(self, comment_id, text, user_id):
        self.id = comment_id
        self.text = text
        self.user_id = user_id

class TestApp(tornado.web.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._next_comment_id = 1
        self._next_user_id = 1
        self.comments = []

        test_users = (
            ('Linus T.', 'torvalds@osdl.org', 'kernel'),
            ('Iryna K.', 'kostushkoia5@gmail.com', 'numericalerror'),
        )

        test_commentaries = (
            "Input: [2, 4, 16, 256] Answer: 128.2692480682724",
            "Input: [1, -1, 4, -4] Answer: 2.9154759474226504",
        )

        self.users_by_id = {}
        self.users_by_email = {}

        for display_name, email, password in test_users:
            self.add_user(display_name, email).make_hash(password)

        for comm, (user_id, user) in zip(test_commentaries, self.users_by_id.items()):
            self.add_comment(comm, user.id)

        self.sessions = {}
        self.token_by_id = {}

    def add_user(self, display_name, email):
        user = User(self._next_user_id, display_name, email)
        self.users_by_id[self._next_user_id] = user
        self.users_by_email[email] = user
        self._next_user_id += 1
        return user

    def add_comment(self, text, user_id):
        new_comment = Comment(self._next_comment_id, text, user_id)
        self.comments.append(new_comment)
        self._next_comment_id += 1

    def set_jwt(self, user_id, token):
        self.token_by_id.update({user_id: token})

    def get_jwt(self, user_id):
        return self.token_by_id.get(user_id)

    def del_jwt(self, user_id):
        del self.token_by_id[user_id]

    def is_users_comment(self, comment_id, user_id):
        for comment in self.comments:
            if comment.id == comment_id:
                return comment.user_id == user_id
                break

    def remove_comment(self, comment_id):
        for idx, comment in enumerate(self.comments):
            if comment.id == comment_id:
                del self.comments[idx]
                break


class ApiUserSignupHandler(tornado.web.RequestHandler):

    def post(self, path):
        data = tornado.escape.json_decode(self.request.body)
        user = self.application.users_by_email.get(data['email'])

        if user or not data['email'] or not data['display_name'] or not data['password']:
            raise tornado.web.HTTPError(status_code=500)
        else:
            user = self.application.add_user(
                data['display_name'], data['email'])
            user.make_hash(data['password'])
        token = str(uuid.uuid4())
        self.application.set_jwt(user.id, token)
        self.write({'token': token, 'user_id': user.id,
                    'display_name': user.display_name})


class ApiUserLoginHandler(tornado.web.RequestHandler):

    def post(self, path):
        data = tornado.escape.json_decode(self.request.body)
        user = self.application.users_by_email.get(data['email'])

        if not user or not user.test_password(data.get('password', '')):
            raise tornado.web.HTTPError(status_code=403)
        token = str(uuid.uuid4())
        self.application.set_jwt(user.id, token)
        self.write({'token': token, 'user_id': user.id,
                    'display_name': user.display_name})


class ApiUserLogoutHandler(tornado.web.RequestHandler):
    def post(self, path):
        data = tornado.escape.json_decode(self.request.body)
        user = self.application.users_by_id.get(data['id'])
        if self.get_cookie('jwt') != self.application.get_jwt(data['id']):
            raise tornado.web.HTTPError(status_code=401)
        if not user:
            raise tornado.web.HTTPError(status_code=403)
        if self.application.get_jwt(data['id']) == self.get_cookie('jwt'):
            self.application.del_jwt(data['id'])
            self.write("OK")


class ApiTaskHandler(tornado.web.RequestHandler):
    def write_comments(self):
        users = self.application.users_by_id
        comments = [{'id': x.id, 'text': x.text, 'user_id': x.user_id, 'display_name': users[x.user_id].display_name}
                    for x in self.application.comments]
        self.write({'comments': comments, 'answer': self.answer})

    def post(self, path):
        data = tornado.escape.json_decode(self.request.body)
        if self.get_cookie('jwt') != self.application.get_jwt(data['user_id']):
            raise tornado.web.HTTPError(status_code=401)
        numbers = list(filter(lambda x: x is not None, data.get('numbers')))
        self.answer = root_mean_square(numbers)
        text = "Input: " + str(numbers) + " Answer: " + str(self.answer)
        self.application.add_comment(text, data['user_id'])
        self.write_comments()


class ApiCommentsHandler(tornado.web.RequestHandler):
    def write_comments(self):
        users = self.application.users_by_id
        comments = [{'id': x.id, 'text': x.text, 'user_id': x.user_id, 'display_name': users[x.user_id].display_name}
                    for x in self.application.comments]
        self.write({'comments': comments})

    def get(self, path):
        self.write_comments()

    # def post(self, path):
    #     data = tornado.escape.json_decode(self.request.body)
    #     self.application.add_comment(data['text'], data['user_id'])
    #     self.write_comments()

    def delete(self, path):
        data = tornado.escape.json_decode(self.request.body)
        if self.application.is_users_comment(data['id'], data['user_id']) and (self.get_cookie('jwt') == self.application.get_jwt(data['user_id'])):
            self.application.remove_comment(data['id'])
            self.write_comments()
        else:
            raise tornado.web.HTTPError(status_code=403)


class FileHandler(tornado.web.RequestHandler):

    def get(self, path):
        if not path:
            path = 'index.html'
        file_location = os.path.join(FILES_ROOT, path)
        if not os.path.isfile(file_location):
            raise tornado.web.HTTPError(status_code=404)
        content_type, _ = guess_type(file_location)
        self.set_header('Content-Type', content_type)
        with open(file_location, 'rb') as source_file:
            self.write(source_file.read())


app = TestApp([
    tornado.web.url(r"/api/v1/user/(login)$", ApiUserLoginHandler),
    tornado.web.url(r"/api/v1/user/(logout)$", ApiUserLogoutHandler),
    tornado.web.url(r"/api/v1/user/(signup)$", ApiUserSignupHandler),
    tornado.web.url(r"/api/v1/(comments)$", ApiCommentsHandler),
    tornado.web.url(r"/api/v1/(task)$", ApiTaskHandler),
    tornado.web.url(r"/(.*)", FileHandler),
])

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(app)
    ADDRESS = 'localhost'
    http_server.listen(HTTP_PORT, address=ADDRESS)
    # print("Host on http://" + str(ADDRESS) + ':' + str(HTTP_PORT))
    tornado.ioloop.IOLoop.instance().start()
