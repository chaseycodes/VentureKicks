import sqlite3

DBNAME = 'shoebox.db'

def setDB(dbname):
    """opencursor.setDB() sets the default DBNAME for opencursor obj"""
    global DBNAME
    DBNAME = db

class OpenCursor:
    """imports sqlite3 functions into other files"""
    def __init__(self, db=None, *args, **kwargs):
        if db is None:
            db = DBNAME
        kwargs['check_same_thread'] = kwargs.get('check_same_thread',False)

        self.conn = sqlite3.connect(db,*args,**kwargs)
        #access results by coloumn name
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def __enter__(self):
        return self.cur
    
    def __exit__(self, extype, exvalue, extraceback):
        if not extype:
            self.conn.commit()
        self.cur.close()
        self.conn.close()
