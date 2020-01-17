
class TrainingResource:

    # 培训资源
    @classmethod
    def open_training_resource(cls, session, open_training_resource_url):
        return session.get(open_training_resource_url)

    # 查询：培训资源
    @classmethod
    def query_training_resource(cls, session, query_training_resource_url, query_training_resource_info):
        return session.post(query_training_resource_url, query_training_resource_info)

    # 新增： add_training_resource
    @classmethod
    def add_training_resource(cls, session, add_training_resource_url, add_training_resource_info):
        return session.post(add_training_resource_url, add_training_resource_info)

    # 废弃 abandon_training_resource
    @classmethod
    def abandon_training_resource(cls, session, abandon_training_resource_url, abandon_training_resource_info):
        return session.post(abandon_training_resource_url, abandon_training_resource_info)

    # 跟踪（查看简历）  query_abandon
    @classmethod
    def query_abandon_resource(cls, session, query_resource_url, query_resource_info):
        return session.post(query_resource_url, query_resource_info)

    # 跟踪（跟踪资源）
    @classmethod
    def tracking_resource(cls, session, tracking_resource_url, tracking_resource_info):
        return session.post(tracking_resource_url, tracking_resource_info)

    # 跟踪（跟踪资源）
    @classmethod
    def Modify_resource(cls, session, Modify_resource_url, Modify_resource_info):
        return session.post(Modify_resource_url, Modify_resource_info)