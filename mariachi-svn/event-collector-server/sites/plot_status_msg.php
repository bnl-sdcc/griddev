<?php
  include ("jpgraph/src/jpgraph.php");
  include ("jpgraph/src/jpgraph_scatter.php");
  include ("jpgraph/src/jpgraph_date.php");

  $site = $_REQUEST['site'];
  
  $now = time();
  $dayago = $now - (3600 * 24);
  $activex[0] = $now;
  $activey[0] = -1;
  $offlinex[0] = $now;
  $offliney[0] = -1;
  if (file_exists("../" . $site . "_status_msg")) {
    $lines = file("../" . $site . "_status_msg");
    $a = 0;
    $o = 0;
    foreach ($lines as $value) {
      $timestamp = substr($value, 0, 10);
      $status = trim(substr($value, 12, 6));
      if (($timestamp >= $dayago) && ($timestamp < $now)) { 
        switch ($status) {
        case "active":
          $activex[$a] = trim($timestamp);
          $activey[$a] = 2;
          $a++;
          break;
        case "offlin":
          $offlinex[$o] = trim($timestamp);
          $offliney[$o] = 1;
          $o++;
          break;
        }
      }
    }
  }

$graph = new Graph(600,200,"auto");
$graph->SetScale("datlin", 0, 3, $dayago, $now);
$graph->SetTickDensity(TICKD_VERYSPARSE);
$graph->xgrid->Show(true);
$graph->ygrid->Show(false);
$graph->img->SetMargin(50,40,40,60);		
// $graph->SetMarginColor("lightgreen");
$graph->SetMarginColor("powderblue");
$graph->SetShadow();

$graph->title->Set($s, "low");
$graph->title->Set("Status Messages During the Past 24 Hours", "low");
$graph->title->SetFont(FF_FONT1,FS_BOLD);
$graph->xaxis->SetTitle("Local Time", "middle");
$graph->xaxis->SetTitleMargin(25);
$graph->xaxis->title->SetFont(FF_FONT1,FS_BOLD);
$graph->xaxis->SetLabelAngle(90);
//$graph->xaxis->SetLabelAlign("left");
$graph->xaxis->scale->SetDateFormat("H:i");
$graph->yaxis->HideTicks();
$graph->yaxis->HideLabels();

$txt1 = new Text("Active");
$txt1->Pos(5, 63);
$txt1->SetColor("black");

$txt2 = new Text("Offline");
$txt2->Pos(5, 98);
$txt2->SetColor("black");

$sp1 = new ScatterPlot($activey,$activex);
$sp1->mark->SetType(MARK_SQUARE);
$sp1->mark->SetColor("green");
$sp1->mark->SetFillColor("green");
$sp1->mark->SetWidth(2);

$sp2 = new ScatterPlot($offliney,$offlinex);
$sp2->mark->SetType(MARK_SQUARE);
$sp2->mark->SetColor("gray");
$sp2->mark->SetFillColor("gray");
$sp2->mark->SetWidth(2);

$graph->AddText($txt1);
$graph->AddText($txt2);
$graph->Add($sp1);
$graph->Add($sp2);
$graph->Stroke();
  
?>

