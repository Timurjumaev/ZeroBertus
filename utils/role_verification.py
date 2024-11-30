from fastapi import HTTPException


def role_verification(user, function):
    not_allowed_functions_for_admins = ["create_user", "update_user", "delete_user", "create_permission"]

    if user.role == "boss":
        return True

    if user.role == "admin" and function not in not_allowed_functions_for_admins:
        return True

    raise HTTPException(status_code=401, detail='Sizga ruhsat berilmagan!')

