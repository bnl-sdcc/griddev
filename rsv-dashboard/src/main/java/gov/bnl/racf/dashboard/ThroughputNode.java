package gov.bnl.racf.dashboard;

import java.sql.*;
import java.util.Calendar;
import java.io.*;

import java.awt.Color;

import java.util.Iterator;
import java.util.List;
import java.util.ArrayList;

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
import org.jfree.data.xy.DefaultTableXYDataset;


public class ThroughputNode
{  

    private String moduleName="ThroughputNode";

    private String source="";
    private String destination="";
    private String monitor="";


    
    private Timestamp state_time = null;
    public ProbeStatus status=null;
    private double throughput_min=0.0;
    private double throughput_max=0.0;
    private double throughput_avg=0.0;
    private double sigma=0.0;

    private String metricName="net.perfsonar.service.ma.throughput.";
    private ProbeStatus metricStatus = null; 
    private Timestamp timestamp = null;
    private String serviceType = null;
    private String serviceUri=null;
    private String gatheredAt=null;
    private String summaryData=null;
    private String detailsData = null;
    
    private String linkToNodeDetailPage=null;

    private ParameterBag parameterBag = null;

    private DbConnector db=null;

    private String initialisationSqlQuery="";
    private PreparedStatement initialisationSql=null;
    private PreparedStatement getHistoryPreparedSql=null;
    // lists which keep history information

    private ProbeStatus[] metricStatus_list = new ProbeStatus[1000];

    private Timestamp[] timestamp_list  = new Timestamp[1000];
    private String[] serviceType_list   = new String[1000];
    private String[] serviceUri_list    = new String[1000];
    private String[] gatheredAt_list    = new String[1000];
    private String[] summaryData_list   = new String[1000];
    private String[] detailsData_list   = new String[1000];

    private double[] throughput_min_list= new double[1000];
    private double[] throughput_max_list= new double[1000];
    private double[] throughput_avg_list= new double[1000];
    private double[] sigma_list         = new double[1000];

    private int numberOfHistoryRecords=0;

    String imageFileName="temporary_file_delete_it.jpg";
    private int imageXsize=500;
    private int imageYsize=300;

    File imageFile=null;

    List<ThroughputNodeRecord> history=new ArrayList<ThroughputNodeRecord>();


    public ThroughputNode(ParameterBag paramBag,  DbConnector inputDb,String inputSource, String inputDestination, String inputMonitor )
	{
	    parameterBag=paramBag;
	    db=inputDb;

	    source=inputSource;
	    destination=inputDestination;
	    monitor=inputMonitor;

	    metricName=metricName+source.replace(".","_")+"."+destination.replace(".","_");

	    /// create link to node detail page
	    ParameterBag paramBagLocal=(ParameterBag)paramBag.clone();
	    paramBagLocal.addParam("page",ParameterBag.pageAddress("Throughput Node")  );
	    paramBagLocal.addParam("src",source);
	    paramBagLocal.addParam("dst",destination);
	    paramBagLocal.addParam("mon",monitor);
	    linkToNodeDetailPage=paramBagLocal.makeLink();
	    	   
	    //=========== get information =======

	    //initialisationSqlQuery="select * from perfSONAR_throughput where src=? and dest=? and monitor=?";
	    //initialisationSqlQuery="select  * from MetricRecord where MetricName=? order by Timestamp DESC limit 1";
	    initialisationSqlQuery="select  * from MetricRecord where MetricName=? order by Timestamp DESC limit 1";
	    try{
		initialisationSql= db.getConn().prepareStatement(initialisationSqlQuery);
		//initialisationSql.setString(1,source);
		//initialisationSql.setString(2,destination);
		//initialisationSql.setString(3,monitor);
		initialisationSql.setString(1,metricName);		       
		
		ResultSet rs=initialisationSql.executeQuery();
	    	   
		while (rs.next ())
		    {
			metricStatus=new ProbeStatus(rs.getString("MetricStatus"));
			timestamp=rs.getTimestamp("Timestamp");
			serviceType=rs.getString("ServiceType");
			serviceUri =rs.getString("ServiceUri");
			gatheredAt =rs.getString("GatheredAt");
			summaryData=rs.getString("SummaryData");
			detailsData=rs.getString("DetailsData");
			
			StringBuffer detailsStringBuffer=new StringBuffer(detailsData);
			throughput_min=extractFloatFromStringBuffer(detailsStringBuffer,"min=","Gbps");
			throughput_max=extractFloatFromStringBuffer(detailsStringBuffer,"max=","Gbps");
			throughput_avg=extractFloatFromStringBuffer(detailsStringBuffer,"mean=","Gbps");
			sigma = extractFloatFromStringBuffer(detailsStringBuffer,"stddev=","Gbps");

		    }
	    }catch (Exception e){
		System.out.println(moduleName+" error occured when reading database");
		System.out.println(initialisationSqlQuery);
		System.out.println(metricName) ;   
		System.out.println(e);
	    }
	}

