package gov.bnl.racf.dashboard;

public class HtmlLink
{  
    private String linkUrl="";
    private String linkDisplayedText="";
    private String linkTitle="";
     
    public HtmlLink(String inputText )
	{
	    linkDisplayedText=inputText;
	}
   
    public HtmlLink(String inputUrl, String inputText )
	{
	    linkUrl=inputUrl;
	    linkDisplayedText=inputText;
	}
    public HtmlLink(String inputUrl, String inputText,String inputTitle )
	{
	    linkUrl=inputUrl;
	    linkDisplayedText=inputText;
	    linkTitle=inputTitle;
	}
   
    public String toHtml(){
	String result="";
	if ( !emptyLink()){
	    if (linkTitle==""){
		result="<a href=\"" + linkUrl + "\">"+linkDisplayedText+"</a>";
	    }else{
		result="<a href=\"" + linkUrl + "\" title=\""+linkTitle+"\">"+linkDisplayedText+"</a>";
	    }
	}else{
	    result=linkDisplayedText;
	}
	return result;
    }

    public String toString(){
	return toHtml();
    }

    public boolean emptyLink(){
	if ( linkUrl!=""){
	    return false;
	}else{
	    return true;
	}
    }

}
