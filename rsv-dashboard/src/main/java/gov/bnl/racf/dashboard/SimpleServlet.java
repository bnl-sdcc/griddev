

package gov.bnl.racf.dashboard;


import java.io.*;
import java.text.*;
import java.util.*;
import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.ServletContext;

public class SimpleServlet extends HttpServlet {

    public void doGet(HttpServletRequest request,
                      HttpServletResponse response)
        throws IOException, ServletException
    {

        response.setContentType("text/html");
        PrintWriter out = response.getWriter();

        //out.println("<html>");
        //out.println("<head>");

	//String title = rb.getString("helloworld.title");
	//String title="hello World from hw";

	//    out.println("<title>" + title + "</title>");
	// out.println("</head>");
        //out.println("<body bgcolor=\"white\">");

	out.println("AAAAAAA --- SimpleServlet --- BBBBBBBB");
	out.println(request.getRealPath(request.getServletPath()));

	out.println("<br>");
	//out.println(request.getSession().getServletContext().getRealPath("/"));

        //out.println("</body>");
        //out.println("</html>");
    }
}



