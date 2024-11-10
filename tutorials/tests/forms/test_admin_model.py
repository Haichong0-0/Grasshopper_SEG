from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

import datetime

from tutorials.forms import SignUpForm 

class AdminSignUpFormTestCase(TestCase):
    def setUp(self):
        self.form_input = {
            'first_name': "Doe",
            'last_name': "John",
            'username': "@Doe123",
            'email': "Doe@gmail.com",
            'date_of_birth':datetime.datetime(2024, 11, 1),
            'bio': "admin",
            'new_password': "Joe$$$123",
            'password_confirmation': "Joe$$$123",
        }

    def test_valid_form(self):
        form = SignUpForm(data=self.form_input)
        print(form.errors)
        self.assertTrue(form.is_valid())
    
    def test_blank_first_name_is_invalid(self):
        self.form_input['first_name'] = ""
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # def test_first_name_is_empty(self):
    #     self.form_input['first_name'] = " "
    #     form = SignUpForm(data=self.form_input)
    #     self.assertFalse(form.is_valid())

    # def test_blank_first_name_number(self):
    #     self.form_input['first_name'] = "6"
    #     form = SignUpForm(data=self.form_input)
    #     self.assertFalse(form.is_valid())

    # def test_blank_first_name_is_symbol(self):
    #     self.form_input['first_name'] = "&"
    #     form = SignUpForm(data=self.form_input)
    #     self.assertFalse(form.is_valid()

    def test_overlong_first_name_is_invalid(self):
        self.form_input['first_name'] = 'x' * 60
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_blank_last_name_is_invalid(self):
        self.form_input['first_name'] = ""
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_last_name_is_empty(self):
        self.form_input['first_name'] = " "
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_overlong_first_name_is_invalid(self):
        self.form_input['first_name'] = 'x' * 60
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_overlong_last_name_is_invalid(self):
        self.form_input['last_name'] = 'x' * 60
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
