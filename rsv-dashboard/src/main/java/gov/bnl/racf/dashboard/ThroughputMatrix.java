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


public class ThroughputMatrix
{  

    private String moduleName="ThroughputMatrix";



    private ParameterBag parameterBag = null;

    private DbConnector db=null;

    private ResultSet rs=null;
    private String initialisationSql="";

    private List<String> listOfSourceHosts=new ArrayList<String>();
    private List<String> listOfDestinationHosts=new ArrayList<String>();
    private int numberOfHostNames=0;

    public ThroughputMatrix(ParameterBag paramBag,   DbConnector inputDb)
	{
	    parameterBag=paramBag;
	    db=inputDb;

	    //=========== get matrix nodes =======
	    initialisationSql="select DISTINCT src from perfSONAR_throughput";	    
		
	    try{
		rs=db.query(initialisationSql);
	    	   
		int count = 0;
		while (rs.next ())
		    {
			String src=rs.getString("src");
			listOfSourceHosts.add(src);
			listOfDestinationHosts.add(src);					
			count=count+1;
		    }
		numberOfHostNames=count;
	    }catch (Exception e){
		System.out.println(moduleName+" error occured when reading database");
		System.out.println(e);
	    }


	}

    public String toString(){
	String result="Hello world from throughput matrix";
	return result;
    }

    public HtmlTable htmlTable(){

	HtmlTable ht=new HtmlTable(numberOfHostNames+1);
	
	HtmlTableCell firstCell=new HtmlTableCell("---");
	ht.addCell(firstCell);

	for (int i=0;i<numberOfHostNames;i=i+1){
	    ht.addCell(new HtmlTableCell(Integer.toString(i)));
	}

	for (int iSrc=0;iSrc<listOfSourceHosts.size();iSrc=iSrc+1){
	    String src=listOfSourceHosts.get(iSrc);

	    HtmlTableCell firstColumnCell = new HtmlTableCell(Integer.toString(iSrc)+":"+src);
	    firstColumnCell.alignLeft();
	    ht.addCell(firstColumnCell);
	    
	    for (int iDst=0;iDst<listOfDestinationHosts.size();iDst=iDst+1){		
		String dst=listOfDestinationHosts.get(iDst);
		if (src.equals(dst)){
		    ht.addCell(new HtmlTableCell("---"));
		}else{
		    ThroughputNode upperNode=new ThroughputNode(parameterBag,db,src,dst,src);
		    ThroughputNode lowerNode=new ThroughputNode(parameterBag,db,src,dst,dst);
		    HtmlTable nodeTable=new HtmlTable(1);
		    nodeTable.addCell(upperNode.veryShortStatusCell());
		    nodeTable.addCell(lowerNode.veryShortStatusCell());
		    nodeTable.setBorder(0);
		    nodeTable.setPadding(0);
		    ht.addCell(new HtmlTableCell(nodeTable.toHtml()));
		    
		    //ht.addCell(new HtmlTableCell(src+"<br>"+dst));
		}
	    }
	}


	return ht;
    }

    public HtmlTable shortHtmlTable(){

	HtmlTable ht=new HtmlTable(1);

	return ht;	    	    		
    }
}