    public float extractFloatFromStringBuffer(StringBuffer inputStringBuffer, String startString, String endString){
	
	int startIndex=inputStringBuffer.indexOf(startString)+startString.length();
	int endIndex=inputStringBuffer.indexOf(endString,startIndex);
	
	String substring = inputStringBuffer.substring(startIndex,endIndex);
	float result = (Float.valueOf(substring) ).floatValue();  
	return result;
    }

    public HtmlTableCell veryShortStatusCell(){
	// return very short status table containing only status word and color
	// to be used in throughput matrix	

	HtmlLink link=new HtmlLink(linkToNodeDetailPage,metricStatus.statusWordShort());
	HtmlTableCell cell=new HtmlTableCell(link,metricStatus.color());
	return cell;
	
    }
    public HtmlTable veryShortHtmlTable(){
	HtmlTable ht=new HtmlTable(1);
	ht.addCell(veryShortStatusCell());
	return ht;
	
    }

    public HtmlTableCell shortStatusCell(){
	// return very short status table containing only status word and color
	// to be used in throughput matrix	

	HtmlLink link=new HtmlLink(linkToNodeDetailPage,metricName );
	HtmlTableCell cell=new HtmlTableCell(link,metricStatus.color());
	return cell;
	
    }
    public HtmlTable shortHtmlTable(){
	HtmlTable ht=new HtmlTable(1);
	ht.addCell(shortStatusCell());
	return ht;
	
    }

