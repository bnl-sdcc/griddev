<?php
	$outdir = '/data/www/html/data/';
	$logfile = '/data/www/html/data/recv_status.log';

	$siteid        = trim($_POST['site_id']);
	$status        = trim($_POST['status']);
	$lastMsgTime   = trim($_POST['lastMsgTime']);
	$timingStatus  = trim($_POST['timingStatus']);
	$antennaStatus = trim($_POST['antennaStatus']);
	$timingRef     = trim($_POST['timingRef']);
	$ettStatus     = trim($_POST['ettStatus']);
	$ettMsg        = trim($_POST['ettMsg']);

	if (strstr($siteid, "..") !== FALSE) {
		$logstring = date("Y.m.d  H:i:s  ") . "Site id " . $siteid . " from " .  $_SERVER["REMOTE_ADDR"] . " contains ..\n";
		$handle = fopen($logfile, "a");
		$result = fwrite($handle, $logstring);
		fclose($handle);
	} else {
	
                if ($timingStatus == "not_valid") { $status = "offline"; }
                if ($antennaStatus == "fault") { $status = "offline"; }
                if ($timingRef == "not_ready") { $status = "offline"; }
                if ($ettStatus == "off") { $status = "offline"; }
	
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
		$line = $status . "  " . $lastMsgTime . "  " . $timingStatus . "  " . $antennaStatus;
		$line .= "  " . $timingRef . "  " . $ettStatus . "  " . $ettMsg;
		$result = fwrite($handle, time() . "  " . $line . "\n");
		fclose($handle);
                
//		$handle = fopen($msgfile . "_x", "a+");
//		$result = fwrite($handle, time() . "  ");
//		foreach ($_POST as $key => $value) {
//		    $line = $key . "=" . trim($value) . " ";
//		    $result = fwrite($handle, $line);
//		}
//		$result = fwrite($handle, "\n");
//		fclose($handle);

	}
?>
