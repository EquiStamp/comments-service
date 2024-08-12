from comments.settings import DB_USERNAME, DB_PASSWORD, DB_ENDPOINT, DB_PORT, DB_NAME


def make_connection_string():
    return f"mariadb+mariadbconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_ENDPOINT}:{DB_PORT}/{DB_NAME}"