    public HtmlTable fullHtmlTable(){
	String result="";
	result="<strong>Source: </strong>"+source +"<br>";
	result=result+"<strong>Destination: </strong>"+destination +"<br>";
	result=result+"<strong>Monitor: </strong>"+monitor+"<br>";
	result=result+"<strong>Timestamp: </strong>"+timestamp+"<br>";
	result=result+"<strong>Throughput Min=</strong>"+throughput_min+"<br>";
	result=result+"<strong>Throughput Max=</strong>"+throughput_max+"<br>";
	result=result+"<strong>Throughput Avg=</strong>"+throughput_avg+"<br>";
	result=result+"<strong>Sigma=</strong>"+sigma+"<br>";
	result=result+"<strong>ServiceType: </strong>"+serviceType+"<br>";
	result=result+"<strong>ServiceUri: </strong>"+serviceUri+"<br>";

	result=result+"<strong>gatheredAt: </strong>"+gatheredAt+"<br>";
	result=result+"<strong>SummaryData: </strong>"+summaryData+"<br>";
	result=result+"<strong>DetailsData: </strong>"+detailsData+"<br>";

	//result=result+new HtmlLink(nagios_link, "Nagios page of this node").toHtml()+"<br>";
	
	// build the address to plot page
	/*
	ParameterBag temporaryParameterBag = (ParameterBag)parameterBag.clone();
	temporaryParameterBag.page=ParameterBag.pageAddress("Throughput Node History Plot");
	String urlOfPlotPage=temporaryParameterBag.makeLink();
	HtmlLink linkToPlotPage=new HtmlLink(urlOfPlotPage,"Link to history plot");
	result=result+linkToPlotPage.toHtml()+"<br>";
	*/

	
	// build the address to history table page
	ParameterBag temporaryParameterBag2 = (ParameterBag)parameterBag.clone();
	temporaryParameterBag2.page=SitePages.pageId("Throughput Node History Table");
	String urlOfHistoryTablePage=temporaryParameterBag2.makeLink();
	HtmlLink linkToHistoryTablePage=new HtmlLink(urlOfHistoryTablePage,"Link to history table");
	result=result+linkToHistoryTablePage.toHtml()+"<br>";

	// build the address to history plot page
	ParameterBag temporaryParameterBag3 = (ParameterBag)parameterBag.clone();
	temporaryParameterBag3.page=SitePages.pageId("Throughput Node History Plot");
	String urlOfHistoryTablePlot=temporaryParameterBag3.makeLink();
	HtmlLink linkToHistoryPlotPage=new HtmlLink(urlOfHistoryTablePlot,"Link to history plot");
	result=result+linkToHistoryPlotPage.toHtml()+"<br>";

	result=result+"query: "+initialisationSqlQuery;
       
	
	HtmlTableCell hc =new HtmlTableCell(result,metricStatus.color());
	hc.alignLeft();
	HtmlTable ht=new HtmlTable(1);
	ht.addCell(hc);

	return ht;	    	    		
    }


   
    public void getHistory(){
	String encodedSource = source.replace(".","_");
	String encodedDestination=destination.replace(".","_");
	String expectedMetricName="net.perfsonar.service.ma.throughput.SOURCE.DESTINATION";
	expectedMetricName=expectedMetricName.replace("SOURCE",encodedSource);
	expectedMetricName=expectedMetricName.replace("DESTINATION",encodedDestination);
	String expectedServiceUri="http://"+monitor+":8085/perfSONAR_PS/services/pSB";

	String getHistorySql="select  * from MetricRecord where MetricName=? and  ServiceUri=? ";

	IntervalSelector iS = new IntervalSelector(parameterBag);
	iS.setTimeVariable("Timestamp");
	iS.setTimeZoneShift(-4);
	getHistorySql=getHistorySql+" "+iS.buildQuery(parameterBag.interval);

	history.clear();

	try{
	    
	    getHistoryPreparedSql= db.getConn().prepareStatement(getHistorySql);
	    getHistoryPreparedSql.setString(1,expectedMetricName);
	    getHistoryPreparedSql.setString(2,expectedServiceUri);
	
	    ResultSet rs=getHistoryPreparedSql.executeQuery(); 

	    int count = 0;
	    while (rs.next ()){
		ThroughputNodeRecord historyRecord = new ThroughputNodeRecord();
		historyRecord.metricStatus = new ProbeStatus(rs.getString("MetricStatus"));
		historyRecord.timestamp    = rs.getTimestamp("Timestamp");
		historyRecord.serviceType  = rs.getString("ServiceType");
		historyRecord.serviceUri   = rs.getString("ServiceUri");
		historyRecord.gatheredAt   = rs.getString("GatheredAt");
		historyRecord.summaryData  = rs.getString("SummaryData");
		historyRecord.detailsData  = rs.getString("DetailsData");
		
		StringBuffer detailsStringBuffer=new StringBuffer(historyRecord.detailsData);
		historyRecord.throughput_min = (double)extractFloatFromStringBuffer(detailsStringBuffer,"min=","Gbps");
		historyRecord.throughput_max = (double)extractFloatFromStringBuffer(detailsStringBuffer,"max=","Gbps");
		historyRecord.throughput_avg = (double)extractFloatFromStringBuffer(detailsStringBuffer,"mean=","Gbps");
		historyRecord.sigma          = (double)extractFloatFromStringBuffer(detailsStringBuffer,"stddev=","Gbps");

		history.add(historyRecord);

		count=count+1;
	    }
	    numberOfHistoryRecords=count;

	}catch (Exception e){
	    System.out.println(moduleName+" failed to execute history query "+getHistorySql);
	    System.out.println(moduleName+" "+e);
	    System.out.flush();
	}
	
    }


    public String makeHistoryPlot(String plotDirectory){
	getHistory();

	String plotFileName="temp_picture.jpg";

	String result="";

	// make history plot
	//DefaultTableXYDataset dataset = new DefaultTableXYDataset(); 
	XYSeriesCollection dataset = new XYSeriesCollection();

	ValueAxis timeAxis = new DateAxis("Date and Time"); 
	NumberAxis valueAxis = new NumberAxis("Throughput [Gb/s]"); 
	valueAxis.setAutoRangeIncludesZero(false); 
	StandardXYItemRenderer renderer = new StandardXYItemRenderer( StandardXYItemRenderer.LINES); 
	
	XYSeries throughput_max_series=new XYSeries("throughput max",false);
	XYSeries throughput_avg_series=new XYSeries("throughput avg",false);
	XYSeries throughput_min_series=new XYSeries("throughput min",false);

	Iterator iter = history.iterator();
	while (iter.hasNext()){
	    ThroughputNodeRecord historyRecord = (ThroughputNodeRecord)iter.next();
	    long xTime=historyRecord.timestamp.getTime();
	    double yAvg=historyRecord.throughput_avg;
	    double yMax=historyRecord.throughput_max;
	    double yMin=historyRecord.throughput_min;
	    
	    throughput_max_series.add(xTime,yMax);
	    throughput_avg_series.add(xTime,yAvg);
	    throughput_min_series.add(xTime,yMin);
	}
	dataset.addSeries(throughput_max_series); 
	dataset.addSeries(throughput_avg_series); 
	dataset.addSeries(throughput_min_series); 
	
	//renderer.setSeriesPaint(0,new Color(255, 255, 180)); 
	//renderer.setSeriesPaint(1,new Color(206, 230, 255)); 
	//renderer.setSeriesPaint(2,new Color(255, 230, 230)); 

	renderer.setSeriesPaint(0,Color.BLUE); 
	renderer.setSeriesPaint(1,Color.RED); 
	renderer.setSeriesPaint(2,Color.BLACK); 	
	
	XYPlot plot = new XYPlot(dataset, timeAxis, valueAxis, renderer); 

	JFreeChart chart = new JFreeChart("Throughput: src="+source+"; dst="+destination+"; mon="+monitor,plot);

	try{
	    imageFile = new File (plotDirectory+plotFileName);
	    ChartUtilities.saveChartAsJPEG(imageFile,chart,imageXsize,imageYsize);
	}catch(Exception e){
	    System.out.println(moduleName+" failed to write output file to "+plotFileName);
	    System.out.println(e);
	}
	

	IntervalSelector iS=new IntervalSelector(parameterBag);

	result=result+iS.toHtml()+"<br>";

	result=result+"<img style=\"width: XSIZEpx; height: YSIZEpx;\" alt=\"alternate text\" src=\""+ plotFileName +"\">";
	result=result.replace("XSIZE",Integer.toString(imageXsize));
	result=result.replace("YSIZE",Integer.toString(imageYsize));
	return result;	
    }
   

