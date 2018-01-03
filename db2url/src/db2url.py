import MySQLdb

from ConfigParser import ConfigParser
# Read in config file
config=ConfigParser()
config.read(['/home/jhover/devel/db2url/config/db2url.conf' ])


MIMEHTML="text/html"
MIMETXT="text/plain"
MIMEJPG="image/jpeg"
MIMESGML="text/sgml"
    
def dbquery(req,tables=None,columns=None):
    from mod_python import Session 
    from mod_python import util 
    from mod_python import psp 
    from mod_python import apache 
    
    req.content_type=MIMETXT
    req.add_common_vars()
    
    database = config.get('global','dbdatabase')
    conn = MySQLdb.connect( host=config.get('global','dbhost'),
                            user=config.get('global','dbuser'),
                            passwd=config.get('global','dbpassword'),
                            db=database
                            )
    cur=conn.cursor()
    cur.execute('SHOW TABLES;')
    alltables = cur.fetchall()
    actual_tables = []
    for item in alltables:
        actual_tables.append(item[0])
        # actual tables is now a Python list of strings.
    
    req.write("tables=%s" % actual_tables)
    
    tabledesc = {}
    
    for table in actual_tables:
        cur.execute('desc %s' % table)
        allcolumns = cur.fetchall()
        actual_columns = []
        for item in allcolumns:
            actual_columns.append(item[0])
        tabledesc[table] = actual_columns    
        #req.write("table= %s columns=%s" % (table, actual_columns))
    
    if tables:
        desired_tables= tables.split(",")
    else:
        desired_tables= actual_tables
   
    for t in desired_tables:
        req.write("desired=%s\n" % t)
    
    if columns:
        desired_columns = columns.split(",")
    else:
        desired_columns = actual_columns
    
    for c in desired_columns:
        req.write("desired=%s\n" % c)
    
    #req.write("Database '%s' selected.\n" % database )
    #req.write("Table '%s' selected.\n" % table)
    for table in desired_tables:
        req.write("desired=%s\n" % table)
        cur.execute("select * from %s ;" % table)
        rows = cur.fetchall()
        for row in rows:
            rowlength=len(row)
            for i in range(rowlength):
                req.write("%s" % row[i])
                if (i + 1) < rowlength :
                    req.write(",")    
            req.write('\n')

def _check_access(req,table,column):
    tablestr = config.get(database,'allowed_tables' )
    allowed_tables = tablestr.split(",")
    req.write("table:%s is allowed...\n" % table)
    for t in allowed_tables:
        req.write("allowed=%s\n"% t)  
#        else:
#            req.write("table:%s is not in allowed: %s\n" % (table, allowed_tables))

def _sanitize_name(sqlstring):
    OK_CHARS = "abcdefghijklmnopqrstuvwxyz0123456789 .,!?:"
    if [x for x in sqlstring if x.lower() not in OK_CHARS] == []:
        return sqlstring
    else:
        raise Exception("Bad character in SQL")
    

def test(req):
    return "OK"

def status(req):
    from mod_python import Session 
    from mod_python import util 
    from mod_python import psp 
    from mod_python import apache 
    import modpystatus 

    req.content_type="text/html" 
    req.add_common_vars() 
    r=modpystatus.modPyStats() 
    r.status(req) 
    req.write(r.page) 
    return apache.OK 