
struct srm_filestatus {
  char  *surl;
  char  *turl;
  int   fileid;
  int   status;
};

struct srm_filemetadata {
  char  *surl; 
  long  size;
  char  *owner;
  char  *group;
  int   permMode;
  char  *checksumType;
  char  *checksumValue;
  int   isPinned;
  int   isPermanent;
  int   isCached; 
};

int
srm_ping(char *srmep, char **errbuf);

int
srm_setfilestatus(char *srmep, int reqid, int fileid, char *state, char **errbuf);

int
srm_get(char *srmep, int nbfiles, char **surls, int nbprotocols, char **protocols,
        int *reqid, struct srm_filestatus **filestatuses, char **errbuf);

int
srm_put(char *srmep, int nbfiles, char **surls, int *filesizes, int nbprotocols, char **protocols,
        int *reqid, int **fileids, char **token, char ***turls, char **errbuf);

int
srm_getrequeststatus(char *srmep, int reqid,
                     struct srm_filestatus **filestatuses, char **errbuf);

int
srm_getfilemetadata(char *srmep, int nbfiles, char **surls, struct srm_filemetadata **metadata,
                    char **errbuf);

int
srm_pin(char *srmep, int nbfiles, char **surls,
        int *reqid, struct srm_filestatus **filestatuses, char **errbuf);

int
srm_unpin(char *srmep, int nbfiles, char **surls,
          int reqid, struct srm_filestatus **filestatuses, char **errbuf);
