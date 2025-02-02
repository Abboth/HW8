from mongoengine import StringField, BooleanField, Document, ReferenceField, IntField


class User(Document):
    name = StringField(required=True)
    age = IntField()


class UserContact(Document):
    user = ReferenceField(User)
    phone = StringField(required=True)
    email = StringField(required=True)
    contact_method_priority = StringField()


class Newsletter(Document):
    contact = ReferenceField(User)
    newsletter_status = BooleanField(default=False)
