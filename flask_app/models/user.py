from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
user_db = 'user_passwords'


class User:
    # Might need to add in more variables
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.login = data['login']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def full_name(self): return self.first_name + " " + self.last_name

    @classmethod
    def save(cls, data):
        query = '''
        INSERT INTO users 
        ( first_name, last_name, email, password, login, 
        created_at, updated_at )
        VALUES ( %(first_name)s, %(last_name)s, %(email)s,
        %(password)s, 1, NOW(), NOW() );
        '''
        return connectToMySQL(user_db).query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(user_db).query_db(query, data)
        # print(result)
        return cls(result[0])

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(user_db).query_db(query, data)
        if len(result) < 1: return False
        return cls(result[0])

    @staticmethod
    def validate_user(user):
        is_valid = True
        print(user)
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            is_valid = False
        elif User.get_by_email(user) is not False:
            flash("There's already a user please login instead.")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if user['password_conf'] != user['password']:
            flash("Passwords don't match.")
            is_valid = False
        return is_valid
