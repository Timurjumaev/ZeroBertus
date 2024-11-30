from routes.login import get_password_hash
from utils.db_operations import save_in_db
from models.users import Users


def get_user(usr):
    return usr


def create_user_f(form, db):
    new_item_db = Users(
        username=form.username,
        role=form.role,
        password=get_password_hash(form.password))
    save_in_db(db, new_item_db)


def update_user_own(usr, form, db):
    db.query(Users).filter(Users.username == usr.username).update({
        Users.username: form.username,
        Users.password: get_password_hash(form.password),
    })
    db.commit()


