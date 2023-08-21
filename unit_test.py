import unittest
import main as server


class TestLoginFunction(unittest.TestCase):

    def setUp(self):
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()

    def test_login_success(self):
        # 先添加用户以供测试
        server.users['user@example.com'] = {'password': server.pbkdf2_sha256.hash('password123'), 'logged_in': False}

        # 测试登录
        response = self.app.post('/login', json={'username': 'user@example.com', 'password': 'password123'})
        self.assertEqual(response.status_code, 200)

    def test_login_failure(self):
        response = self.app.post('/login', json={'username': 'user@example.com', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
