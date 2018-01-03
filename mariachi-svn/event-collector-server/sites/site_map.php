<html>

<head>
<meta http-equiv="refresh" content="60">
<meta http-equiv="Content-Type" content="text/html; charset=windows-1252">
<title></title>
</head>

<body>
<?php
  $site = $_REQUEST['site'];
  echo '<p><a href="site_status.php?site=' . $site . '" target="_blank"><img border="0"'; 
  if (file_exists("../" . $site . "_last_event")) {
    if (time() < (filemtime("../" . $site . "_last_event") + 120)) {
      echo 'src="' . $site . 'recent.gif"';
    } elseif (time() > (filemtime("../" . $site . "_last_status") + 900)) {
      echo 'src="' . $site . 'offline.gif"';
    } else {
      $handle = fopen("../" . $site . "_last_status", "r", 1024);
      if ($handle) {
        $status = trim(fgets($handle));
        fclose($handle);
        if ($status == "active") {
          echo 'src="' . $site . 'active.gif"';
        } else {
          echo 'src="' . $site . 'offline.gif"';
        }
      } else {
        echo 'src="' . $site . 'offline.gif"';
      }
    }
  } else {
    echo 'src="' . $site . 'offline.gif"';
  }
  switch ($site) {
  case "BNLB":
    $width = 33; 
    $height = 26;
    $title = "Brookhaven Lab";
    break;
  case "BWHS":
    $width = 19;
    $height = 80;
    $title = "Brentwood HS";
    break;
  case "DPHS":
    $width = 22;
    $height = 80;
    $title = "Deer Park HS";
    break;
  case "GCHS":
    $width = 23;
    $height = 80;
    $title = "Garden City HS";
    break;
  case "HPHS":
    $width = 16;
    $height = 80;
    $title = "Hauppauge HS";
    break;
  case "MPHS":
    $width = 15;
    $height = 80;
    $title = "Mepham HS";
    break;
  case "RPHS":
    $width = 54; 
    $height = 30;
    $title = "Rocky Point High School";
    break;
  case "RVHS":
    $width = 19;
    $height = 80;
    $title = "Roosevelt HS";
    break;
  case "SBRK":
    $width = 26;
    $height = 30;
    $title = "Stony Brook Univ.";
    break;
  case "SCCC":
    $width = "24"; 
    $height = "26"; 
    $title = "Suffolk County CC";
    break;
  case "SEHS":
    $width = 27;
    $height = 26;
    $title = "Sachem East HS";
    break;
  case "SMHS":
    $width = 25;
    $height = 26;
    $title = "Smithtown HS";
    break;
  case "WMHS": 
    $width = 29; 
    $height = 30;
    $title = "Ward Melville High School";
    break;
  default:
    $width = 10; 
    $height = 10;
    $title = "UNKNOWN";
  }
  echo 'width="' . $width . '" height="' . $height . '" title="' . $title . '"></a></p>';
?> 

</body>

</html>
