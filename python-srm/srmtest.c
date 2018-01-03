#include "libsrm_v1_1.h"

/* Standalone C client for testing */

int main() {
  char **surls;
  char **prots;
  int reqid;
  struct srm_filestatus *fs;
  struct srm_filemetadata *fm;
  int j, i;

  surls = (char**)malloc(sizeof(char*)*2);
  surls[0] = (char*)malloc(sizeof(char)*200);
  surls[1] = (char*)malloc(sizeof(char)*200);
  prots = (char**)malloc(sizeof(char*));
  prots[0] = (char*)malloc(sizeof(char)*200);

  sprintf(surls[0], "srm://castorsrm.cern.ch:8443/castor/cern.ch/grid/atlas/f1");
  sprintf(surls[1], "srm://castorsrm.cern.ch:8443/castor/cern.ch/grid/atlas/f2");
  sprintf(prots[0], "gsiftp");

  printf("ping result %d\n", srm_ping("srm://castorsrm.cern.ch:8443"));

  j = srm_get("srm://castorsrm.cern.ch:8443", 2, surls, 1, prots, &reqid, &fs);
  printf("get count is %d\n", j);
  for (i=0; i<j; i++) {
    printf("SURL is %s\n", fs[i].surl);
    printf("STATUS is %d\n", fs[i].status);
    if (fs[i].status != 0)
      printf("TURL is %s\n", fs[i].turl);
  }

  j = srm_getfilemetadata("srm://castorsrm.cern.ch:8443", 2, surls, &fm);
  printf("getfilemetadata count is %d\n", j);
  for (i=0; i<j; i++) {
    printf("SURL is %s\n", fm[i].surl);
    printf("isPinned is %d\n", fm[i].isPinned);
    printf("size is %ld\n", fm[i].size);
  }
}
