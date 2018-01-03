// Java servlet Document

import java.io.*;
import java.sql.*;
import javax.servlet.*;
import javax.servlet.http.*; 

public class first extends HttpServlet
{
    public void doGet(HttpServletRequest req,HttpServletResponse res)
     throws ServletException,IOException
    {
        PrintWriter out = res.getWriter();
        res.setContentType("text/html");
        out.println("this is First servlet Example ");
    }
}
