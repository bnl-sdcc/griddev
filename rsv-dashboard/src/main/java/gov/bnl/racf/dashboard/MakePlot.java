package gov.bnl.racf.dashboard;

import java.io.*;
import javax.servlet.*;
import org.jfree.*;
import org.jfree.chart.*;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.JFreeChart;
import org.jfree.data.xy.XYSeries;
import org.jfree.data.xy.XYDataset; 
import org.jfree.data.xy.XYSeriesCollection;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.chart.axis.ValueAxis;
import org.jfree.chart.axis.NumberAxis;
import org.jfree.chart.axis.DateAxis;
import org.jfree.chart.plot.XYPlot;
import org.jfree.chart.renderer.xy.StandardXYItemRenderer;

public class MakePlot
{  
    String moduleName="MakePlot";
    
    String imageDirectory="";
    String imageFileName="temporary_file_delete_it.jpg";
    String imageLocation=null;
    File imageFile=null;

    XYSeries series=null;


    public MakePlot( )
	{
	}

    public void setImageDirectory(String inputImageDirectory){
	imageDirectory=inputImageDirectory;
	System.out.println(moduleName+": imageDirectory="+imageDirectory);
	System.out.println("=====================");
    }
    
    public void setXandYData(XYSeries inputSeries){
	series=inputSeries;
    }

    public void makeImageFile(){

	imageLocation=imageDirectory+imageFileName;
	XYSeriesCollection xyDataset = new XYSeriesCollection(series);
	ValueAxis timeAxis = new DateAxis("Data"); 
	NumberAxis valueAxis = new NumberAxis("Throughput"); 
	valueAxis.setAutoRangeIncludesZero(false); 
	// override default 
	StandardXYItemRenderer renderer = new StandardXYItemRenderer( StandardXYItemRenderer.LINES); 

	XYPlot plot = new XYPlot(xyDataset, timeAxis, valueAxis, renderer); 

	//JFreeChart chart = new JFreeChart("", JFreeChart.DEFAULT_TITLE_FONT, plot, false); 
	JFreeChart chart = new JFreeChart("Throughput Plot",  plot); 
	chart.setBackgroundPaint(java.awt.Color.white); 

	/*
	//XYDataset xyDataset = new XYSeriesCollection(series);
	JFreeChart chart = ChartFactory.createXYLineChart
	//JFreeChart chart = ChartFactory.createXYAreaChart
                     ("Experimental XY Chart",  // Title
                      "X Axis",           // X-Axis label
                      "Y Axis",           // Y-Axis label
                      xyDataset,          // Dataset
		      PlotOrientation.VERTICAL,
                      true, true, false
                     );
	*/
	try{
	    imageFile = new File (imageLocation);
	    ChartUtilities.saveChartAsJPEG(imageFile,chart,500,300);
	}catch(Exception e){
	    System.out.println(moduleName+" failed to write output file to "+imageLocation);
	    System.out.println(e);
	}
    }

    public void makeImageFile2(){

	imageLocation=imageDirectory+imageFileName;

	XYDataset xyDataset = new XYSeriesCollection(series);
	JFreeChart chart = ChartFactory.createXYLineChart
	//JFreeChart chart = ChartFactory.createXYAreaChart
                     ("Experimental XY Chart",  // Title
                      "X Axis",           // X-Axis label
                      "Y Axis",           // Y-Axis label
                      xyDataset,          // Dataset
		      PlotOrientation.VERTICAL,
                      true, true, false
                     );
	try{
	    imageFile = new File (imageLocation);
	    ChartUtilities.saveChartAsJPEG(imageFile,chart,500,300);
	}catch(Exception e){
	    System.out.println(moduleName+" failed to write output file to "+imageLocation);
	    System.out.println(e);
	}
    }

    public String imageFileInHtml(){
	String result="";
	System.out.println(moduleName+": imageLocation="+imageLocation);
	System.out.println("=====================");
	result="<img style=\"width: 750px; height: 450px;\" alt=\"alternate text\" src=\""+ imageFileName +"\">";
	return result;
    }


    public static String linkToDemoPlot(String imageDir){
	XYSeries series2 = new XYSeries("Average Size");
	series2.add(20.0, 10.0);
	series2.add(40.0, 20.0);
	series2.add(70.0, 50.0);
	XYDataset xyDataset = new XYSeriesCollection(series2);
	JFreeChart chart = ChartFactory.createXYAreaChart
                     ("Demo plot2",  // Title
                      "Height",           // X-Axis label
                      "Weight",           // Y-Axis label
                      xyDataset,          // Dataset
		      PlotOrientation.VERTICAL,
                      true, true, false
                     );

	String returnString="";
	
	try{
	    File dir1 = new File (".");
	    returnString=returnString+dir1.getCanonicalPath()+"<br>";

	    String imageFile=imageDir+"/temp.chart.jpg";
	    ChartUtilities.saveChartAsJPEG(new File(imageFile), chart, 750, 450);
	    returnString="<img style=\"width: 750px; height: 450px;\" alt=\"alternate text\" src=\"temp.chart.jpg\">";


	}catch (Exception e){
	    returnString="Failed to open temporary file";
	}
	return returnString;

    }
    public static String getCurrentDir(){
	String result="CurrentDirectory:";
	try{
	File dir1 = new File (".");
	result=result+dir1.getCanonicalPath()+"<br>";
	}catch (Exception e){
	    result=result+"FAILED";
	}
	return result;
    }

}
