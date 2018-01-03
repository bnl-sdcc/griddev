package gov.bnl.racf.dashboard;

import java.sql.*;
import java.util.Calendar;
import java.io.*;

import java.awt.Color;

import java.util.Iterator;
import java.util.List;
import java.util.ArrayList;

//import org.jfree.*;
//import org.jfree.chart.*;
//import org.jfree.chart.ChartFactory;
//import org.jfree.chart.JFreeChart;
//import org.jfree.data.xy.XYSeries;
//import org.jfree.data.xy.XYDataset; 
//import org.jfree.data.xy.XYSeriesCollection;
//import org.jfree.chart.plot.PlotOrientation;
//import org.jfree.chart.axis.ValueAxis;
//import org.jfree.chart.axis.NumberAxis;
//import org.jfree.chart.axis.DateAxis;
//import org.jfree.chart.plot.XYPlot;
//import org.jfree.chart.renderer.xy.StandardXYItemRenderer;
//import org.jfree.data.xy.DefaultTableXYDataset;


public class PerfSonarPrimitiveService
{  

    private String moduleName="PerfSonarPrimitiveService";

    private String serviceName="";
    private String serviceType="";
    private String serviceUri="";
    private String metricType="";
    public ProbeStatus status =null;
    
    private Timestamp state_time = null;

    private String summaryData="";
    private String detailsData="";
    private String hostName="";

    // the host name parameter in the database
    private String hostNameInDatabase = "";


    private ParameterBag parameterBag = null;
    private DbConnector db=null;

    ResultSet rs=null;
    private String initialisationSqlQuery="";
    private PreparedStatement initialisationSql=null;

    // lists which keep history information
    private Timestamp[] state_time_list=new Timestamp[1000];
    private String[] summaryData_list=new String[1000];
    private String[] detailsData_list=new String[1000];
		
    private ProbeStatus[] status_list = new ProbeStatus[1000];
    private int numberOfHistoryRecords=0;

    private String linkToDetailPage = "";

    //List<String> ls=new ArrayList<String>();


    public PerfSonarPrimitiveService(ParameterBag paramBag,  DbConnector inputDb,String inputServiceName, String inputHostName)
	{
	    parameterBag=(ParameterBag)paramBag.clone();
	    
	    db=inputDb;

	    hostName=inputHostName;
	    parameterBag.addParam("hostName",hostName);

	    System.out.println(moduleName+" hostName="+hostName);

	    serviceName=inputServiceName;
	    parameterBag.addParam("serviceName",serviceName);

	    /// create link to node detail page
	    ParameterBag paramBagLocal=(ParameterBag)paramBag.clone();
	    paramBagLocal.addParam("page",ParameterBag.pageAddress("perfSonar Primitive")  );
	    paramBagLocal.addParam("serviceName",serviceName);
	    paramBagLocal.addParam("hostName",hostName);
	    
	    linkToDetailPage=paramBagLocal.makeLink();
	   
	    //=========== get information =======

	    initialisationSqlQuery="select * from MetricRecord where MetricName=?  and ServiceUri like ? order by Timestamp desc limit 1";
	    try{
		initialisationSql= db.getConn().prepareStatement(initialisationSqlQuery);
		initialisationSql.setString(1,serviceName);
		initialisationSql.setString(2,"%"+hostName+"%");

		rs=initialisationSql.executeQuery();
	    	   
		int count = 0;
		while (rs.next ())
		    {
			state_time=rs.getTimestamp("Timestamp");
			String status_str=rs.getString("MetricStatus");			
			status=new ProbeStatus(status_str);

			serviceType=rs.getString("ServiceType");
			serviceUri=rs.getString("ServiceUri");
			summaryData=rs.getString("SummaryData");
			detailsData=rs.getString("DetailsData");
			hostNameInDatabase=rs.getString("HostName");
		       			
			count=count+1;
		    }
	    }catch (Exception e){
		System.out.println(moduleName+" error occured when reading database");
		System.out.println(e);
	    }


	}



