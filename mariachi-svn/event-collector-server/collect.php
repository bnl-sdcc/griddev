<?php
	$uploaddir = '/data/data/hs/';
	$logfile = '/data/www/html/data/log';

	$source = $_FILES['userfile']['tmp_name'];
	$sourcename = $_FILES['userfile']['name'];
	$siteid = trim($_POST['siteid']);

	if ((strstr($siteid, "..") !== FALSE) || (strstr($sourcename, "..") !== FALSE))
		$logstring = "site id \"$siteid\" contains \"..\"\n";
	else {
		$dest = $uploaddir . $siteid . $sourcename;

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
