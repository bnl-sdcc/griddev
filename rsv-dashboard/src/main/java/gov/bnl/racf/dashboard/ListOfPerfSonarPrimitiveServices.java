package gov.bnl.racf.dashboard;

import java.sql.*;
import java.util.Calendar;
import java.io.*;

import java.awt.Color;

import java.util.Iterator;
import java.util.List;
import java.util.ArrayList;


public class ListOfPerfSonarPrimitiveServices
{  

    private String moduleName="ListOfPerfSonarPrimitiveServices";

    private String serviceName="";

    private ParameterBag parameterBag = null;
    private DbConnector db=null;

    private ProbeStatus status =null;

    ArrayList<String> listOfHostNames=new ArrayList<String>();

    ArrayList<PerfSonarPrimitiveService> listOfServices = new ArrayList<PerfSonarPrimitiveService>();


    public ListOfPerfSonarPrimitiveServices(ParameterBag paramBag,  DbConnector inputDb,String inputServiceName,ArrayList<String> inputListOfHostNames )
	{
	    parameterBag=(ParameterBag)paramBag.clone();

	    db=inputDb;

	    serviceName=inputServiceName;
	    parameterBag.addParam("serviceName",serviceName);

	    listOfHostNames=inputListOfHostNames;

	    status = new ProbeStatus("OK");

	    Iterator itr = listOfHostNames.iterator();
	    while(itr.hasNext()){
		String hostName=(String)itr.next();
		PerfSonarPrimitiveService pPS=new PerfSonarPrimitiveService(parameterBag,db,serviceName,hostName);
		if (status.statusLevel()<pPS.status.statusLevel()){
		    status=pPS.status;
		}
			
		listOfServices.add(pPS);
	    }
	   
	}






    public HtmlTableCell veryShortStatusCell(){
	// return very short status table containing only status word and color
	// to be used in throughput matrix	
	//HtmlLink link=new HtmlLink(linkToDetailPage,status.statusWordShort());
	//HtmlTableCell cell=new HtmlTableCell(link,status.color());

	HtmlLink link=new HtmlLink(serviceName,status.statusWordShort());
	HtmlTableCell cell=new HtmlTableCell(link,status.color());
	return cell;
	
    }
    
    public HtmlTable detailedHtmlTable(){

	// build the address to history table page
	ParameterBag temporaryParameterBag2 = (ParameterBag)parameterBag.clone();
	temporaryParameterBag2.page=ParameterBag.pageAddress("Link to history table");
	String urlOfHistoryTablePage=temporaryParameterBag2.makeLink();
	HtmlLink linkToHistoryTablePage=new HtmlLink(urlOfHistoryTablePage,"Link to history table");

	HtmlTable ht=new HtmlTable(4);

	Iterator iter = listOfServices.iterator();
	while (iter.hasNext()){
	    PerfSonarPrimitiveService currentService = (PerfSonarPrimitiveService)iter.next();
	    ht.addCell(currentService.veryShortStatusCell());
	}


	return ht;	    	    		
    }
    

    
    public HtmlTable shortHtmlTable(){

	// build the address to history table page
	ParameterBag temporaryParameterBag2 = (ParameterBag)parameterBag.clone();
	temporaryParameterBag2.page=ParameterBag.pageAddress("List Of Services Page");
	String urlOfHistoryTablePage=temporaryParameterBag2.makeLink();
	HtmlLink linkToServicesPage=new HtmlLink(urlOfHistoryTablePage,serviceName);

	HtmlTableCell hc =new HtmlTableCell(linkToServicesPage,status.color());
	hc.alignLeft();
	HtmlTable ht=new HtmlTable(1);
	ht.addCell(hc);

	return ht;	    	    		
    }
    

    public String toHtml(){
	String result="";
	
	Iterator itr = listOfHostNames.iterator();
	while(itr.hasNext()){
	    result=result+" "+itr.next();
	}

	return result;
    }

}
