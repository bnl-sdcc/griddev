<%@ page contentType="text/html" %>
<%@ page pageEncoding="UTF-8" %>
<%@ page import="gov.bnl.racf.gridinfo.*" %>

<jsp:useBean id="gridinfo" scope="application" class="gov.bnl.racf.gridinfo.GridInfo" />

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
  <%@include file="title.jsp"%>
  <body>

    <%@include file="topnav.jsp"%>
    <%@include file="sidenav.jsp"%>

    <div id="body">
       <p>The GridInfo system serves as a general template for Grid-enabled apps. </p>
       
 
     </div>

    <%@include file="bottomnav.jsp"%>

  </body>
</html>
