from mongoengine import Document, StringField, BooleanField
from flask_admin.contrib.mongoengine import ModelView
from flask_login import UserMixin
from config import *

__, admin, __ = start()


class User(Document, UserMixin):
    username = StringField(required=True, unique=True)
    name = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True)
    is_active = BooleanField(default=True)
    is_authenticated = BooleanField(default=True)
    is_anonymous = BooleanField(default=True)

    def __str__(self):
        return self.username


class UserView(ModelView):
    column_list = ('username', 'name','email')
    form_columns = ('username', 'name' ,'email', 'password')


@login_manager.user_loader
def load_user(user_id):
    return User.objects.get(id=user_id)


admin.add_view(UserView(User))