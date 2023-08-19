from utils import messages

invalid_credentials_error = {
    "message_en": "Invalid credentials!",
    "message_fa": "رمز عبور اشتباه است.",
}

no_such_user_error = {
    "message_en": "No such user!",
    "message_fa": "کاربری با این نام کاربری یافت نشد",
}


authorization_bad_request_error = messages.message(
    en="Please submit valid parameters",
    fa="پارامتر های داده شده صحیح نمی باشند",
    type=messages.MessageType.ERROR,
)
wrong_key_path_error = messages.message(
    en="Requested key path does not exists",
    fa="کلید دسترسی درخواست شده وجود ندارد",
    type=messages.MessageType.ERROR,
)
invalid_token_error = messages.message(
    en="Access token is not valid",
    fa="توکن وارد شده معتبر شده است",
    type=messages.MessageType.INFO,
)

no_access_to_path_error = messages.message(
    en="User not authorized to access this action",
    fa="دسترسی به این بخش برای شما امکانپذیر نیست",
    type=messages.MessageType.ERROR,
)
