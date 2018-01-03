<?php
	$outdir = '/data/www/html/data/';
	$logfile = '/data/www/html/data/recv_new_event.log';

	$siteid = trim($_POST['site_id']);
	$event_time = trim($_POST['event_time']);

	if (strstr($siteid, "..") !== FALSE) {
		$logstring = date("Y.m.d  H:i:s  ") . "Site id " . $siteid . " from " .  $_SERVER["REMOTE_ADDR"] . " contains ..\n";
		$handle = fopen($logfile, "a");
		$result = fwrite($handle, $logstring);
		fclose($handle);
	} else {
		$lastfile = $outdir . $siteid . "_last_event";
		$handle = fopen($lastfile, "w+");
		$result = fwrite($handle, $event_time . "\n");
		fclose($handle);

		$eventfile = $outdir . $siteid . "_events";

//		$result = 0;
//		if (filesize($eventfile) > 2640) {
//			$lines = file($eventfile);
//			array_shift($lines);
//			$handle = fopen($eventfile, "w");
//			$result = fwrite($handle, join('', $lines));
//			fclose($handle);
//		}

		$handle = fopen($eventfile, "a+");
		$result = fwrite($handle, $event_time . "\n");
		fclose($handle);
	}

?>
