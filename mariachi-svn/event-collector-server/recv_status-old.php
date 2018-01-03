<?php
	$outdir = '/data/www/html/data/';
	$logfile = '/data/www/html/data/recv_status.log';

	$siteid = trim($_POST['site_id']);
	$status = trim($_POST['status']);

	if (strstr($siteid, "..") !== FALSE) {
		$logstring = date("Y.m.d  H:i:s  ") . "Site id " . $siteid . " from " .  $_SERVER["REMOTE_ADDR"] . " contains ..\n";
		$handle = fopen($logfile, "a");
		$result = fwrite($handle, $logstring);
		fclose($handle);
	} else {
		$lastfile = $outdir . $siteid . "_last_status";
		$handle = fopen($lastfile, "w+");
		$result = fwrite($handle, $status . "\n");
		fclose($handle);

		$statusfile = $outdir . $siteid . "_status";
		$handle = fopen($statusfile, "r+");
		$old_status = fgets($handle);
		fclose($handle);
		$old_status = trim($old_status);
		if ($old_status <> $status) {
			$handle = fopen($statusfile, "w+");
			rewind($handle);
			$result = fwrite($handle, $status);
			fclose($handle);
		}

		$msgfile = $outdir . $siteid . "_status_msg";

		$result = 0;
		if (filesize($msgfile) > 17000) {
			$lines = file($msgfile);
			array_shift($lines);
			$handle = fopen($msgfile, "w");
			$result = fwrite($handle, join('', $lines));
			fclose($handle);
		}

		$handle = fopen($msgfile, "a+");
		$result = fwrite($handle, time() . "  " . $status . "\n");
		fclose($handle);



	}
?>
