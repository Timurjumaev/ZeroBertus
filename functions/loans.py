from utils.db_operations import save_in_db, get_in_db
from models.workers import Workers
from models.loans import Loans


def create_loan_f(form, db):
    get_in_db(db, Workers, form.worker_id)
    if db.query(Loans).filter(Loans.worker_id == form.worker_id).first():
        db.query(Loans).filter(Loans.worker_id == form.worker_id).update({
            Loans.total: Loans.total + form.total,
            Loans.residual: Loans.residual + form.total
        })
        db.commit()
    else:
        new_item_db = Loans(
            total=form.total,
            residual=form.total,
            worker_id=form.worker_id
        )
        save_in_db(db, new_item_db)



