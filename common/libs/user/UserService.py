import hashlib, base64, random, string


class UserService():

    @staticmethod
    def geneAuthCode(user_info):
        m = hashlib.md5()
        str = "%s-%s-%s" % (user_info.id, user_info.user_name, user_info.password)
        m.update(str.encode('utf-8'))
        return m.hexdigest()

    @staticmethod
    def genePwd(pwd, salt):
        m = hashlib.md5()
        str = "%s-%s" % (base64.encodebytes(pwd.encode("utf-8")), salt)
        m.update(str.encode('utf-8'))
        return m.hexdigest()

    @staticmethod
    def geneSalt(length=16):
        keylist = random.choices(string.ascii_letters + string.digits, k=16)
        return ''.join(keylist)
