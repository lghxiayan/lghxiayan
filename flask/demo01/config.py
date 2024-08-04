DB_CONFIG = {
    'host': '192.168.112.13',
    'port': '3306',
    'user': 'flask',
    'password': 'nCybeJ5tKidDS8B8',
    'database': 'flask',
    'charset': 'utf8mb4'
}
DB_URI = (f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
          f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}?charset=utf8")
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
