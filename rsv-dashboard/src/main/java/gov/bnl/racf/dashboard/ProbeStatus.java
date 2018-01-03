package gov.bnl.racf.dashboard;

public class ProbeStatus
{  

    private static int OK=0;
    private static int WARNING=1;
    private static int CRITICAL=2;
    private static int UNKNOWN=3;

    private int status=3;

    public ProbeStatus( int inputStatus)
	{
	    status=inputStatus;
	}
    public ProbeStatus( String inputStatus)
	{
	    status=string2intStatus(inputStatus);
	}    
    public HtmlColor color(){
	HtmlColor statusColor=new HtmlColor("brown");
	if (status==OK){
	    statusColor=new HtmlColor("green");
	}
	if (status==WARNING){
	    statusColor=new HtmlColor("yellow");
	}
	if (status==CRITICAL){
	    statusColor=new HtmlColor("red");
	}	
	if (status==UNKNOWN){
	    statusColor=new HtmlColor("brown");
	}	
	return statusColor;
    }
    public String statusWord(){
	String result="";
	if (status==OK){
	    result="OK";
	}else{
	    if (status==WARNING){
		result="WARNING";
	    }else{
		if (status==CRITICAL){
		    result= "CRITICAL";
		}else{
		    if (status==UNKNOWN){
			result= "UNKNOWN";
		    }else{
			result="UNKNOWN";
		    }
		}
	    }
	}
	return result;
    }
    public String statusWordShort(){
	String result="";
	if (status==OK){
	    result="OK";
	}else{
	    if (status==WARNING){
		result="WARN";
	    }else{
		if (status==CRITICAL){
		    result= "CRIT";
		}else{
		    if (status==UNKNOWN){
			result= "UNKN";
		    }else{
			result="UNKN";
		    }
		}
	    }
	}
	return result;
    }

    public String toString(){
	return statusWord();
    }
    public static int string2intStatus(String inputStatus){
	if (inputStatus.equals("OK")){
	    return OK;
	}else{
	    if (inputStatus.equals("WARNING") || inputStatus.equals("WARN")){  
		return WARNING;
	    }else{
		if (inputStatus.equals("CRITICAL") ||inputStatus.equals("CRIT")){
		    return CRITICAL;
		}else{
		    if (inputStatus.equals("UNKNOWN") ||inputStatus.equals("UNKN")){
			return UNKNOWN;
		    }
		}
	    }
	}
	return UNKNOWN;
    }

    public int statusLevel(){
	int level=-1;
	if (status==OK){
	    level=0;
	}
	if (status==UNKNOWN){
	    level=1;
	}	
	if (status==WARNING){
	    level=2;
	}
	if (status==CRITICAL){
	    level=3;
	}	
	return level;
    }

    

}
