import sys
try:
    import libsrm
except:
    print "Fatal Error. SRM module failed to initialize."
    print "Please verify your environment!"
    sys.exit(2)


class SRMException(Exception):
    def __init__(self, val):
        self.m_val = """SRM exception: %s""" % val
    def __str__(self):
        return str(self.m_val)

    
 
def srmGet(srmep, surls, prots):
    """SRM v1.1 GET
    srmep: SRM endpoint
    surls: python list with SURLs
    prots: python list with protocols to use for GET request

    Return: Tuple with (Request ID, File Structure)
            Request ID is an integer
            File Structure is a vector of dictionaries with:
              'surl', 'turl', 'fileid', 'status'
              status: 1 READY; -1 FAILED; 0 PENDING
    """

    p_err = libsrm_v1_1.new_str_ptr()
    p_reqid = libsrm_v1_1.new_int_ptr()
    p_fs = libsrm_v1_1.new_fslist_ptr()
    p_surls = libsrm_v1_1.new_str_array(len(surls))
    for i in range(0, len(surls)):
        libsrm_v1_1.str_array_setitem(p_surls, i, surls[i])
    p_prots = libsrm_v1_1.new_str_array(len(prots))
    for i in range(0, len(prots)):
        libsrm_v1_1.str_array_setitem(p_prots, i, prots[i])
    r = libsrm_v1_1.srm_get(srmep, len(surls), p_surls, len(prots), p_prots,
                            p_reqid, p_fs, p_err)
    if r < 0:
        err = libsrm_v1_1.str_ptr_value(p_err)
        libsrm_v1_1.delete_str_ptr(p_err)
        raise SRMException(err)
    fs = []

    ptr = libsrm_v1_1.fslist_array_getitem(p_fs, 0)
    for i in range(0, r):
        f = libsrm_v1_1.fs_array_getitem(ptr, i)
        if f.status == 1:
            fs.append( { 'surl': f.surl, 'turl': f.turl,
                         'fileid': f.fileid, 'status': f.status } )
        else:
            fs.append( { 'surl': f.surl, 'turl': '',
                         'fileid': f.fileid, 'status': f.status } )

    reqid = libsrm_v1_1.int_ptr_value(p_reqid)
    libsrm_v1_1.delete_int_ptr(p_reqid)
    libsrm_v1_1.delete_fslist_ptr(p_fs)
    libsrm_v1_1.delete_str_array(p_surls)
    libsrm_v1_1.delete_str_array(p_prots)
    return (reqid, fs)
 
 
def srmPut(srmep, surls, fsizes, prots):
    
    p_err = libsrm_v1_1.new_str_ptr()
    p_reqid = libsrm_v1_1.new_int_ptr()
    p_fsizes = libsrm_v1_1.new_int_array(len(fsizes))
    p_fileids = libsrm_v1_1.new_intlist_ptr()
    token = libsrm_v1_1.new_str_ptr()
    p_turls = libsrm_v1_1.new_strlist_ptr()
 
    p_surls = libsrm_v1_1.new_str_array(len(surls))
    for i in range(0, len(surls)):
        libsrm_v1_1.str_array_setitem(p_surls, i, surls[i])
 
    p_prots = libsrm_v1_1.new_str_array(len(prots))
    for i in range(0, len(prots)):
        libsrm_v1_1.str_array_setitem(p_prots, i, prots[i])
 
    for i in range(0, len(fsizes)):
        libsrm_v1_1.int_array_setitem(p_fsizes, i, fsizes[i])
 
    r = libsrm_v1_1.srm_put(srmep, len(surls), p_surls, p_fsizes, len(prots),
                            p_prots, p_reqid, p_fileids, token, p_turls, p_err)
    if r < 0:
        err = libsrm_v1_1.str_ptr_value(p_err)
        libsrm_v1_1.delete_str_ptr(p_err)
        raise SRMException(err)
 
    fileids = []
    ptr = libsrm_v1_1.intlist_array_getitem(p_fileids, 0)
    for i in range(0, r):
        fileids.append( libsrm_v1_1.int_array_getitem(ptr, i) )
    libsrm_v1_1.delete_int_ptr(ptr)
    libsrm_v1_1.delete_intlist_ptr(p_fileids)
 
    turls = []
    ptr = libsrm_v1_1.strlist_array_getitem(p_turls, 0)
    for i in range(0, r):
        turls.append( libsrm_v1_1.str_array_getitem(ptr, i) )
    libsrm_v1_1.delete_str_ptr(ptr)
    libsrm_v1_1.delete_strlist_ptr(p_turls)
 
    reqid = libsrm_v1_1.int_ptr_value(p_reqid)
    token = libsrm_v1_1.str_ptr_value(token)
    libsrm_v1_1.delete_int_ptr(p_reqid)
    libsrm_v1_1.delete_str_ptr(token)
    libsrm_v1_1.delete_int_array(p_fsizes)
    libsrm_v1_1.delete_str_array(p_surls)
    libsrm_v1_1.delete_str_array(p_prots)
    return (reqid, fileids, token, turls)
 
 
