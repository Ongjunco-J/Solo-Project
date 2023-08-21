from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

db = "char_data_schema"
class Char:
    db = "char_data_schema"
    def __init__(self, data):
        self.id = data['id']
        self.char_class = data['char_class']
        self.sub_class = data['sub_class']
        self.race = data['race']
        self.sub_race= data['sub_race']
        self.background = data['background']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.player = None

    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM chars
                JOIN users on chars.user_id = users.id;
                """
        results = connectToMySQL(cls.db).query_db(query)
        all_chars = []
        for row in results:
            one_char = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password":row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            one_char.player = user.User(user_data)
            all_chars.append(one_char)
        return all_chars
    
    @classmethod
    def get_one_char_by_id(cls,data):
        query = """
                SELECT * FROM chars
                JOIN users on chars.user_id = users.id
                WHERE chars.id = %(id)s;
                """
        results = connectToMySQL(db).query_db(query,data)

        if not results:
            return False
        
        results = results[0]

        this_char = cls(results)

        user_data = {
                "id": results['users.id'],
                "first_name": results['first_name'],
                "last_name": results['last_name'],
                "email": results['email'],
                "password":results['password'],
                "created_at": results['users.created_at'],
                "updated_at": results['users.updated_at']
        }
        this_char.player = user.User(user_data)

        return this_char


    @classmethod
    def create_char_fighter(cls,data):
        query = """
                INSERT INTO chars (char_class,sub_class,race,sub_race,background,user_id)
                VALUES (%(char_class)s,%(sub_class)s,%(race)s,%(sub_race)s,%(background)s,%(user_id)s);
                """
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def create_char_race(cls,data):
        query = """
                INSERT INTO chars (race)
                VALUES (%(race)s);
                """
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def choose_char_race(cls,data):
        query = """
                UPDATE chars
                SET
                race = %(race)s,
                WHERE id = %(id)s;
                """
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def update_char(cls,data):
        query = """
                UPDATE chars
                SET
                sub_race = %(sub_race)s
                background = %(background)s
                WHERE id = %(id)s;
                """
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def create_char_options(cls, data):
        query = """
                INSERT INTO chars (sub_class,sub_race,background)
                VALUES (%(sub_class)s,%(sub_race)s,%(background)s);
                """
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def update_char(cls,data):
        query = """
                UPDATE chars
                SET char_class = %(char_class)s,
                sub_class = %(sub_class)s,
                race = %(race)s,
                sub_race = %(sub_race)s
                background = %(background)s
                WHERE id = %(id)s;
                """
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def delete_char(cls,data):
        query = """
                DELETE FROM chars
                WHERE id = %(id)s;
                """
        return connectToMySQL(cls.db).query_db(query,data)
    
    # @staticmethod
    # def validate_char(data):
    #     is_valid = True

    #     if len(data['char_class']) < 1:
    #         flash("All fields must be selected!.")
    #         is_valid = False
    #     if len(data['sub_class']) < 1:
    #         flash("All fields must be selected!")
    #         is_valid = False
    #     if len(data)['race'] < 1:
    #         flash("All fields must be selected!")
    #         is_valid = False
    #     if len(data['sub_race']) < 1:
    #         flash("All fields must be selected!")
    #         is_valid = False

        return is_valid