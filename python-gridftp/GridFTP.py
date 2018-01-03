try:
    import libgridftp
except:
    import sys
    
    print "Fatal Error. SRM module failed to initialize."
    print "Please verify your environment!"
    sys.exit(2)


class GridFTPException(Exception):
    def __init__(self, val):
        self.m_val = """GridFTP exception: %s""" % val
    def __str__(self):
        return str(self.m_val)
 

def deleteFile(file):
    err = ''
    p_err = libgridftp.new_str_ptr()
    libgridftp.deletefile(file, p_err)
    if r != 0:
        err = libgridftp.str_ptr_value(p_err)
        libgridftp.delete_str_ptr(p_err)
        raise GridFTPException(err)


def getFileSize(file):
    p_size = libgridftp.new_long_ptr()
    p_err = libgridftp.new_str_ptr()
    r = libgridftp.getfilesize(file, p_size, p_err)
    if r != 0:
        err = libgridftp.str_ptr_value(p_err)
        libgridftp.delete_str_ptr(p_err)
        raise GridFTPException(err)
    siz = libgridftp.long_ptr_value(p_size)
    libgridftp.delete_long_ptr(p_size)
    return siz


def test():
    print "Try valid call to get file size:"
    try:
        print getFileSize('gsiftp://dcgftp.usatlas.bnl.gov/pnfs/usatlas.bnl.gov/data/prod/rome/datafiles/rome/simul/rome.004100.simul.T1_McAtNLO_top/rome.004100.simul.T1_McAtNLO_top._16837.pool.root.1')
    except Exception, e:
        print "Error occurred", str(e)
    print "Try invalid call to get file size:"
    try:
        print getFileSize('gsiftp://dcgftp.usatlas.bnl.gov/pnfs/usatlas.bnl.gov/data/prod/rome/datafiles/rome/simul/rome.004100.simul.T1_McAtNLO_top/rome.004100.simul.T1_McAtNLO_top._16837.pool.root.1.FAIL')
    except Exception, e:
        print "Error occurred", str(e)


if __name__ == '__main__':
    test()
