"""Configuración del proyecto.

Si 'mysqlclient' no se pudo instalar (a veces pasa en Windows con versiones muy nuevas de
Python), usamos 'PyMySQL' como sustituto: pip install pymysql
"""
try:
    import MySQLdb  # noqa: F401
except ImportError:
    try:
        import pymysql

        pymysql.version_info = (2, 2, 1, "final", 0)
        pymysql.install_as_MySQLdb()
    except ImportError:
        pass
