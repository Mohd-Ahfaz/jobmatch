import pymysql

pymysql.install_as_MySQLdb()

# Bypass MySQL 8.4+ requirement in newer Django versions for MySQL 8.0.x
try:
    from django.db.backends.base.base import BaseDatabaseWrapper
    BaseDatabaseWrapper.check_database_version_supported = lambda self: None
    from django.db.backends.mysql.features import DatabaseFeatures
    DatabaseFeatures.minimum_database_version = (8, 0)
except Exception:
    pass
