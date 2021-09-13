"""
Додати для усіх таблиць із бази даних моделі для валідації.
Додати валідацію полів та даних для методів GET/UPDATE/DELETE
"""

import re
import unittest
from pprint import pprint
# REdEX paterns

name_pattern = r'^([a-zA-Zа-щА-ЩЬьЮюЯяЇїІіЄєҐґ]+)\-?([a-zA-Zа-щА-ЩЬьЮюЯяЇїІіЄєҐґ]+)$'
email_pattern = r'^([a-zA-Z0-9-_\*\.]+)@([a-zA-Z0-9-]+)(\.[a-zA-Z0-9]+)+$'
password_pattern = r'^((?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{6,}))|((?=.*[a-z])(?=.*[A-Z])(?=.*[^A-Za-z0-9])(?=.{8,}))$'
phone_pattern = r'^\+\d{12}$'
date_pattern = r'^([0-3]?[0-9])(\.|\-|\/)([0-1]?[0-9])(\.|\-|\/)(\d{4})$'
address_pattern = r"^[A-Za-z0-9'\.\-\s\,]{10,}$"
product_pattern = r"^[A-Za-z0-9'\.\-\s]{2,}$"
role_pattern = r'^(admin|customer|superAdmin)$'
number_pattern = r'^\d+\.?[0-9]*$'
img_pattern = r'^([A-Za-z0-9\_\-\.\S])+[\.](jpg|png|jpeg)$'

# models
USERS = {
    "id": [int, number_pattern],
    "first_name": [str, name_pattern],
    "last_name": [str, name_pattern],
    "date_of_bitrth": [str, date_pattern],
    "phone": [str, phone_pattern],
    "address": [str, address_pattern],
    "password": [str, password_pattern],
    "email": [str, email_pattern],
    "role": [str, role_pattern],
    "discount": [int, number_pattern]
}
ORDERS = {
    "id": [int, number_pattern],
    "date_of_order": [str, date_pattern],
    "customer_id": [int, number_pattern],
    "product_id": [int, number_pattern],
    "price": [float, number_pattern],
    "count": [int, number_pattern],
    "discount": [int, number_pattern],
    "total": [float, number_pattern],
}
PRODUCT = {
    "id": [int, number_pattern],
    "code": [int, number_pattern],
    "product_name": [str, product_pattern],
    "unit_price": [float, number_pattern],
    "count": [int, number_pattern],
    "description": [str, address_pattern],
    "img": [str, img_pattern],
    "sub_category_id": [int, number_pattern],
}
SUBCATEGORY = {
    "id": [int, number_pattern],
    "sub_category_name": [str, product_pattern],
    "category_id": [int, number_pattern],
}
CATEGORY = {
    "id": [int, number_pattern],
    "category_name": [str, product_pattern],

}
SELECT_TABLE = {
    'users': USERS,
    'orders': ORDERS,
    'product': PRODUCT,
    'product_subcategory': SUBCATEGORY,
    'product_category': CATEGORY,
}


class Validate(unittest.TestCase):
    def validate(self, request, model, model_name):
        for key in request:
            self.assertIn(key, model,
                          f'Field "{key}" is not in {model_name} model. Incorrect field name!')
            self.assertIsInstance(request[key], model[key][0],
                                  f'Field "{key}" has invalid data type for {model_name} model, it must been {model[key][0].__name__}. Type error!')
            value = request[key].strip() if isinstance(
                request[key], str) else str(request[key])
            self.assertRegex(value, model[key][1],
                             f'Field "{key}" has incorrect value for {model_name} model. Value error!')

    def validate_table(self, table, model, column_table):

        column = [item for key in model for item in model[key]]
        first_word = re.findall(r'\w+', column_table)[0]

        self.assertIn(table, model.keys(
        ),  f'Field "{table}" is not in {model.keys()} model. Incorrect field name!')
        self.assertIn(first_word, column,
                      f'Field "{first_word}" is not in {table} model. Incorrect field name!')


if __name__ == '__main__':

    admin_1_data = [{
        "first_name": "Bob",
        "last_name": "Bobb",
        "date_of_bitrth": "2-5-1684",
        "phone": "+380123456789",
        "address": "Some  15 st. 17 app.",
        "password": "Qwewe123!3",
        "email": "opa@mail.dog",
        "role": "admin",
        "discount": 0
    }]
    orders_data = [{
        "date_of_order": '2-5-2020',
        "customer_id": 1,
        "product_id": 2,
        "price": 1256.0,
        "count": 2,
        "discount": 10,
        "total": 2712.0,
    }]

    product_data = [{
        "code": 25694,
        "product_name": 'table',
        "unit_price": 1256.3,
        "count": 10,
        "description": 'table for kitchen',
        "img": 'table-1.jpg',
        "sub_category_id": 4,
    }]
    subcategory_data = [{
        "sub_category_name": 'table kithen',
        "category_id": 7,
    }]
    category_data = [{
        "category_name": 'kithen',
    }]


# admin_1 = Admin('Bad','BOB')
# admin_1.add_admin(admin_1_data)
# rez = re.search(re.compile(name_pattern), "Bob")
# print(rez)
# -----------------------------------------------------------------
# Validate().validate(admin_1_data[0], USERS, 'users')
# Validate().validate(orders_data[0], ORDERS, 'orders')
# Validate().validate(product_data[0], PRODUCT, 'product')
# Validate().validate(subcategory_data[0],
#                     SUBCATEGORY, 'product_subcategory')
# Validate().validate(category_data[0], CATEGORY, 'category')
# -----------------------------------------------------------------
# Validate().validate_table('users', SELECT_TABLE, "category_name = 'wardrobe'")
# -----------------------------------------------------------------
# admin_1 = SuperAdmin('opa@mail.dog', '123fff$FG')
# admin_1.add_admin(admin_1_data)

# for key in admin_1_data[0]:
#     print(key)

# for value in admin_1_data[0].items():
# for value, key in enumerate(admin_1_data[0]):
#     print(value, key, admin_1_data[0][key])
# print(SELECT_TABLE.keys())
# print(SELECT_TABLE.values())
# if SELECT_TABLE.keys() == 'users':
#     print(SELECT_TABLE.values())
# # c = [i for i in range(1, 11) if i % 2 == 0]
# model = [SELECT_TABLE[key] for key in SELECT_TABLE if key == 'product_subcategory']

# column = [item for key in SELECT_TABLE for item in SELECT_TABLE[key]]

# for item in model:
#     print(item)

# s = 'category_name = wardrobe'
# s = 'category_name'
# first_word = re.findall(r'\w+', s)[0]
# print(first_word)
