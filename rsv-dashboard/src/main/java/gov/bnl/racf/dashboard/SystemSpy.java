package gov.bnl.racf.dashboard;

import java.io.*;

public class SystemSpy
{
    public static String getCwd(){
	String curDir = System.getProperty("user.dir");
	return curDir;
    }
    public static void listCurrentDir(){
	File dir = new File(getCwd());
	String[] children = dir.list();
	if (children == null) {
	    System.out.println("Directory "+getCwd()+"is empty");
	} else {
	    for (int i=0; i<children.length; i++) {
		// Get filename of file or directory
		System.out.println("<br>");
		System.out.println(children[i]);		
	    }
	}


    }
}