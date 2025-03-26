import MySQLdb
def get_connection():
    return MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="",
        db="hackathon"
    )


