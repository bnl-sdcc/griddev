/**
 * 
 */
package gov.bnl.racf.jwget;

import java.io.*;
import java.net.*;
import javax.net.ssl.*;
import java.security.*;
import java.security.cert.CertificateException;
import sun.security.validator.ValidatorException;



/**
 * @author jhover
 *
 */
public class HTTPDownloader {

	String CACertDir = "/etc/grid-security/certificates";
	String userCertp12 = "/home/jhover/.globus/jhover-doegrids-2009-2.p12";
	String userKeyPw = "XXXXX";
	
	
	private SSLSocketFactory getFactory (File pKeyFile, String pKeyPassword)
	{
		SSLSocketFactory ssf = null;
		try {
			KeyManagerFactory kmf = KeyManagerFactory.getInstance("SunX509");
			KeyStore ks = KeyStore.getInstance("PKCS12");

			InputStream ki = new FileInputStream(pKeyFile);
			ks.load(ki, pKeyPassword.toCharArray());
			ki.close();
			
			kmf.init(ks , pKeyPassword.toCharArray());
			
			SSLContext ctx = SSLContext.getInstance("TLS");
			//ctx.init(kmf.getKeyManagers(), null, null);
			ctx.init(null, null, null);
			ssf = ctx.getSocketFactory();
		
		}
		catch (NoSuchAlgorithmException nsa) {
			nsa.printStackTrace();
		}
		catch (KeyStoreException kse) {
			kse.printStackTrace();
		}
		catch (FileNotFoundException fnfe) {
			fnfe.printStackTrace();
		}
		catch (CertificateException ce){
			ce.printStackTrace();
		}
		catch (IOException ioe){
			ioe.printStackTrace();
		}
		catch (UnrecoverableKeyException uke)
		{
			uke.printStackTrace();
		}
		catch (KeyManagementException kme)
		{
			kme.printStackTrace();
		}
		return ssf;
		
	} // end getFactory()
	
	
	public String get(String aURL) throws IOException, ValidatorException
	{
		String reply = "";
		URL u = new URL(aURL);
		if ( u.getProtocol().equalsIgnoreCase("https") )
		{
			System.out.println("get(): Detected HTTPS URL..., redirecting...");
			reply = getHTTPS(u);
		}
		else if (u.getProtocol().equalsIgnoreCase("http") )
		{
			System.out.println("get(): Detected HTTP URL..., redirecting...");
			reply = getHTTP(u);
		}
		else {
			System.out.println("Unrecognized protocol: " + u.getProtocol() + " Exitting.");
			System.exit(1);
		}
		return reply;		
	
	} // end get()
	
	private String getHTTPS(URL url) throws IOException, ValidatorException 
	{
		System.out.println("Getting HTTPS URL: " + url.toString() );
		StringBuffer sb = new StringBuffer();
		
		try 
		{
			HttpsURLConnection con = (HttpsURLConnection) url.openConnection();
			con.setSSLSocketFactory(this.getFactory(new File(userCertp12), userKeyPw));
		
			InputStreamReader isr = new InputStreamReader(url.openStream());
			BufferedReader in = new BufferedReader(isr);
			String inputLine;
    
			//grab the contents at the URL
			while ((inputLine = in.readLine()) != null){
				sb.append(inputLine+"\r\n");
			}
		}
		catch (MalformedURLException mue) 
		{
			mue.printStackTrace();
		}
		catch (IOException ioe) 
		{
			throw ioe;
		}			
		return sb.toString();
		
	} // end getHTTPS()
	
	
	private String getHTTP(URL url) throws IOException 
	{
		System.out.println("Getting HTTP URL: " + url.toString() );
		StringBuffer sb = new StringBuffer();
		try {
	    
	            InputStreamReader isr = new InputStreamReader(url.openStream());
	            BufferedReader in = new BufferedReader(isr);
	            String inputLine;
            
	            //grab the contents at the URL
	            while ((inputLine = in.readLine()) != null){
	                sb.append(inputLine+"\r\n");
	            }

	        }
	        catch (MalformedURLException mue) {
	            mue.printStackTrace();
	        }
	        catch (IOException ioe) {
	            throw ioe;
	        }			
		return sb.toString();
	} // end getHTTP()
	
	
	
	
    public static void main( String[] args) {
    	
    	String httpsProxyHost = "proxy.sec.bnl.local";
    	String httpsProxyPort = "3128"; 
    	
    	System.setProperty("https.proxyHost", httpsProxyHost);
    	System.setProperty("https.proxyPort", httpsProxyPort); 
    	
    	
        if (args.length != 1) {
            System.out.println("\nUsage: java -jar <JAR-WITH-DEPS> URL");
            System.out.println("Example: java-jar <JAR-WITH-DEPS>  https://www.amazon.com ");
            System.exit(1);
        }
        try {
            HTTPDownloader hdl = new HTTPDownloader();
            System.out.println("Beginning...");
            String s = hdl.get(args[0]);
            System.out.println(s);
        }
        catch ( ValidatorException  ve)
        {
        	System.out.println("Server validation exception:");
        }
        
        catch (Exception ex) {
            ex.printStackTrace();
        }

    } // end main()

    
} // end HTTPDownloader
