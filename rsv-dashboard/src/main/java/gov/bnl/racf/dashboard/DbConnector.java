package gov.bnl.racf.dashboard;

import java.sql.*;
import java.util.Properties;
import java.io.FileOutputStream;
import java.io.FileInputStream;
import java.io.IOException;
//import java.io.*;

public class DbConnector
{  
    private String moduleName="DbConnector";
    

    private String userName1 = "";
    private String userPwd1="";
    private String url1="";

    private String userName2 = "";
    private String userPwd2="";
    private String url2="";

    private String userName3 = "";
    private String userPwd3="";
    private String url3="";
    
    private String userName = "";
    private String userPwd="";
    private String url="";
    /*
    private String userName1 = "nagios";
    private String userPwd1="nagi0s";
    private String url1="jdbc:mysql://rnagios01.usatlas.bnl.gov:3306/perfSONAR";

    private String userName2 = "nagios";
    private String userPwd2="nagi0s";
    private String url2="jdbc:mysql://localhost:3306/perfSONAR";

    private String userName3 = "gratia-reader";
    private String userPwd3="reader";
    private String url3="jdbc:mysql://griddev03.usatlas.bnl.gov:49152/gratia";
    */

    private Connection conn = null;

    private ResultSet rs=null;
    private Statement s=null;

    private String configFileName="";
    //private String configFileName="src/main/resources/config.properties";
    //private String configFileName="/WEB-INF/config.properties";


    public DbConnector()
	{	    
	    loadConfiguration();
	    openConnection(1);	
	}

    public DbConnector(int dbNumber,String inputConfigFileName  )
	{
	    configFileName=inputConfigFileName;
	    loadConfiguration();
	    openConnection(dbNumber);	
	}

    private void loadConfiguration(){
      
	
	Properties prop = new Properties();
	try{
	    prop.load(new FileInputStream( configFileName ));

	    userName1=prop.getProperty("userName1");
	    userPwd1 =prop.getProperty("userPwd1");
	    url1     =prop.getProperty("url1");
	    
	    userName2=prop.getProperty("userName2");
	    userPwd2 =prop.getProperty("userPwd2");
	    url2     =prop.getProperty("url2");
	    
	    userName3 =prop.getProperty("userName3");
	    userPwd3 =prop.getProperty("userPwd3");
	    url3     =prop.getProperty("url3");

	} catch (IOException ex) {
	    System.out.println(moduleName+" Error: unable to open configuration file "+configFileName);
	    ex.printStackTrace();
        }
	
    }

    private void openConnection (int dbNumber){

	url=url1;
	userName=userName1;
	userPwd=userPwd1;

	if (dbNumber==1){
	    url=url1;
	    userName=userName1;
	    userPwd=userPwd1;
	}
	if (dbNumber==2){
	    url=url2;
	    userName=userName2;
	    userPwd=userPwd2;
	}
	if (dbNumber==3){
	    url=url3;
	    userName=userName3;
	    userPwd=userPwd3;
	}


	try{
	    Class.forName ("com.mysql.jdbc.Driver").newInstance ();
	}catch (Exception e){
	    System.out.println(moduleName+": failed to load database driver");
	}
	try{
	    conn = DriverManager.getConnection (url,userName,userPwd);
	}catch (Exception e){
	    System.out.println(moduleName+": failed to establish database connection");
	    System.out.println(e);
	}	


    }

    public Connection getConn(){
	return conn;
    }
    public ResultSet  query(String sql){
	
	try{
	    s = conn.createStatement ();
	    s.executeQuery (sql);
	}catch (Exception e){
	    System.out.println(moduleName+": failed to execute query "+sql);
	    System.out.println(e);
	}
	try{
	    rs = s.getResultSet ();
	    //s.close();
	}catch(Exception e){
	    System.out.println(moduleName+": failed to obtain result set for query query "+sql);
	    System.out.println(e);
	}
	return rs;
    }
    public void close(){
	try{
	    s.close();
	    conn.close();
	}catch (Exception e){
	    System.out.println(moduleName+": failed to close dB connection");
	}
    }
    public Connection getConnection(){
	return conn;
    }
    public boolean isClosed(){
	boolean result=true;
	try{
	    result=conn.isClosed();
	}catch (Exception e){
	    System.out.println(moduleName+": failed to check if dB is closed");
	    System.out.println(e);
	}
	return result;
    }

}
