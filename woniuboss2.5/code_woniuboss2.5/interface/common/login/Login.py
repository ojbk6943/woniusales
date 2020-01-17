
class Login:

    # 首页
    @classmethod
    def open_page(cls,session,url):
        return session.get(url)

    # 登录
    @classmethod
    def login(cls,session,url,login_info):
        return session.post(url, login_info)

    # 解密
    @classmethod
    def decode(cls, session, url, decodeinfo):
        return session.post(url, decodeinfo)
