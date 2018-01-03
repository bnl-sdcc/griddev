package gov.bnl.racf.gridinfo;

import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import gov.bnl.racf.gridinfo.SSLCertFilter;

/**
 * Hello world!
 */
public class ServletApp extends HttpServlet 
{
	static private Logger log = LoggerFactory.getLogger(ServletApp.class);
	
	public void doGet(HttpServletRequest request, HttpServletResponse response)
    throws IOException, ServletException
    {
		log.debug("Peforming doGet() for ServletApp...");
        response.setContentType("text/html");
        PrintWriter out = response.getWriter();          
        helloWorld(out);
    }
	
	
	public void helloWorld(PrintWriter out) {
		log.debug("Peforming helloWorld() for ServletApp...");
		out.println("<html>");
        out.println("<head>");
        out.println("<title>Hello World!</title>");
        out.println("</head>");
        out.println("<body>");
        out.println("<h1>Hello World!</h1>");
        out.println(otherStuff());
        out.println("</body>");
        out.println("</html>");
	}
	
	public String otherStuff() {
		return "Client DN is " + SSLCertFilter.getClientSubject();
		//return "Other Stuff!";
	}
	
	
    public static void main( String[] args )
    {
        System.out.println( "Hello World from Java!" );
    }
}
