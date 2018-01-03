<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
		pageEncoding="ISO-8859-1"
	import="java.util.Calendar"
	import="java.text.SimpleDateFormat"
	import="java.sql.*"
	import="java.io.*"
	import="java.util.Date"
        import="gov.bnl.racf.dashboard.*"


%>

<head>
<style type="text/css">
<%@include file="style.css" %>
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
  <li><a href="https://nagios.racf.bnl.gov/nagios/cgi-bin/prod/dashboard.php">Old RACF dashboard</a></li>
  <li><a href="https://nagios.racf.bnl.gov/nagios/cgi-bin/prod/perfSonar.php">Old perfSONAR dashboard</a></li>

  <li><a href="https://nagios.racf.bnl.gov/nagios/cgi-bin/test/dashboard.php">Old RACF dashboard (test)</a></li>
  <li><a href="https://nagios.racf.bnl.gov/nagios/cgi-bin/test/perfSonar.php">Old perfSONAR dashboard (test)</a></li>

  <li><a href="http://google.com">Google</a></li>
  <li><a href="http://yahoo.com">Yahoo</a></li>
  
</div>

<div id="body">

<h2>Hello World with List2</h2>
<% out.println("Hello from java "); %>
<%

Connection conn = null;

try{
 	String userName = "root";
       	String password = "toor";
        String url = "jdbc:mysql://localhost:3306/dashboard";
        Class.forName ("com.mysql.jdbc.Driver").newInstance ();
	out.println ("Driver loaded");
	conn = DriverManager.getConnection (url,userName,password);
	out.println ("Database connection established");


        String sql="select * from perfSONAR_sites";

	out.println("<br>");
	out.println(sql);
	out.println("<br>");

	Statement s = conn.createStatement ();
 	s.executeQuery (sql);
  	ResultSet rs = s.getResultSet ();

	out.println("query executed<br>");

	int count = 0;
	while (rs.next ())
	{
	
	//int idVal = rs.getInt ("prob");
       	//String nameVal = rs.getString ("probename");
	String siteName= rs.getString("siteName");
       	out.println ("name = " + siteName + "<br>");
       ++count;
        }
        rs.close ();
       s.close ();
       out.println (count + " rows were retrieved");       
}
catch (Exception e)
{
	out.println ("Cannot connect to database server<br>");
	out.println (e.toString());
}
finally
           {
               if (conn != null)
               {
                   try
                   {
                       conn.close ();
                       out.println ("Database connection terminated");
                   }
                   catch (Exception e) { /* ignore close errors */ }
               }
           }






 java.sql.Timestamp dbSqlTimestamp = new Timestamp(1234567890);

   String curDir= SystemSpy.getCwd();
   out.println("<br>current directory is "+curDir+"<br>");
   SystemSpy.listCurrentDir();

 out.println(dbSqlTimestamp);
 HelloWorld hw=new HelloWorld();
 out.println(hw.hw());
   hw.printHello();


   long maxInactiveInterval=session.getMaxInactiveInterval();
   out.println("<br>max inactive="+maxInactiveInterval+"<br>");
   if (session.isNew()){
      out.println("<br>session is new");
   }else{
       out.println("<br>session  is old<br>");
       java.util.Date d=new Date(session.getLastAccessedTime());
       out.println("last accessed: "+d );
       java.util.Date currentTime=new Date();
       out.println("<br>current time: "+currentTime );
       long dT=currentTime.getTime()-d.getTime();
       out.println("seconds ago: "+dT);
       out.println("<br>");
       session.setMaxInactiveInterval(60); 
   }

 HtmlLink hl=new HtmlLink("http://www.google.com/","google");
 out.println(hl.toHtml()); 
 out.println("<br>DRRRRRRR<br>"); 
   
out.println(HtmlColor.htmlColor("red"));

 HtmlLink hl2=new HtmlLink("http://www.yahoo.com/","yahoo","link title");
 out.println(hl2.toHtml()); 

   HtmlTable tb=new HtmlTable(3);
   tb.addCell((new HtmlTableCell(hl2,new HtmlColor("green"))));
   tb.addCell((new HtmlTableCell(hl2,new HtmlColor("red"))));
   tb.addCell((new HtmlTableCell(hl2,new HtmlColor("yellow"))));
   tb.addCell((new HtmlTableCell(hl2,new HtmlColor("brown"))));

   tb.addCell((new HtmlTableCell(hl,new HtmlColor("white"))));
   tb.addCell((new HtmlTableCell(hl,new HtmlColor("red"))));
   tb.addCell((new HtmlTableCell(hl,new HtmlColor("yellow"))));
   tb.addCell(new HtmlTableCell(hl));

   out.println(tb.toHtml());

   MakePlot mp=new MakePlot();
   out.println(mp. getCurrentDir());
   out.println(mp.linkToPlot(request.getRealPath("/")));



%>

The Path of the current jsp page is: <%out.println(request.getRealPath("/"));%>
</div>


<div id="tail">
<p><b>(c) 2010 Brookhaven National Laboratory </b>- send suggestions
and comments to <a href="mailto:tomw@bnl.gov">tomw@bnl.gov</a><br>
</p>
</div>

</body>
</html>
