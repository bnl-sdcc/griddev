<?php
  include ("jpgraph/src/jpgraph.php");
  include ("jpgraph/src/jpgraph_pie.php");

  $site = $_REQUEST['site'];
  
  $now = time();
  $hourago = $now - (3600 * 24);
  $active = 0;
  $offline = 0;
  if (file_exists("../" . $site . "_status_msg")) {
    $lines = file("../" . $site . "_status_msg");
    $a = 0;
    $o = 0;
    foreach ($lines as $value) {
      $timestamp = substr($value, 0, 10);
      $status = trim(substr($value, 12));
      if (($timestamp >= $hourago) && ($timestamp < $now)) { 
        switch ($status) {
        case "active":
          $active++;
          break;
        case "offline":
          $offline++;
          break;
        }
      }
    }
  }

if (($active + $offline) < 12) {
  $nomsg = 12 - $active - $offline;
} else {
  $nomsg = 0;
}

$data = array($active, $offline, $nomsg);

$graph = new PieGraph(200,200);

$graph->title->Set("Status");
$graph->title->SetFont(FF_FONT1,FS_BOLD);

$p1 = new PiePlot($data);

$graph->Add($p1);
$graph->Stroke();
  
?>

