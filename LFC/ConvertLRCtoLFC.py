import os
import MySQLdb
import lfc
import errno

os.environ['LFC_HOST']='lfc.usatlas.bnl.gov'
os.environ['LFC_CATALOG_TYPE']='lfc'
os.environ['LCG_GFAL_VO']='atlas'

def createPath(dname):
    #print "creating path for %s" % dname
    ans=1
    ans=lfc.lfc_mkdir(dname,0775)
    while ans != 0:
        if lfc.cvar.serrno == errno.EEXIST:
            ans=0
        else :
            # print'me'
            tmp=os.path.dirname(dname)
            print tmp
            if tmp.startswith('/grid/atlas/'):
                # print "creat sub directory %s" % tmp
                if createPath(tmp)==0:
                    ans=lfc.lfc_mkdir(dname,0775)
                else :
                    ans=1
                    break
            else :
                print "You can not make parent directory(%s) since it already exist. Creation failed." % tmp
                ans=1
                break        
            
    return ans


def lfc_create_path(dname):
    if not dname.startswith("/grid/atlas"):
        return -1
    
    parts = dname.split("/")
    n=N=len(parts)
    s=0
    while n>0:
        tmpName="/" + os.path.join(*parts[:n])
        s = lfc.lfc_mkdir(tmpName, 0775) 
        if s !=0 and lfc.cvar.serrno != errno.EEXIST:
            n=n-1
        else:
            break
        
    n = n+1
    while n<=N:
        tmpName="/" + os.path.join(*parts[:n])
        s = lfc.lfc_mkdir(tmpName, 0775)
        if s != 0:
            break
        else:
            n=n+1
            
    if n>N:
        if s==0:
            return 0
        elif lfc.cvar.serrno==errno.EEXIST:
            return 1
    else:
        return -1
            

db=MySQLdb.connect('lrc.usatlas.bnl.gov','dsdb-reader','dsdb-reader1','localreplicas')

cur=db.cursor()

cur.execute('select guid, md5sum, fsize, archival, adler32 from t_meta limit 200000')

rows=cur.fetchall()
counter=0
counter1=0
for fileinfo in rows:

    print "guid: %s, md: %s, fsize: %s, archival: %s, adler32: %s" % (fileinfo[0], fileinfo[1], fileinfo[2], fileinfo[3], fileinfo[4])
    counter=counter+1
    if (counter%100)==0:
        print "counter %d" % counter
        
    cur.execute('select l.lfname, p.pfname from t_lfn as l, t_pfn as p where l.guid=p.guid and l.guid=\'%s\'' % fileinfo[0])
    for filename in cur.fetchall():
        counter1=counter1+1
        
        if "srm://dcsrm.usatlas.bnl.gov" in filename[1] and "pnfs/usatlas.bnl.gov/" in filename[1]:
            lfn="/grid/atlas/" + os.path.dirname(filename[1].split("/pnfs/usatlas.bnl.gov/")[1]) + "/" + filename[0]
        
            ## try create file at first (it might fail with file exist or dir not exist, which will be dealt later.)
            s=lfc.lfc_creatg(lfn,fileinfo[0],0755)

            # check failure
            if s!=0:
                # lfn/guid exist, it is ok. just pretend it worked
                if lfc.cvar.serrno==errno.EEXIST:
                    s=0

                #directory does not exist, creat one at first.
                elif lfc.cvar.serrno==errno.ENOENT:
                    s=lfc_create_path(os.path.dirname(lfn))
                    #directory created successfully.
                    if s==0:
                        s=lfc.lfc_creatg(lfn,fileinfo[0],0755)

            # s is 0 if lfn information exists             
            if s==0:
                ## create pfn (or replica in LFC languate)

                fsizevlue=0
                if fileinfo[2] not in [None, '', 0,'NULL', 'exist:']:
                    #print "fszie %s : guid  %s" % (fileinfo[2][1], fileinfo[0])
                    try: 
                        fsizevalue=long(fileinfo[2])
                    except:
                        fsizevalue=0

                
                archival=fileinfo[3]
                if archival is None:
                    archival='P'

                #print "arhival=%s  ; guid%s" % (archival, fileinfo[0])
                s=lfc.lfc_addreplica(fileinfo[0],None,"dcsrm.usatlas.bnl.gov",filename[1],'-',archival,'','')
                if s!=0:
                    print "failed to add pfn for guid:%s   pfn:%s" % (fileinfo[1],filename[1])
                
                ## add file meta info.
                chsumtype=''
                chsumvalue=''
                if fileinfo[1] not in [None, '', 'NULL']:
                    chsumtype='MD'
                    chsumvalue=fileinfo[1]
                elif fileinfo[4] not in [None, '', 'NULL']:
                    chsumtype='AD'
                    chsumvalue=fileinfo[4]
                    
                s=lfc.lfc_setfsizeg(fileinfo[0],fsizevalue,chsumtype,chsumvalue)

                
                    
            