    public PerfSonarPrimitiveService(ParameterBag paramBag,  DbConnector inputDb,String inputServiceName)
	{
	    parameterBag=(ParameterBag)paramBag.clone();
	    
	    db=inputDb;

	    serviceName=inputServiceName;
	    parameterBag.addParam("serviceName",serviceName);

	    /// create link to node detail page
	    ParameterBag paramBagLocal=(ParameterBag)paramBag.clone();
	    paramBagLocal.addParam("page",ParameterBag.pageAddress("perfSonar Primitive")  );
	    paramBagLocal.addParam("serviceName",serviceName);
	    
	    linkToDetailPage=paramBagLocal.makeLink();
	    

	   
	    //=========== get information =======

	    initialisationSqlQuery="select * from MetricRecord where MetricName=? order by Timestamp desc limit 1";
	    try{
		initialisationSql= db.getConn().prepareStatement(initialisationSqlQuery);
		initialisationSql.setString(1,serviceName);

		rs=initialisationSql.executeQuery();
	    	   
		int count = 0;
		while (rs.next ())
		    {
			state_time=rs.getTimestamp("Timestamp");
			String status_str=rs.getString("MetricStatus");			
			status=new ProbeStatus(status_str);

			serviceType=rs.getString("ServiceType");
			serviceUri=rs.getString("ServiceUri");
			summaryData=rs.getString("SummaryData");
			detailsData=rs.getString("DetailsData");
			hostNameInDatabase=rs.getString("HostName");
		       			
			count=count+1;
		    }
	    }catch (Exception e){
		System.out.println(moduleName+" error occured when reading database");
		System.out.println(e);
	    }


	}

    public void getHistory(){
	String getHistorySql="select * from MetricRecord where MetricName=? and ServiceUri like ? ";
	IntervalSelector iS=new IntervalSelector(parameterBag,"Timestamp",-4);
	getHistorySql=getHistorySql+" "+iS.buildQuery(parameterBag.interval);
	
	System.out.println(moduleName+" getHistorySql="+getHistorySql);

	try{
	    PreparedStatement getHistoryStatement= db.getConn().prepareStatement(getHistorySql);
	    getHistoryStatement.setString(1,serviceName);
	    getHistoryStatement.setString(2,"%"+hostName+"%");
	    rs=getHistoryStatement.executeQuery();

	    int count = 0;
	    while (rs.next ()){
		state_time_list[count]=rs.getTimestamp("Timestamp");
		summaryData_list[count]=rs.getString("SummaryData");
		detailsData_list[count]=rs.getString("DetailsData");
		
		status_list[count]= new ProbeStatus(rs.getString("MetricStatus"));
		count=count+1;
		numberOfHistoryRecords=count;
		}
	}catch (Exception e){
	    System.out.println(moduleName+" failed to execute history query "+getHistorySql);
	    System.out.println(moduleName+" "+e);
	}
	
    }



    public String getHistoryTablePage(){
	String result="";

	IntervalSelector iS=new IntervalSelector(parameterBag);

	result=result+iS.toHtml()+"<br>";
	result=result.replace("state_time","Timestamp");

	HtmlTable historyTable=getHistoryTable();
	result=result+historyTable.toHtml();
	return result;
    }

    public HtmlTable getHistoryTable(){
	getHistory();

	System.out.println(moduleName+" loaded history table");
	System.out.println(moduleName+" numberOfHistoryRecords="+numberOfHistoryRecords);

	HtmlTable ht=new HtmlTable(4);
	ht.setBorder(0);
	ht.setPadding(0);
	for (int i=0;i<numberOfHistoryRecords;i=i+1){
	    ht.addCell(new HtmlTableCell(state_time_list[i].toString()));
	    ht.addCell(new HtmlTableCell(status_list[i].statusWord(),status_list[i].color()));

	    HtmlTableCell summaryDataCell=new HtmlTableCell(summaryData_list[i]);
	    summaryDataCell.alignLeft();
	    ht.addCell(summaryDataCell);

	    HtmlTableCell detailsDataCell=new HtmlTableCell(detailsData_list[i]);
	    detailsDataCell.alignLeft();
	    ht.addCell(detailsDataCell);

	}
	return ht;
    }


    public HtmlTableCell veryShortStatusCell(){
	// return very short status table containing only status word and color
	// to be used in throughput matrix	
	//HtmlLink link=new HtmlLink(linkToDetailPage,status.statusWordShort());
	HtmlLink link=new HtmlLink(linkToDetailPage,serviceName+"<br>"+hostName);
	HtmlTableCell cell=new HtmlTableCell(link,status.color());
	return cell;
	
    }

    public HtmlTable shortHtmlTable(){

	String result="";
	result="<strong>ServiceName: </strong>"+serviceName +"<br>";
	result=result+"<strong>ServiceType: </strong>"+serviceType +"<br>";
	result=result+"<strong>ServiceUri: </strong>"+serviceUri+"<br>";
	result=result+"<strong>Timestamp: </strong>"+state_time+"<br>";
	result=result+"<strong>SummaryData=</strong>"+summaryData+"<br>";
	result=result+"<strong>DetailsData=</strong>"+detailsData+"<br>";
	result=result+"<strong>HostName=</strong>"+hostNameInDatabase+"<br>";
	result=result+"<strong>HostName=</strong>"+hostName+"<br>";

	// build the address to history table page
	ParameterBag temporaryParameterBag2 = (ParameterBag)parameterBag.clone();
	temporaryParameterBag2.page=ParameterBag.pageAddress("Link to history table");
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
}