    public String getHistoryTablePage(){
	String result="";

	IntervalSelector iS=new IntervalSelector(parameterBag);

	result=result+iS.toHtml()+"<br>";

	HtmlTable historyTable=getHistoryTable();
	result=result+historyTable.toHtml();
	return result;
    }
    

    public HtmlTable getHistoryTable(){
	
	getHistory();
	
	HtmlTable ht=new HtmlTable(3);
	ht.setBorder(0);
	ht.setPadding(0);

	Iterator iter = history.iterator();
	while (iter.hasNext()){
	    ThroughputNodeRecord currentRecord = (ThroughputNodeRecord)iter.next();
	    ht.addCell(new HtmlTableCell(currentRecord.timestamp.toString()));
	    ht.addCell(new HtmlTableCell(currentRecord.metricStatus.statusWord(),currentRecord.metricStatus.color()));
	    HtmlTableCell detailsCell=new HtmlTableCell(currentRecord.detailsData);
	    detailsCell.alignLeft();
	    ht.addCell(detailsCell);
	}

	return ht;
    }

    /*
    public HtmlTable shortHtmlTable(){
	String result="";
	result="<strong>Source: </strong>"+source +"<br>";
	result=result+"<strong>Destination: </strong>"+destination +"<br>";
	result=result+"<strong>Monitor: </strong>"+monitor+"<br>";
	result=result+"<strong>state_time: </strong>"+state_time+"<br>";
	result=result+"<strong>Throughput Min=</strong>"+throughput_min+"<br>";
	result=result+"<strong>Throughput Max=</strong>"+throughput_max+"<br>";
	result=result+"<strong>Throughput Avg=</strong>"+throughput_avg+"<br>";
	result=result+"<strong>Sigma=</strong>"+sigma+"<br>";
	result=result+"<strong>Nagios message: </strong>"+nagios_message+"<br>";
	result=result+"<strong>Nagios command: </strong>"+nagios_command+"<br>";
	result=result+new HtmlLink(nagios_link, "Nagios page of this node").toHtml()+"<br>";
	
	// build the address to plot page
	ParameterBag temporaryParameterBag = (ParameterBag)parameterBag.clone();
	temporaryParameterBag.page=ParameterBag.pageAddress("Throughput Node History Plot");
	String urlOfPlotPage=temporaryParameterBag.makeLink();
	HtmlLink linkToPlotPage=new HtmlLink(urlOfPlotPage,"Link to history plot");
	result=result+linkToPlotPage.toHtml()+"<br>";

	// build the address to history table page
	ParameterBag temporaryParameterBag2 = (ParameterBag)parameterBag.clone();
	temporaryParameterBag2.page=ParameterBag.pageAddress("Throughput Node History Table");
	String urlOfHistoryTablePage=temporaryParameterBag2.makeLink();
	HtmlLink linkToHistoryTablePage=new HtmlLink(urlOfHistoryTablePage,"Link to history table");
	result=result+linkToHistoryTablePage.toHtml()+"<br>";

	result=result+"query: "+initialisationSqlQuery;
	
	System.out.println(moduleName+" result="+result);
	System.out.println(moduleName+" status="+status.toString());	

	HtmlTableCell hc =new HtmlTableCell(result,status.color());
	hc.alignLeft();
	HtmlTable ht=new HtmlTable(1);
	ht.addCell(hc);

	return ht;	    	    		
    }
    */
}
