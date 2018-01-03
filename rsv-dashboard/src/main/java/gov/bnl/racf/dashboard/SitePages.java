package gov.bnl.racf.dashboard;

public class SitePages{

    public SitePages()
	{

	}

    public static String pageId(String pageName){
	String result="0";
	if (pageName.equals("Main")){
		result="1";
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
    public static String pageName(String pageId){
	String result="";
	if (pageId==null){
	    result="Main";
	}else{
	    if (pageId.equals("1")){
		result="Main";
	    }
	    if (pageId.equals("2")){
		result="Throughput Node";
	    }
	    if (pageId.equals("3")){
		result="Throughput Node History Table";
	    }
	    if (pageId.equals("4")){
		result="Throughput Node History Plot";
	    }
	    if (pageId.equals("5")){
		result="perfSonar Primitive";
	    }
	    if (pageId.equals("7")){
		result="Link to history table";
	    }
	    if (pageId.equals("8")){
		result="List Of Services Page";
	    }
	}
	return result;
    }
}

