class MessageType:
    INFO = "info"
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"


def message(en: str, fa: str = None, type: str = MessageType.INFO):
    return {
        "message_en": en,
        "message_fa": fa if fa else en,
        "message_type": type,
    }


default_not_found_message = message(
    en="Instance not found!",
    fa="مورد درخواستی یافت نشد!",
    type=MessageType.ERROR,
)

default_forbidden_message = message(
    en="Access to this object is denied!",
    fa="دسترسی به این بخش برای شما امکان پذیر نیست!",
    type=MessageType.ERROR,
)

default_created_message = message(
    en="Object created successfully!",
    fa="با موفقیت اضافه شد!",
    type=MessageType.SUCCESS,
)

default_deleted_message = message(
    en="Object deleted successfully!",
    fa="با موفقیت حذف شد!",
    type=MessageType.INFO,
)


default_edited_message = message(
    en="Object edited successfully!",
    fa="با موفقیت ویرایش شد!",
    type=MessageType.INFO,
)
