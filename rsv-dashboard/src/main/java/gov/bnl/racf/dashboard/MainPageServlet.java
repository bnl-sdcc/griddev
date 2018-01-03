

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

public class MainPageServlet extends HttpServlet {

    private String moduleName="MainPageServlet";

    private Properties dbParameters = null;
    private DbConnector dB=null;
 


    public void doGet(HttpServletRequest request,
                      HttpServletResponse response)
        throws IOException, ServletException
    {
        response.setContentType("text/html");
        PrintWriter out = response.getWriter();

	out.println("we are in MinPageServlet");
	out.println("<br>");
    }
}



