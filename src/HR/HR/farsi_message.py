def successful_delete(subject):
    """ سابجکت باموفقیت پاک شد"""
    return {"message": f"{subject} با موفقیت پاک شد"}


def not_found(subject):
    """ سابجکت یافت نشد"""
    return {"message": f"{subject} یافت نشد"}
