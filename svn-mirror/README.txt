svn mirror
----------

quick and dirty script to safely mirror the contents of a
subversion repository for re-export by apache. 

--if repo is down, mirror remains unchanged
--contents are mirrored into offline directory, and symlink is 
swapped atomically (in order to guarantee consistency). 
--logs activities