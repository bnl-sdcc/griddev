<?php
  include ("jpgraph/src/jpgraph.php");
  include ("jpgraph/src/jpgraph_bar.php");
  include ("jpgraph/src/jpgraph_line.php");
  include ("jpgraph/src/jpgraph_date.php");

  $site = $_REQUEST['site'];
  $archdir = "../../../../data/hs/";

// Old events
  $count[0] = 0;
  $day[0] = 0;
  $i = 0;
  $archives = glob($archdir . $site . "*");

  if (count($archives) <= 0) {
    $graph = new Graph(600, 400, "auto");
    $graph->SetScale("textlin");
    $graph->SetTickDensity(TICKD_VERYSPARSE);
    $graph->img->SetMargin(40,40,40,80);		
    $graph->SetShadow();
    $graph->SetMarginColor("powderblue");
    $graph->title->Set("Daily Event Counts (Archived Events)", "low");
    $graph->title->SetFont(FF_FONT1,FS_BOLD);
    
    $data = array(0, 0);
    $bp1 = new BarPlot($data);
    
    $txt2 = new Text("NO ARCHIVED EVENTS");
    $txt2->Pos(250, 150);
    $txt2->SetColor("black");
    $txt2->SetFont(FF_FONT1,FS_BOLD);

    $graph->Add($bp1);
    $graph->AddText($txt2);
    $graph->Stroke();
    exit;
  }




  foreach ($archives as $oldfile) {
    $lines = file($oldfile);
    foreach ($lines as $value) {
      $value = trim($value);
      if (strcspn($value, "0123456789 /:.UTC") == 0) {
        $d = substr($value, 0, 10);
        if (($j = array_search($d, $day)) !== FALSE) {
          $count[$j]++; 
        } else {
	  $i++;
	  $day[$i] = $d;
          $count[$i] = 1;
	}
      }
    }
  }

// clean out some crap
array_shift($day);
array_shift($count);
foreach ($day as $key => $value) {
  $day[$key] = strtotime($day[$key]);
}

$graph = new Graph(600, 400, "auto");
//$graph->SetScale("textlin");
$graph->SetScale("datlin");
$graph->SetTickDensity(TICKD_VERYSPARSE);
$graph->img->SetMargin(40,40,40,80);		
$graph->SetShadow();
$graph->SetMarginColor("powderblue");
$graph->title->Set("Daily Event Counts (Archived Events)", "low");
$graph->title->SetFont(FF_FONT1,FS_BOLD);
$graph->xaxis->SetTitle("Date", "middle");
$graph->xaxis->SetTitleMargin(35);
$graph->xaxis->scale->SetDateFormat("M d");
$graph->xaxis->title->SetFont(FF_FONT1,FS_BOLD);
$graph->xaxis->SetLabelAngle(90);
//$graph->xaxis->HideTicks(true, true);
$graph->yaxis->title->SetFont(FF_FONT1,FS_BOLD);
$graph->yaxis->SetTitle("Events/Day", "middle");

$bp1 = new BarPlot($count, $day);
$bp1->SetFillGradient("palegreen4", "palegreen", GRAD_HOR);
$bp1->SetWidth(60000);

$graph->Add($bp1);
$graph->Stroke();

?>

