from mongoengine import Document, StringField, ListField, ReferenceField


class Author(Document):
    name = StringField(required=True, max_length=80)
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField(required=True)
    author = ReferenceField(Author)
    quote = StringField(required=True)
