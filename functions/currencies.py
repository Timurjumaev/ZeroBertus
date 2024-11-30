from utils.db_operations import save_in_db
from models.currencies import Currencies
from utils.pagination import pagination


def get_currencies(ident, status, page, limit, db):

    if ident > 0:
        ident_filter = Currencies.id == ident
    else:
        ident_filter = Currencies.id > 0

    if status is None:
        status_filter = Currencies.id > 0
    elif status:
        status_filter = Currencies.status == True
    else:
        status_filter = Currencies.status == False

    items = db.query(Currencies).filter(ident_filter, status_filter).order_by(Currencies.id.desc())

    return pagination(items, page, limit)


def create_currency_f(form, db):
    old_currency = db.query(Currencies).filter(Currencies.status == True).first()
    if old_currency:
        db.query(Currencies).filter(Currencies.id == old_currency.id).update({
            Currencies.status: False
        })
        db.commit()
    new_item_db = Currencies(
        price=form.price,
    )
    save_in_db(db, new_item_db)