def srmGetRequestStatus(srmep, reqid):
    """Return File Structure (see srmGet)"""
    
    p_err = libsrm_v1_1.new_str_ptr()    
    p_fs = libsrm_v1_1.new_fslist_ptr()
    r = libsrm_v1_1.srm_getrequeststatus(srmep, reqid, p_fs, p_err)
    if r < 0:
        err = libsrm_v1_1.str_ptr_value(p_err)
        libsrm_v1_1.delete_str_ptr(p_err)
        raise SRMException(err)
   
    fs = []
    ptr = libsrm_v1_1.fslist_array_getitem(p_fs, 0)
    for i in range(0, r):
        f = libsrm_v1_1.fs_array_getitem(ptr, i)
        if f.status == 1:
            fs.append( { 'surl': f.surl, 'turl': f.turl,
                         'fileid': f.fileid, 'status': f.status } )
        else:
            fs.append( { 'surl': f.surl, 'turl': '',
                         'fileid': f.fileid, 'status': f.status } )
                                                                                                                   
    libsrm_v1_1.delete_fslist_ptr(p_fs)
    return fs


def srmGetFileMetaData(srmep, surls):
    """Return File Meta Data"""

    p_err = libsrm_v1_1.new_str_ptr()
    p_fmd = libsrm_v1_1.new_fmdlist_ptr()
    p_surls = libsrm_v1_1.new_str_array(len(surls))
    for i in range(0, len(surls)):
        libsrm_v1_1.str_array_setitem(p_surls, i, surls[i])
    r = libsrm_v1_1.srm_getfilemetadata(srmep, len(surls), p_surls, p_fmd, p_err)
    if r < 0:
        err = libsrm_v1_1.str_ptr_value(p_err)
        libsrm_v1_1.delete_str_ptr(p_err)
        raise SRMException(err)
    
    fm = []
    ptr = libsrm_v1_1.fmdlist_array_getitem(p_fmd, 0)
    for i in range(0, r):
        f = libsrm_v1_1.fmd_array_getitem(ptr, i)
        fm.append( { 'surl': f.surl, 'size': f.size,
                     'owner': f.owner, 'group': f.group,
                     'permMode': f.permMode, 'checksumType': f.checksumType,
                     'checksumValue': f.checksumValue, 'isPinned': f.isPinned,
                     'isPermanent': f.isPermanent, 'isCached': f.isCached } )
    libsrm_v1_1.delete_fmdlist_ptr(p_fmd)
    return fm
 
 
def srmSetFileStatus(srmep, reqid, fileid, status):
    return libsrm_v1_1.srm_setfilestatus(srmep, reqid, fileid, status)
 
 
def srmSetFileStatusDone(srmep, reqid, fileid):
    return srmSetFileStatus(srmep, reqid, fileid, "Done")
 
 
def srmSetFileStatusRunning(srmep, reqid, fileid):
    return srmSetFileStatus(srmep, reqid, fileid, "Running")
 

def srmPin(srmep, surls):

    p_err = libsrm_v1_1.new_str_ptr()
    p_reqid = libsrm_v1_1.new_int_ptr()
    p_fs = libsrm_v1_1.new_fslist_ptr()
    p_surls = libsrm_v1_1.new_str_array(len(surls))
    for i in range(0, len(surls)):
        libsrm_v1_1.str_array_setitem(p_surls, i, surls[i])
    r = libsrm_v1_1.srm_pin(srmep, len(surls), p_surls,
                            p_reqid, p_fs, p_err)
    if r < 0:
        err = libsrm_v1_1.str_ptr_value(p_err)
        libsrm_v1_1.delete_str_ptr(p_err)
        raise SRMException(err)
    
    fs = []
    ptr = libsrm_v1_1.fslist_array_getitem(p_fs, 0)
    for i in range(0, r):
        f = libsrm_v1_1.fs_array_getitem(ptr, i)
        if f.status == 1:
            fs.append( { 'surl': f.surl, 'turl': f.turl,
                         'fileid': f.fileid, 'status': f.status } )
        else:
            fs.append( { 'surl': f.surl, 'turl': '',
                         'fileid': f.fileid, 'status': f.status } )

    reqid = libsrm_v1_1.int_ptr_value(p_reqid)
    libsrm_v1_1.delete_int_ptr(p_reqid)
    libsrm_v1_1.delete_fslist_ptr(p_fs)
    libsrm_v1_1.delete_str_array(p_surls)
    return (reqid, fs)


def srmUnPin(srmep, reqid, surls):

    p_err = libsrm_v1_1.new_str_ptr()
    p_fs = libsrm_v1_1.new_fslist_ptr()
    p_surls = libsrm_v1_1.new_str_array(len(surls))
    for i in range(0, len(surls)):
        libsrm_v1_1.str_array_setitem(p_surls, i, surls[i])
    r = libsrm_v1_1.srm_unpin(srmep, len(surls), p_surls,
                              reqid, p_fs, p_err)
    if r < 0:
        err = libsrm_v1_1.str_ptr_value(p_err)
        libsrm_v1_1.delete_str_ptr(p_err)
        raise SRMException(err)
    
    fs = []
    ptr = libsrm_v1_1.fslist_array_getitem(p_fs, 0)
    for i in range(0, r):
        f = libsrm_v1_1.fs_array_getitem(ptr, i)
        if f.status == 1:
            fs.append( { 'surl': f.surl, 'turl': f.turl,
                         'fileid': f.fileid, 'status': f.status } )
        else:
            fs.append( { 'surl': f.surl, 'turl': '',
                         'fileid': f.fileid, 'status': f.status } )

    libsrm_v1_1.delete_fslist_ptr(p_fs)
    libsrm_v1_1.delete_str_array(p_surls)
    return fs

