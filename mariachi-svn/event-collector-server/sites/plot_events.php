<?php
  include ("jpgraph/src/jpgraph.php");
  include ("jpgraph/src/jpgraph_scatter.php");
  include ("jpgraph/src/jpgraph_date.php");

  $site = $_REQUEST['site'];
  
  $now = time();
  $hourago = $now - 3600;
  $datax[0] = $now;
  $datay[0] = -1;
  if (file_exists("../" . $site . "_events")) {
    $lines = file("../" . $site . "_events");
    $i = 0;
    foreach ($lines as $value) {
      if (($value >= $hourago) && ($value < $now)) {
        $datax[$i] = trim($value);
        $datay[$i] = 1;
	$i++;
      }
    }
  }

$graph = new Graph(600,200,"auto");
$graph->SetScale("datlin", 0, 2, $hourago, $now);
$graph->SetTickDensity(TICKD_VERYSPARSE);
$graph->xgrid->Show(true);
$graph->ygrid->Show(false);
$graph->img->SetMargin(40,40,40,40);		
$graph->SetMarginColor("powderblue");
$graph->SetShadow();

$graph->title->Set("Events During the Past Hour");
$graph->title->SetFont(FF_FONT1,FS_BOLD);
$graph->xaxis->SetTitle("Local Time", "middle");
$graph->xaxis->title->SetFont(FF_FONT1,FS_BOLD);
$graph->xaxis->scale->SetTimeAlign(MINADJ_5);
$graph->yaxis->HideTicks();
$graph->yaxis->HideLabels();

$sp1 = new ScatterPlot($datay,$datax);
$sp1->mark->SetType(MARK_IMG_LBALL, "red", 0.5);

$graph->Add($sp1);
$graph->Stroke();

?>

