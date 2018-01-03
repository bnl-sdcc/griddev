To lock a set of files:

1) find <full-path-name-of-the-target-dir> -type f
redirect the results to a file <file1>
2) ./refresh_dcache_ssh_process &
3) ./dcache_file_lock ./<file1>
The result is in file <file>_table

Then you may want to try several times for the step 3)
to lock all files.
