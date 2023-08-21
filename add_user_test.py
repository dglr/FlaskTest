import unittest
from main import app
import json

class AdminAddUserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_add_user_by_admin(self):
        # 假设管理员Token为一个有效的管理员邮箱
        admin_token = "admin@example.com"

        # 需要添加的新用户
        new_user_data = {
            'username': '13195185901', 'password': 'AnotherNewUser123'
        }

        # 发送添加用户请求
        response = self.app.post('/admin/add_user',
                                 data=json.dumps(new_user_data),
                                 content_type='application/json',
                                 headers={'Authorization': admin_token,'X-Secret-Key': 'adminsecret', 'role': 'admin'})

        # 检查状态代码和响应消息
        self.assertEqual(response.status_code, 200)
        self.assertIn('User added successfully', response.data.decode())

    def test_add_user_by_non_admin(self):
        # 假设非管理员Token
        non_admin_token = "nonadmin@example.com"

        # 需要添加的新用户
        new_user_data = {
            "username": "anothernewuser@example.com",
            "password": "AnotherNewUser123"
        }


        # 发送添加用户请求
        response = self.app.post('/admin/add_user',
                                 data=json.dumps(new_user_data),
                                 content_type='application/json',
                                 headers={'Authorization': non_admin_token})

        # 检查状态代码和响应消息
        self.assertEqual(response.status_code, 403)
        self.assertIn('Admin access required', response.data.decode())

    def test_add_user_without_token(self):
        # 需要添加的新用户
        new_user_data = {
            "username": "noauthtokenuser@example.com",
            "password": "NoAuthTokenUser123"
        }

        # 发送添加用户请求
        response = self.app.post('/admin/add_user',
                                 data=json.dumps(new_user_data),
                                 content_type='application/json')

        # 检查状态代码和响应消息
        self.assertEqual(response.status_code, 403)
        self.assertIn('Admin access required', response.data.decode())

if __name__ == "__main__":
    unittest.main()
