package gov.bnl.racf.dashboard;

import javax.servlet.*;
import org.jfree.*;

public class HelloWorld
{  
    public HelloWorld( )
	{
	}
    public static String hw(){
	return "Hello world from a class";
    }
    public static void printHello(){
	System.out.println("Hello from print hello");
    }
    public static void main(String args[])
    {
           System.out.println("Hello World!");
    }
}
