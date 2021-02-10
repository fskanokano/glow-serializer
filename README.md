# glow-serializer

#### Glow-Serializer
    Glow-Serializer is a lightweight ORM serializer, compatible with mainstream ORM.


#### Installing

    pip install glow-serializer

#### A Simple Example

    import peewee
    
    from glow_serializer import Serializer, NestedField
    
    database = peewee.MySQLDatabase(
        # Your database name.
        # 'xxxxx',
        host='localhost',
        user='root',
        password='123456',
        port=3306,
    )
    
    
    class User(peewee.Model):
        username = peewee.CharField()
        nickname = peewee.CharField()
    
        class Meta:
            database = database
    
    
    class Book(peewee.Model):
        name = peewee.CharField()
        price = peewee.IntegerField()
        user = peewee.ForeignKeyField(User, backref='books')
    
        class Meta:
            database = database
    
    
    class UserSerializer(Serializer):
        class Meta:
            fields = ['id', 'username', 'nickname']
    
    
    class BookSerializer(Serializer):
        user = NestedField(UserSerializer(exclude=['id']))
    
        class Meta:
            fields = ['id', 'name', 'price', 'user']
    
    
    class ReverseBookSerializer(Serializer):
        class Meta:
            fields = ['id', 'name', 'price']
    
    
    class ReverseUserSerializer(Serializer):
        books = NestedField(ReverseBookSerializer(many=True))
    
        class Meta:
            fields = ['id', 'username', 'nickname', 'books']
    
    
    if __name__ == '__main__':
        # Create tables
        # database.connect()
        # database.create_tables([User, Book])
    
        books = Book.select().where(Book.id != 0)
        data1 = BookSerializer().dumps(books, many=True)
        print(data1)

        users = User.select().where(User.id != 0)
        data2 = ReverseUserSerializer().dumps(users, many=True)
        print(data2)
    
