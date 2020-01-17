
class Transferee:

    # 打开转让责任人模块
    @classmethod
    def open_trans_feree(cls, session, open_trans_feree_url):
        return session.get(open_trans_feree_url)

    # 查询
    @classmethod
    def query_trans_feree(cls, session, query_trans_feree_url, query_trans_feree_info):
        return session.post(query_trans_feree_url, query_trans_feree_info)

    # 查看
    @classmethod
    def show_resume(cls, session, show_resume_url, show_resume_info):
        return session.post(show_resume_url, show_resume_info)

    # 查询页数
    @classmethod
    def switch_page(cls, session, switch_page_url, switch_page_info):
        return session.post(switch_page_url, switch_page_info)

    # 提交
    @classmethod
    def submit_trans(cls, session, submit_url, submit_info):
        return session.post(submit_url, submit_info)
