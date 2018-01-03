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
       <p><h2>Client Information</h2></p>
      <p>Current User: <%=gridinfo.getClientSubject()%><br/>
      Current User CA: <%=gridinfo.getClientIssuer()%><br/>
      Current User Serial: <%=gridinfo.getClientSerial()%><br/>
      Current User NotBefore: <%=gridinfo.getClientNotBefore()%><br/>
      Current User NotAfter: <%=gridinfo.getClientNotAfter()%></p>
      <jsp:include page="fingerprint.jsp" />
    </div>

    <%@include file="bottomnav.jsp"%>

  </body>
</html>