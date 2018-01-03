<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
		pageEncoding="ISO-8859-1"
	import="java.util.Calendar"
	import="java.text.SimpleDateFormat"
	import="java.sql.*"
	import="java.io.*"
	import="java.util.Date"
        import="gov.bnl.racf.dashboard.*"

	import="java.io.FileOutputStream"
	import="java.io.IOException"
	import="java.util.Properties"
	import="java.util.Iterator"
	import="java.util.List"
	import="java.util.ArrayList"


%>

<head>
<style type="text/css">
<%@include file="Navy.css" %>
</style>
</head>

<html>
<body>



<div id="title">
<h1><span>RACF</span></h1>
<h3><span>Grid Group</h3>
<h2><span>The Experimental Gratia/RSV Dashboard</span></h2>
</div>



<div id="sideNav">
<ul>
  <li><a href="http://localhost:8080/dashboard/">Gratia dashboard main page</a></li>
  <li><a href="https://nagios.racf.bnl.gov/nagios/cgi-bin/prod/dashboard.php">RACF dashboard</a></li>
  <li><a href="https://nagios.racf.bnl.gov/nagios/cgi-bin/prod/perfSonar.php">perfSONAR dashboard</a></li>

  <li><a href="https://nagios.racf.bnl.gov/nagios/cgi-bin/test/dashboard.php">RACF dashboard (test)</a></li>
  <li><a href="https://nagios.racf.bnl.gov/nagios/cgi-bin/test/perfSonar.php">perfSONAR dashboard (test)</a></li>

</div>

<div id="body">

<%

ArrayList<String> listOfHostNames = new ArrayList<String>();
listOfHostNames.add("psmsu01.aglt2.org");
listOfHostNames.add("psmsu02.aglt2.org");
listOfHostNames.add("lhcmon.bnl.gov");
listOfHostNames.add("lhcperfmon.bnl.gov");
listOfHostNames.add("psum01.aglt2.org");
listOfHostNames.add("psum02.aglt2.org");
listOfHostNames.add("iut2-net1.iu.edu");
listOfHostNames.add("iut2-net2.iu.edu");
listOfHostNames.add("uct2-net1.uchicago.edu");
listOfHostNames.add("uct2-net2.uchicago.edu");
listOfHostNames.add("atlas-npt1.bu.edu");
listOfHostNames.add("atlas-npt2.bu.edu");
listOfHostNames.add("ps1.ochep.ou.edu");
listOfHostNames.add("ps2.ochep.ou.edu");
listOfHostNames.add("netmon1.atlas-swt2.org");
listOfHostNames.add("netmon2.atlas-swt2.org");


out.flush();


RequestDispatcher rd
            = getServletContext().getRequestDispatcher("/DriverServlet");
            rd.include(request, response);



%>


</div>


<div id="tail">
<p><b>(c) 2010 Brookhaven National Laboratory </b>- send suggestions
and comments to <a href="mailto:tomw@bnl.gov">tomw@bnl.gov</a><br>
</p>
</div>

</body>
</html>
