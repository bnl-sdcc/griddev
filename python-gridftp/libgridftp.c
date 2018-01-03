/* Based on code from lcg_util */
#include <errno.h>
#include <stdlib.h>
#include <string.h>

#include <libgridftp.h>
#include <globus_gass_copy.h>

typedef struct {
  globus_mutex_t mutex;
  globus_cond_t cond;
  volatile globus_bool_t done;
  volatile globus_bool_t errflag;
  globus_object_t *error;
} monitor_t;


save_errmsg (char **errbuf, const char *errmsg)
{
  *errbuf = strdup(errmsg);
}


static void
gcallback (void *callback_arg, globus_ftp_client_handle_t *ftp_handle, globus_object_t *error)
{
  monitor_t *monitor = (monitor_t *) callback_arg;
  globus_mutex_lock (&monitor->mutex);
  if (error != GLOBUS_SUCCESS) {
    monitor->errflag = GLOBUS_TRUE;
    monitor->error = globus_object_copy (error);
  }
  monitor->done = GLOBUS_TRUE;
  globus_cond_signal (&monitor->cond);
  globus_mutex_unlock (&monitor->mutex);
}

int
deletefile (char *file, char **errbuf)
{
  return (deletefilet (file, errbuf, 0));
}

int
deletefilet (char *file, char **errbuf, int timeout)
{
  globus_ftp_client_handle_t ftp_handle;
  globus_ftp_client_handleattr_t ftp_handleattr;
  globus_ftp_client_operationattr_t ftp_op_attr;
  globus_result_t gresult;
  monitor_t monitor;
  char *p;
  int rc;
  struct timespec ts;

  globus_mutex_init (&monitor.mutex, NULL);
  globus_cond_init (&monitor.cond, NULL);
  monitor.done = GLOBUS_FALSE;
  monitor.errflag = GLOBUS_FALSE;
  rc = globus_module_activate (GLOBUS_FTP_CLIENT_MODULE);
  globus_ftp_client_handleattr_init (&ftp_handleattr);
  globus_ftp_client_handle_init (&ftp_handle, &ftp_handleattr);
  globus_ftp_client_operationattr_init (&ftp_op_attr);
  gresult = globus_ftp_client_delete (&ftp_handle, file, &ftp_op_attr,
                                      &gcallback, &monitor);
  globus_mutex_lock (&monitor.mutex);
  if (timeout) {
    ts.tv_sec = time (0) + timeout;
    ts.tv_nsec = 0;
    while (! monitor.done && time (0) < ts.tv_sec)
      globus_cond_timedwait (&monitor.cond, &monitor.mutex, &ts);
  } else
    while (! monitor.done)
      globus_cond_wait (&monitor.cond, &monitor.mutex);
  if (!monitor.done)
    globus_ftp_client_abort (&ftp_handle);
  globus_mutex_unlock (&monitor.mutex);
  globus_mutex_destroy(&monitor.mutex);
  globus_cond_destroy(&monitor.cond);
  globus_ftp_client_operationattr_destroy (&ftp_op_attr);
  globus_ftp_client_handle_destroy (&ftp_handle);
  globus_ftp_client_handleattr_destroy (&ftp_handleattr);
  (void) globus_module_deactivate (GLOBUS_FTP_CLIENT_MODULE);
  if (!monitor.done) {
    errno = ETIMEDOUT;
    goto err;
  }
  if (monitor.errflag == 0)
    return (0);
  p = globus_object_printable_to_string (monitor.error);
  if (strstr (p, "o such file"))
    errno = ENOENT;
  else if (strstr (p, "ermission denied") || strstr (p, "credential"))
    errno = EACCES;
  else
    errno = EINVAL;
 err:
  if (errno != ENOENT)
    save_errmsg (errbuf, p);
  globus_object_free (monitor.error);
  return (-1);
}



int
getfilesize (char *file, long *size, char **errbuf)
{
  return (getfilesizet (file, (globus_off_t *) size, errbuf, 0));
}


int
getfilesizet (char *file, globus_off_t *size, char **errbuf, int timeout)
{
  globus_ftp_client_handle_t ftp_handle;
  globus_ftp_client_handleattr_t ftp_handleattr;
  globus_ftp_client_operationattr_t ftp_op_attr;
  globus_result_t gresult;
  monitor_t monitor;
  char *p;
  int rc;
  struct timespec ts;
	
  globus_mutex_init (&monitor.mutex, NULL);
  globus_cond_init (&monitor.cond, NULL);
  monitor.done = GLOBUS_FALSE;
  monitor.errflag = GLOBUS_FALSE;
  rc = globus_module_activate (GLOBUS_FTP_CLIENT_MODULE);
  globus_ftp_client_handleattr_init (&ftp_handleattr);
  globus_ftp_client_handle_init (&ftp_handle, &ftp_handleattr);
  globus_ftp_client_operationattr_init (&ftp_op_attr);
  gresult = globus_ftp_client_size (&ftp_handle, file, &ftp_op_attr,
                                    size, &gcallback, &monitor);
  globus_mutex_lock (&monitor.mutex);
  if (timeout) {
    ts.tv_sec = time (0) + timeout;
    ts.tv_nsec = 0;
    while (! monitor.done && time (0) < ts.tv_sec) {
      globus_cond_timedwait (&monitor.cond, &monitor.mutex, &ts);
    }
  } else
    while (! monitor.done)
      globus_cond_wait (&monitor.cond, &monitor.mutex);
  if (!monitor.done) 
    globus_ftp_client_abort(&ftp_handle);
  globus_mutex_unlock (&monitor.mutex);
  globus_mutex_destroy(&monitor.mutex);
  globus_cond_destroy(&monitor.cond);
  globus_ftp_client_operationattr_destroy (&ftp_op_attr);
  globus_ftp_client_handle_destroy (&ftp_handle);
  globus_ftp_client_handleattr_destroy (&ftp_handleattr);
  (void) globus_module_deactivate (GLOBUS_FTP_CLIENT_MODULE);
  if (!monitor.done) {
    errno = ETIMEDOUT;
    goto err;
  }
  if (monitor.errflag == 0)
    return (0);
  p = globus_object_printable_to_string (monitor.error);
  if (strstr (p, "o such file"))
    errno = ENOENT;
  else if (strstr (p, "ermission denied") || strstr (p, "credential"))
    errno = EACCES;
  else
    errno = EINVAL;
 err:
  if (errno != ENOENT)
    save_errmsg (errbuf, p);
  globus_object_free (monitor.error);
  return (-1);
}
