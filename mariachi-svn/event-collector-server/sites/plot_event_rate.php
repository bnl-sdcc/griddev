<?php
  include ("jpgraph/src/jpgraph.php");
  include ("jpgraph/src/jpgraph_bar.php");
  include ("jpgraph/src/jpgraph_date.php");

  $site = $_REQUEST['site'];
  
  $timearray = localtime();
  $hour[24] = mktime($timearray[2], 0, 0);
  for ($i = 23; $i >= 0; $i--) {
    $hour[$i] = $hour[$i + 1] - 3600;
  }
  for ($i = 0; $i <= 23; $i++) {
    $ecount[$i] = 0;
  }
  if (file_exists("../" . $site . "_events")) {
    $lines = file("../" . $site . "_events");
    foreach ($lines as $value) {
      for ($i = 1; $i <= 23; $i++) {
        if (($value >= $hour[$i-1]) && ($value < $hour[$i])) { $ecount[$i]++; }
      }
    }
  }
  array_pop($hour);
  
$graph = new Graph(600, 400, "auto");
$graph->SetScale("datlin");
$graph->SetTickDensity(TICKD_VERYSPARSE);
$graph->img->SetMargin(40,40,40,60);		
$graph->SetShadow();
$graph->SetMarginColor("powderblue");
$graph->title->Set("Events/Hour During the Past 24 Hours", "low");
$graph->title->SetFont(FF_FONT1,FS_BOLD);
$graph->xaxis->SetTitle("Local Time", "middle");
$graph->xaxis->SetTitleMargin(25);
$graph->xaxis->title->SetFont(FF_FONT1,FS_BOLD);
$graph->xaxis->SetLabelAngle(90);
$graph->xaxis->HideTicks(true, true);
$graph->yaxis->title->SetFont(FF_FONT1,FS_BOLD);
$graph->yaxis->SetTitle("Events/Hour", "middle");

$bp1 = new BarPlot($ecount, $hour);
$bp1->SetFillGradient("palegreen4", "palegreen", GRAD_HOR);
$bp1->SetWidth(3000);

$graph->Add($bp1);
$graph->Stroke();

?>

