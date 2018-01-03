package gov.bnl.racf.dashboard;

public class ParameterBag implements Cloneable
{  
    public String interval="4";
    
    public String src=null;
    public String dst=null;
    public String mon=null;
    public String site=null;
    public String host=null;
    public String service=null;

    public String serviceName=null;
    public String hostName=null;

    public String page="0";

    // execution parameters
    public String workDirectory=null;
    public String requestUri=null;
    public String serverName=null;
    public String serverPort=null;
    public String servletPath=null;

    public ParameterBag()
	{

	}

    public Object clone()
    {
	try
	    {
		return super.clone();
	    }
	catch ( CloneNotSupportedException e )
	    {
		return null;
	    }
    }



    public void addParam(String key, String value){
	// update value of parameter key to value

	if (value==null){
	    value="";
	}
	if (key=="serviceName"){
	    serviceName=value;
	}
	if (key=="hostName"){
	    hostName=value;
	}		
	if (key=="src"){
	    src=value;
	}
	if (key=="dst"){
	    dst=value;
	}
	if (key=="mon"){
	    mon=value;
	}
	if (key=="site"){
	    site=value;
	}
	if (key=="host"){
	    host=value;
	}
	if (key=="service"){
	    service=value;
	}
	if (key=="page"){
	    page=value;
	}
	if (key=="interval"){
	    interval=value;
	}
	if (key=="workDirectory"){
	    workDirectory=value;
	}
	if (key=="requestUri"){
	    requestUri=value;
	}
	if (key=="serverName"){
	    serverName=value;
	}
	if (key=="serverPort"){
	    serverPort=value;
	}
	if (key=="servletPath"){
	    servletPath=value;
	}	
    }
    public void setRequestUri (String requestUri){
	this.requestUri=requestUri;
    }
    public void setWorkDirectory(String workDirectory){
	this.workDirectory=workDirectory;
    }

    public String makeLink(){
	String result="";
	result=requestUri+"?";
	if (serviceName!=null){
	    result=result+"serviceName="+serviceName+"&";
	}
	if (hostName!=null){
	    result=result+"hostName="+hostName+"&";
	}	
	if (interval!=null){
	    result=result+"interval="+interval+"&";
	}
	if (src!=null){
	    result=result+"src="+src+"&";
	}
	if (dst!=null){
	    result=result+"dst="+dst+"&";
	}
	if (mon!=null){
	    result=result+"mon="+mon+"&";
	}
	if (site!=null){
	    result=result+"site="+site+"&";
	}
	if (host!=null){
	    result=result+"host="+host+"&";
	}
	if (service!=null){
	    result=result+"service="+service+"&";
	}	
	if (page!=null){
	    result=result+"page="+page+"&";
	}		    
	return result;
    }
 
    public String toHtml(){
	String result="";
	result=result+"interval="+interval+"<br>";
	result=result+"serviceName="+serviceName+"<br>";
	result=result+"hostName="+hostName+"<br>";	
	result=result+"src="+src+"<br>";
	result=result+"dst="+dst+"<br>";
	result=result+"mon="+mon+"<br>";
	result=result+"site="+site+"<br>";
	result=result+"host="+host+"<br>";
	result=result+"service="+service+"<br>";
	result=result+"page="+page+"<br>";
	result=result+"workDirectory="+workDirectory+"<br>";
	result=result+"requestUri="+requestUri+"<br>";
	//result=result+"="++"<br>";
	//result=result+"="++"<br>";
	//result=result+"="++"<br>";
	return result;
    }

    public static String pageAddress(String pageName){
	String result="0";
	if (pageName.equals("Main")){
		result="";
	}
	if (pageName.equals("Throughput Matrix")){
		result="0";
	}	
	if (pageName.equals("Throughput Node")){
		result="2";
	}
	if (pageName.equals("Throughput Node History Table")){
		result="3";
	}	
	if (pageName.equals("Throughput Node History Plot")){
		result="4";
	}
	if (pageName.equals("perfSonar Primitive")){
		result="5";
	}	
	if (pageName.equals("Primitive Node History Table")){
		result="6";
	}
	if (pageName.equals("Link to history table")){
		result="7";
	}
	if (pageName.equals("List Of Services Page")){
		result="8";
	}	
	return result;
    }


    public String toString(){
	String result=toHtml();
	return result;
    }

}

