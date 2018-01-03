package gov.bnl.racf.dashboard;

public class HtmlColor
{   
    private  static String red= "rgb(255, 0, 0)";
    private  static String green= "rgb(51, 255, 51)";
    private  static String yellow="rgb(255, 255, 51)";
    private  static String brown="rgb(204, 102, 0)";
    private  static String white="rgb(255, 255, 255)";
    private  static String black="rgb(0, 0, 0)";

    private String currentColor="";

    public HtmlColor(String inputColor){
	currentColor=translateColor(inputColor);
    }
    public String toHtml(){
	return currentColor;
    }
    public static String translateColor(String inputColor){
	String result="";
	if (inputColor=="red"){
	    result=red;
	}else{
	    if (inputColor=="green"){
		result=green;
	    }else{
		if (inputColor=="yellow"){
		    result=yellow;
		}else{
		    if (inputColor=="brown"){
			result=brown;
		    }else{
			if (inputColor=="white"){
			    result=white;
			}else{
			    if (inputColor=="black"){
				result=black;
			    }else{
				result=white;
			    }
			}
		    }
		}
	    }
	}
	return result;
    }
    public static String htmlColor(String inputColor){
	return translateColor(inputColor);
    }

}


