<?php
	$uploaddir = '/data/www/html/data/sites2/';
	$logfile = '/data/www/html/data/recv__event_file.log';

	$source = $_FILES['userfile']['tmp_name'];
	$sourcename = $_FILES['userfile']['name'];
	$siteid = trim($_POST['site_id']);

	if ((strstr($siteid, "..") !== FALSE) || (strstr($sourcename, "..") !== FALSE))
		$logstring = date("Y.m.d  H:i:s  ") . "Site id " . $siteid . " from " .  $_SERVER["REMOTE_ADDR"] . " contains ..\n";
	else {
		$dest = $uploaddir . $sourcename;

		$logstring = date("Y.m.d  H:i:s  ") . "Upload of " . $sourcename . " from " .  $_SERVER["REMOTE_ADDR"] . " as " . $siteid . $sourcename;

		if (move_uploaded_file($source, $dest)) {
			chmod($dest, 0666);
			$logstring .= " succeeded.\n";
		} else {
			$logstring .= " FAILED.  Error code = " . $_FILES['userfile']['error'] . "\n";
		}
	}

	$handle = fopen($logfile, "a");
	$result = fwrite($handle, $logstring);
	fclose($handle)
?>
