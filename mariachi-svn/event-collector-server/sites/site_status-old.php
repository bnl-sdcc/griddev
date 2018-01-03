<?php
  $site = $_REQUEST['site'];
  switch ($site) {
  case "BNLB":
    $url = "http://cosmicray.bnl.gov/";
    $site_name = "Brookhaven Lab";
    $user = "Takai";
    $user_name = "Helio Takai";
    break;
  case "BWHS":
    $title = "Brentwood HS";
    $url = "http://www.brentwood.k12.ny.us/HTMLpages/HighSchool/hsindex.html";
    $site_name = "Brentwood High School";
    $user = "Rebeccabrentwood";
    $user_name = "Rebecca Grella";
    break;
  case "DPHS":
    $title = "Deer Park HS";
    $url = "http://www.deerparkschools.org/news.php?blogid=14";
    $site_name = "Deer Park High School";
    $user = "Sundermier";
    $user_name = "Joe Sundermier";
    break;
  case "GCHS":
    $title = "Garden City HS";
    $url = "http://highschool.gardencity.k12.ny.us/";
    $site_name = "Garden City High School";
    $user = "Hasmort";
    $user_name = "Harry Stuckey";
    break;
  case "HPHS":
    $title = "Hauppauge HS";
    $url = "http://www.hauppauge.k12.ny.us/";
    $site_name = "Hauppauge High School";
    $user = "";
    $user_name = "Tara Newman";
    break;
  case "MPHS":
    $title = "Mepham HS";
    $url = "http://www.bellmore-merrick.k12.ny.us/mepham/index.htm";
    $site_name = "Mepham High School";
    $user = "Leacock";
    $user_name = "Bill Leacock";
    break;
  case "RPHS":
    $url = "http://www.rockypointschools.org/hspage.html";
    $site_name = "Rocky Point High School";
    $user = "Jspahn";
    $user_name = "Jeff Spahn";
    break;
  case "RVHS":
    $title = "Roosevelt HS";
    $url = "http://www.rooseveltufsd.com/";
    $site_name = "Roosevelt High School";
    $user = "Mahyarn";
    $user_name = "Mahyar Nikpour";
    break;
  case "SBRK":
    $title = "Stony Brook Univ.";
    $url = "http://stonybrook.edu/";
    $site_name = "Stony Brook University";
    $user = "Marx";
    $user_name = "Michael Marx";
    break;
  case "SCCC":
    $title = "Suffolk County CC";
    $url = "http://www3.sunysuffolk.edu/index.asp";
    $site_name = "Suffolk County Community College";
    $user = "Inglism";
    $user_name = "Mike Inglis";
    break;
  case "SEHS":
    $title = "Sachem East HS";
    $url = "http://www.sachem.edu/schools/east/";
    $site_name = "Sachem East High School";
    $user = "Rgearns";
    $user_name = "Richard Gearns";
    break;
  case "SMHS":
    $title = "Smithtown HS";
    $url = "http://www.smithtown.k12.ny.us/highschl/";
    $site_name = "Smithtown High School";
    $user = "Jrodichok";
    $user_name = "Joe Rodichok";
    break;
  case "WMHS": 
    $url = "http://www.3villagecsd.k12.ny.us/schools/wardmelville.asp";
    $site_name = "Ward Melville High School";
    $user = "Azart715";
    $user_name = "Tanya Entwistle";
    break;
  default:
    echo "<h1>Unknown Site ID: " . $site . "</h1>";
    return;
  }
  echo '
    <html>

    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=windows-1252">
    <title>';
  
  echo $site_name . " Scintillator Site Status";

  echo '</title>
    </head>

    <body background="paper.gif">
    <br>
    <table border=0 width=100%>
    <tr>
      <td width=80></td>
    <td>';

  echo '<font size=6><b><a href="' . $url . '">' . $site_name;
  echo "</a> Scintillator Site</b></font><br>";
  echo "at " . date("H:i T, j F Y");

// Status information
  echo "<h2>Status</h2>";

  if (file_exists("../" . $site . "_last_status")) {
    $last_time = filemtime("../" . $site . "_last_status");
    if (time() > ($last_time + 900)) {
      $status = "Offline";
      $status_date = date("H:i T, j F Y", $last_time + 300);  
    } else {
      $handle = fopen("../" . $site. "_last_status", "r", 1024);
      if ($handle) {
        $status = trim(fgets($handle));
        $status = ucfirst($status);
        fclose($handle);
      } else {
        $status = "Offline";
      }
      $status_date = date("H:i T, j F Y", filemtime("../" . $site . "_status"));  
    }
    $last_status_date = date("H:i T, j F Y", filemtime("../" . $site . "_last_status"));  
  
    echo " <ul>
            <li>
  	      $status since $status_date
	    </li>
	    <li>
              Last status message received at $last_status_date
	    </li>
          </ul>";
  } else {
    echo "<ul><li>No status information available</li?></ul>";
  }

 // Events information
  echo "<h2>Events</h2>
          <ul>";

  if (file_exists("../" . $site . "_events")) {
    $lines = file("../" . $site . "_events");
    $hourago = time() - 3600;
    $count = 0;
    foreach ($lines as $value) {
      if ($value >= $hourago) { $count++; }
    }
    if ($count == 1) {
      $count_events = "1 event ";
    } else {
      $count_events = $count . " events ";
    }
    echo "<li>$count_events received in the past hour</li>";
  } else {
    echo "<li>No recent events file found</li>";
  } 
  
  if (file_exists("../" . $site . "_last_event")) {
    $last_event_date = date("H:i T, j F Y", filemtime("../" . $site . "_last_event")) ;  
    echo "<li>Last event received at $last_event_date</li>";
  } else {
    echo "<li>No latest event found</li>";
  }
      
  $files = glob("../../../../data/hs/" . $site . "*");
  if (count($files) <> 0) {
    rsort($files);
    $latest = substr(basename($files[0]), 4, 10);
    $stamp = gmmktime(substr($latest, 6, 2), substr($latest, 8, 2), 0, substr($latest, 2, 2), substr($latest, 4, 2), substr($latest, 0, 2));
    $last_file_date = date("H:i T, j F Y", $stamp);
    echo "<li>Last event file received at $last_file_date </li>";
  } else {
    echo "<li>No event files found</li>";
  }
  echo "</ul>";
  echo "<img src=plot_events.php?site=$site>";
  echo "<br><br>";
  echo "<img src=plot_event_rate.php?site=$site>";
  echo "<br><br>";
  echo "<img src=plot_daily_rate.php?site=$site>";
  echo "<br><br>";
  echo "<img src=plot_status_msg.php?site=$site>";
  echo "<br>";
  echo 'Contact: <a href="http://www-mariachi.physics.sunysb.edu/wiki/index.php/User:';
  echo $user . '">' . $user_name . "</a>";
?>
</td>
</tr>
</table>
</body>

</html>

