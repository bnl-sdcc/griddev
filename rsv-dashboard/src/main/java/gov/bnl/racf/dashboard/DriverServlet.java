

package gov.bnl.racf.dashboard;


import java.io.*;
import java.text.*;
import java.util.*;
import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.ServletContext;

import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Properties;

public class DriverServlet extends HttpServlet {

    private String moduleName="DriverServlet";

    private Properties dbParameters = null;
    private DbConnector dB=null;
    
    //private String pictureFileName="WEB-INF/classes/temp_picture.jpg"; 
    private String pictureDirectory=null; 
    private String dbConfigFileName="WEB-INF/classes/config.properties"; 
    private String listOfHostsFileName="WEB-INF/classes/hosts.config";
    ArrayList<String> listOfHostNames=new ArrayList<String>();

    private void openConnection(){
	// create database connector
	    try{
		dbParameters=new Properties();
		dbParameters.load(new FileInputStream( dbConfigFileName ));
	    }catch (IOException ex) {
		System.out.println(moduleName+" Error: unable to open configuration file "+dbConfigFileName);
		ex.printStackTrace();
	    }
	    dB=new DbConnector(3, dbConfigFileName );
    }

    public void init(ServletConfig config) throws ServletException {
            // Store the ServletConfig object and log the initialization
            super.init(config);

	    //pictureFileName=getServletContext().getRealPath("/")+pictureFileName;
	    pictureDirectory = getServletContext().getRealPath("/");
	    dbConfigFileName=getServletContext().getRealPath("/")+dbConfigFileName;
	    listOfHostsFileName=getServletContext().getRealPath("/")+listOfHostsFileName;
	   	  
	    openConnection();

	    // read list of hosts
	    File file = new File(listOfHostsFileName);
	    BufferedReader reader = null;
	    try {
		reader = new BufferedReader(new FileReader(file));
		String text = null;
 
		while ((text = reader.readLine()) != null) {
		    listOfHostNames.add(text);
		}
	    } catch (FileNotFoundException e) {
		e.printStackTrace();
	    } catch (IOException e) {
		e.printStackTrace();
	    } finally {
		try {
		    if (reader != null) {
			reader.close();
		    }
		} catch (IOException e) {
		    e.printStackTrace();
		}
	    }
	    
        }


    public void doGet(HttpServletRequest request,
                      HttpServletResponse response)
        throws IOException, ServletException
    {
        response.setContentType("text/html");
        PrintWriter out = response.getWriter();

	if(dB.getConnection()==null){
	    openConnection();
	}else{
	    if(dB.isClosed()){
		dB.close();
		openConnection();
	    }
	}


	ParameterBag pB=new ParameterBag();
	pB.setRequestUri(request.getRequestURI());
	pB.setWorkDirectory(request.getRealPath("/"));

	pB.addParam("serverName",request.getServerName());
	pB.addParam("serverPort",Integer.toString(request.getServerPort()));
	pB.addParam("servletPath",request.getServletPath());
	pB.addParam("page",request.getParameter("page"));

	pB.addParam("interval",request.getParameter("interval"));
	
	//pB.addParam("src",request.getParameter("src"));
	//pB.addParam("dst",request.getParameter("dst"));
	//pB.addParam("mon",request.getParameter("mon"));

	// hardcode source and destination, for the time being
	pB.addParam("src","lhcmon.bnl.gov");
	pB.addParam("dst","psum02.aglt2.org");
	pB.addParam("mon","lhcmon.bnl.gov");

	pB.addParam("host",request.getParameter("host"));
	pB.addParam("service",request.getParameter("service"));
	pB.addParam("site",request.getParameter("site"));

	pB.addParam("hostName"   ,request.getParameter("hostName"));
	pB.addParam("serviceName",request.getParameter("serviceName"));



	String page = request.getParameter("page");

	if (page==null){
	    
	    page=SitePages.pageId("Main");;
	}

	if (SitePages.pageName(page).equals("Main") ){
	    out.println("<h2>Status of perfSONAR Services</h2>");
	    out.flush();
	    
	    out.println("<h3>Service net.perfsonar.service.hls</h3>");
	    out.println("<br>");
	    out.flush();

	    ListOfPerfSonarPrimitiveServices listOfServices = 
				 new ListOfPerfSonarPrimitiveServices(pB,dB,"net.perfsonar.service.hls",listOfHostNames);
	    out.println(listOfServices.shortHtmlTable().toHtml());

	    out.println("<br>");
	    out.println("<h3>Throughput for source="+pB.src+" destination="+pB.dst+" monitor="+pB.mon+"</h3>");
	    out.flush();
	    
	    ThroughputNode tn=new ThroughputNode(pB,dB,pB.src,pB.dst,pB.mon);
	    out.println(tn.shortHtmlTable().toHtml());

	}
	if (SitePages.pageName(page).equals("Throughput Node") ){
	    out.println("<h2>Throughput for source="+pB.src+" destination="+pB.dst+" monitor="+pB.mon+"</h2>");
	    ThroughputNode tn=new ThroughputNode(pB,dB,pB.src,pB.dst,pB.mon);
	    out.println(tn.fullHtmlTable().toHtml());
	}
	if (SitePages.pageName(page).equals("Throughput Node History Table") ){
	    out.println("<h2>Throughput history for source="+pB.src+" destination="+pB.dst+" monitor="+pB.mon+"</h2>");
	    ThroughputNode tn=new ThroughputNode(pB,dB,pB.src,pB.dst,pB.mon);
	    out.println(tn.getHistoryTablePage());
	}
	if (SitePages.pageName(page).equals("Throughput Node History Plot") ){
	    out.println("<h2>Throughput history plot for source="+pB.src+" destination="+pB.dst+" monitor="+pB.mon+"</h2>");
	    ThroughputNode tn=new ThroughputNode(pB,dB,pB.src,pB.dst,pB.mon);
	    out.println(tn.makeHistoryPlot(pictureDirectory));
	}

	if (SitePages.pageName(page).equals("perfSonar Primitive") ){
	    String serviceName=pB.serviceName;
	    String hostName   =pB.hostName;
	    out.println("<h2>Service "+serviceName+" on host "+hostName+"</h2>");

	    PerfSonarPrimitiveService pSP=new PerfSonarPrimitiveService(pB,dB,serviceName,hostName);
   
	    HtmlTable ht=pSP.shortHtmlTable();
	    out.println(ht.toHtml());		
	}
	if (SitePages.pageName(page).equals("Link to history table")){
	       String serviceName=pB.serviceName;
	       String hostName   =pB.hostName;
	       out.println("<h2>Service "+serviceName+" on host "+hostName+"</h2>");
	       PerfSonarPrimitiveService pSP=new PerfSonarPrimitiveService(pB,dB,serviceName,hostName);
	       String htp = pSP.getHistoryTablePage();
	       out.println(htp);		
	}
	if (SitePages.pageName(page).equals("List Of Services Page") ){
	    out.println("<h2>perfSONAR Primitive Services</h2>");
	       ListOfPerfSonarPrimitiveServices listOfServices = 
				 new ListOfPerfSonarPrimitiveServices(pB,dB,"net.perfsonar.service.hls",listOfHostNames);
	       out.println(listOfServices.detailedHtmlTable().toHtml());

	}
	   

	
    }
}



