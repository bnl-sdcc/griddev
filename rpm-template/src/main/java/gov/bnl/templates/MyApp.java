package gov.bnl.templates;

//import org.apache.commons.logging.*;

public class MyApp {
	
	//static private Log log = LogFactory.getLog(MyApp.class);
	
	private String myvariable ;
	
	public MyApp() {
		myvariable = "Hello.";
		
	}
	
	public String getVar(){
		return myvariable;
		
	}
	
	public void setVar(String s) {
		myvariable = s;
	}
	
	
	public static void main(String[] args) {
		//log.info("Hi there log");
		System.out.println("This is MyApp...\n");
		
	}
}



