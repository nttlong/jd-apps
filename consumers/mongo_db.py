import pymongo.database


def get_db(app_name) -> pymongo.database.Database:
    """
    lấy mongodb database dựa vào cấu hình trong re_process.config
    :param app_name:
    :return:
    """
    import ReCompact.db_context
    import config
    db = ReCompact.db_context.get_db_connection(
        host=config.mongo_db_config["host"],
        password=config.mongo_db_config["password"],
        username=config.mongo_db_config["username"],
        authSource=config.mongo_db_config["authSource"],
        replicaSet=config.mongo_db_config["replicaSet"],
        authMechanism=config.mongo_db_config["authMechanism"],
        port=config.mongo_db_config["port"]

    ).get_database(app_name)
    return db
