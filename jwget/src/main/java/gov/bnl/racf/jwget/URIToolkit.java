package gov.bnl.racf.jwget;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.FilenameFilter;
import java.io.IOException;
import java.io.InputStream;
import java.net.MalformedURLException;
import java.net.URISyntaxException;
import java.net.URL;
import java.net.URI;
import java.security.KeyManagementException;
import java.security.KeyStore;
import java.security.KeyStoreException;
import java.security.NoSuchAlgorithmException;
import java.security.UnrecoverableKeyException;
import java.security.cert.CertificateException;
import java.util.HashMap;
import java.util.List;
import java.util.Iterator;


import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.KeyManagerFactory;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSocketFactory;

import org.apache.commons.cli2.*;
import org.apache.commons.cli2.builder.*;
import org.apache.commons.cli2.commandline.Parser;
import org.apache.commons.cli2.option.*;
import org.apache.commons.cli2.CommandLine;
import org.apache.commons.cli2.util.HelpFormatter;
import org.apache.commons.cli2.Option;
import org.apache.commons.cli2.OptionException;

import org.apache.log4j.Logger;
import org.apache.log4j.BasicConfigurator;
import org.apache.log4j.Level;

import sun.security.validator.ValidatorException;



/**
 * Class to handle validated HTTP, HTTPS, and FILE download of  
 * resources for use by other systems. 
 * 
 * @author Jay Packard <jpackard@bnl.gov>
 * @author John Hover <jhover@bnl.gov>
 *
 */

public class URIToolkit {

	  DefaultOptionBuilder oBuilder;  
  	  ArgumentBuilder aBuilder; 
  	  GroupBuilder gBuilder;
  	  HelpFormatter hf;
  	  String userCertp12;             // PKCS12 format cert for client.    
  	  String userKeyPw;     		  // Cert password. 
  	  HashMap optionhash;	          // Allows retrieval of Option objects by string name. 
  	  File pKeyFile = null;            
  	  String pKeyPassword = null;
  	  
  	  static Logger log = Logger.getLogger(URIToolkit.class);

  	  
	public URIToolkit()
	{
  	  this.oBuilder = new DefaultOptionBuilder();
  	  this.aBuilder = new ArgumentBuilder();
  	  this.gBuilder = new GroupBuilder();
  	  this.hf = new HelpFormatter();
  	
	}
	

	static class CAFilter implements FilenameFilter {
       public boolean accept(File dir, String name) {
           return name.endsWith(".0");
       }
   }

   static class CRLFilter implements FilenameFilter {
       public boolean accept(File dir, String name) {
           return name.endsWith(".crl_url");
       }
   }
   
   /**
    * 
    * 
    * 
    * @param uri
    * @param tempFile
    * @return
    * @throws Exception
    */
   public String parseUri(String uri, String tempFile) throws Exception {
       FileWriter fileWriter = null;
       InputStream inputStream = null;
       try {
           inputStream = getInputStream(uri);
           // write to temp file and string buffer
           StringBuffer buffer = new StringBuffer();
           if (tempFile != null)
               fileWriter = new FileWriter(new File(tempFile));
           int ch;
           while ((ch = inputStream.read()) != -1) {
               buffer.append((char)ch);
               if (tempFile != null)
                   fileWriter.append((char)ch);
           }
                      return buffer.toString();
       } finally {
           if (inputStream != null)
               inputStream.close();
           if (fileWriter != null)
               fileWriter.close();
       }
   }
   
   /**
    * 
    * 
    * 
    * 
    * @param uri
    * @return
    * @throws IOException
    */
   public InputStream getInputStream(String uri) throws IOException{
       	InputStream inputStream = null;
		try
		{       
			URI ui = new URI(uri);
   			log.debug("URI scheme is " + ui.getScheme());
   			log.debug("URI host is " + ui.getHost());
   			log.debug("URI path is " + ui.getPath());

			if (ui.getScheme().equalsIgnoreCase("file")){
				log.debug("get(): Detected File URI, redirecting...");
				return getFile(ui);
				
			}
	
			if ( ui.getScheme().equalsIgnoreCase("https") )
			{
				URL u = new URL(uri);
				log.debug("get(): Detected HTTPS URL, redirecting...");
				return getHTTPS(u);
			}
			else if (ui.getScheme().equalsIgnoreCase("http") )
			{
				URL u = new URL(uri);
				log.debug("get(): Detected HTTP URL, redirecting...");
				return getHTTP(u);
			}
			else 
			{
				log.debug("Unrecognized scheme: " + ui.getScheme() + " Exitting.");
				System.exit(1);
			}
		}
        catch (MalformedURLException mue) {
            mue.printStackTrace();
        }
		catch (IOException ioe) 
		{
			throw ioe;
		}
   		catch (URISyntaxException use)
   		{
   			use.printStackTrace();
   			
   		}
   		catch (ValidatorException ve)
   		{
   			ve.printStackTrace();
   			
   		}
       return inputStream;
   }
   
   /**
    * 
    * @param aURI   A valid URI string.
    * @return       String
    * @throws IOException
    * @throws ValidatorException
    */
   
	public String get(String aURI) throws IOException, ValidatorException
	{
		StringBuffer sb = new StringBuffer();
		InputStream is = this.getInputStream(aURI);
			int c;
			while ( (c = is.read()) != -1 )
			{
				sb.append((char) c);
			}
		return sb.toString();
	} // end get()

	
	private InputStream getFile(URI uri) throws IOException 
	{
		log.info("Getting File URI: " + uri.toString() );
		InputStream ans = null;
		
		try {
			ans = new FileInputStream(uri.getPath());	
	        }
		catch (FileNotFoundException fnfe)
		{	
			fnfe.printStackTrace();
		}
	    return ans;

	} // end getHTTP()
	
	private InputStream getHTTP(URL url) throws IOException 
	{
		log.info("Getting HTTP URL: " + url.toString() );
		InputStream ans = null;
		
		try {
				ans =  url.openStream();
	        }
	        catch (MalformedURLException mue) {
	            mue.printStackTrace();
	        }
	        catch (IOException ioe) {
	            throw ioe;
	        }
	     return ans;

	} // end getHTTP()
   
	private InputStream getHTTPS(URL url) throws IOException, ValidatorException 
	{
		log.info("Getting HTTPS URL: " + url.toString() );
		InputStream ans = null;
		
		try 
		{
			HttpsURLConnection con = (HttpsURLConnection) url.openConnection();
			con.setSSLSocketFactory(this.getFactory());
			ans = url.openStream();
		}
		catch (MalformedURLException mue) 
		{
			mue.printStackTrace();
		}
		catch (IOException ioe) 
		{
			throw ioe;
		}			
		return ans;
		
	} // end getHTTPS() 
   

	/**
	 * 
	 * This method version returns a default socket factory which will validate servers, 
	 * but not use a client cert. 
	 * 
	 * @return SSLSocketFactory
	 */
	private SSLSocketFactory getFactory()
	{
		SSLSocketFactory ssf = null;
		try {
			SSLContext ctx = SSLContext.getInstance("TLS");
			
			if ((pKeyFile != null) && ( pKeyPassword != null))
			{
				KeyManagerFactory kmf = KeyManagerFactory.getInstance("SunX509");
				KeyStore ks = KeyStore.getInstance("PKCS12");
				InputStream ki = new FileInputStream(pKeyFile);
				ks.load(ki, pKeyPassword.toCharArray());
				ki.close();
				kmf.init(ks , pKeyPassword.toCharArray());
				
				ctx.init(kmf.getKeyManagers(), null, null);
				
			}
			else
			{
					
				ctx.init(null, null, null);
			}
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
	
	/**
	 * 
	 * 
	 * @param args
	 * @return
	 */
   public CommandLine parseCommandLine(String[] args) throws OptionException
   {
    	  
    	  CommandLine cl = null;
    	  this.optionhash = new HashMap();
    	  
    	  DefaultOption help = 
    		  this.oBuilder
    		  .withShortName("h")
    	        .withLongName("help")
    	        .withDescription("Print this message.")
    	        .create();
    	  
    	  this.optionhash.put("help", help);
    	  
    	  
    	  Option verbose =
    		  this.oBuilder
    		  .withShortName("v")
    		  .withLongName("verbose")
    		  .withDescription("Do verbose logging.")
    		  .create();
    	  this.optionhash.put("verbose", verbose);

    	  Option debug =
    		  this.oBuilder
    		  .withShortName("d")
    		  .withLongName("debug")
    		  .withDescription("Do debug logging.")
    		  .create();
    	  this.optionhash.put("debug", debug);
    	  
    	  Option certfile =
    		  this.oBuilder
    		  .withShortName("C")
    		  .withLongName("certfile")
    		  .withDescription("User certificate in PKCS format.")
    		  .withArgument(aBuilder
    				  			.withName("certfile")
    				  			.withMinimum(1)
    				  			.withMaximum(1)
    				  			.create() )
    		.create();
    	  this.optionhash.put("certfile", certfile);

    /*	  Option keyfile =
    		  this.oBuilder
    		  .withShortName("K")
    		  .withLongName("keyfile")
    		  .withDescription("User key in .pem format.")
    		  .withArgument(aBuilder
    				  			.withName("keyfile")
    				  			.withMinimum(1)
    				  			.withMaximum(1)
    				  			.create() )
    		.create();
    	  this.optionhash.put("keyfile", keyfile);
    	*/  
    	  Option password =
    		  this.oBuilder
    		  .withShortName("p")
    		  .withLongName("password")
    		  .withDescription("Cert passphrase. ")
    		  .withArgument(aBuilder
    				  			.withName("password")
    				  			.withMinimum(1)
    				  			.withMaximum(1)
    				  			.create() )
    		.create();
    	  this.optionhash.put("password", password);
    	  
    	  
    	  
    	  Option proxyhost =
    		  oBuilder
    		  .withShortName("H")
    		  .withLongName("proxyhost")
    		  .withDescription("HTTP/S Proxy hostname.")
    		  .withArgument(aBuilder
    				  			.withName("proxyhost")
    				  			.withMinimum(1)
    				  			.withMaximum(1)
    				  			.create() )
    		.create();
    	  this.optionhash.put("proxyhost", proxyhost);
    	  
    	  Option proxyport =
    		  oBuilder
    		  .withShortName("P")
    		  .withLongName("proxyport")
    		  .withDescription("HTTP/S Proxy port.")
    		  .withArgument(aBuilder
    				  			.withName("proxyport")
    				  			.withMinimum(1)
    				  			.withMaximum(1)
    				  			.create() )
    		.create();
    	  this.optionhash.put("proxyport", proxyport);
    	  
    	  
    	  Option uri = 
    		  this.aBuilder
    		  .withName("uri")
    			.withMinimum(0)
  	  			.withMaximum(1)
    		  .create();
    	  this.optionhash.put("uri", uri);
    	  
    	  Group options = 
    		  gBuilder
    		  	.withName("options")
    		  	.withOption(help)
    		  	.withOption(debug)
    		  	.withOption(verbose)
    		  	.withOption(certfile)
    		  	//.withOption(keyfile)
    		  	.withOption(password)
    		  	.withOption(proxyhost)
    		  	.withOption(proxyport)
    		  	.withOption(uri)
    		  	.create();
    	 
    	  hf.setShellCommand("jwget");
    	  hf.setGroup(options);
    	  
    	  Parser parser = new Parser();
    	  parser.setGroup(options);
    		  cl = parser.parse(args);
    	  log.debug("parseCommandLine, returning object: " + cl.toString());
    	  return cl;  
      } // end parseCommandLine()s
      
      
      /**
       * May be used from the command line or invoked dynamically, e.g. from unit
       * tests. 
       *
       * Usage: <main> [-C/--certfile FILE -K/-keyfile FILE ] 
       *               [ -H/--proxyhost HOST -P/--proxyport INT ]
       *               [ -D/--cadir       
       *               URI 
       * 
       * URI:
       * http://
       * https://
       * file://
       *
       * @param  uri           an absolute URI
       * @param  usercert      the location of the image, relative to the url argument
       * @param  proxyhost     HTTP/S Proxy server
       * @param  proxyport     HTTP/S Proxy port
       * @param  cacertsdir    absolute path to a CA cert directory. 
       * 
       * 
       */
      public static void main(String[]  args) {    		

    	  log.setLevel(Level.WARN);
    	  BasicConfigurator.configure();
          URIToolkit utk = new URIToolkit();
    	  try{
    		  CommandLine cl = utk.parseCommandLine(args);
    		  
    		  // Handle help
    		  if (cl.hasOption((Option) utk.optionhash.get("help"))) 
    		  {
    			  utk.hf.print();
    			  return;
    		  }

    		  // Handle logging level overrides. 
    		  if (cl.hasOption((Option) utk.optionhash.get("verbose"))) 
    		  {
    			  log.setLevel(Level.INFO);
    		  }
    		  if (cl.hasOption((Option) utk.optionhash.get("debug"))) 
    		  {
    			  log.setLevel(Level.DEBUG);
    		  }

    		  // Handle logging options...
    		  List options= cl.getOptions();
    		  Iterator i = options.iterator();
    		  while (i.hasNext() ){
    			  Option o = (Option) i.next();
    			  log.debug(o.toString());
    		  }
    	  
    		  // Handle proxy host
    		  if (cl.hasOption((Option) utk.optionhash.get("proxyhost"))) {
    			  log.info("Setting proxy host..");
    			  System.setProperty("https.proxyHost", (String)cl.getValue((Option) utk.optionhash.get("proxyhost")));
    			  System.setProperty("http.proxyHost", (String)cl.getValue((Option) utk.optionhash.get("proxyhost")));
    		  }
    		  else
    		  {
    			  log.debug("NOT setting proxy host..");
    		  }
    	  
    		  // Handle proxy port
    		  if (cl.hasOption((Option) utk.optionhash.get("proxyport"))) {
    			  log.info("Setting proxy port..");
    			  System.setProperty("https.proxyPort", (String)cl.getValue((Option) utk.optionhash.get("proxyport")));
    			  System.setProperty("http.proxyPort", (String)cl.getValue((Option) utk.optionhash.get("proxyport")));
    		  }
    		  else
    		  {
    			  log.debug("NOT setting proxy port..");
    		  }
    	  
    		  // Handle user cert
    		  if (cl.hasOption((Option) utk.optionhash.get("usercert"))) {
    			  log.debug("Setting user cert..");
    			  utk.pKeyFile = new File( (String)cl.getValue((Option) utk.optionhash.get("usercert")));
    		  }
    		  else
    		  {
    			  log.debug("NOT setting user cert..");
    		  }
    	  
    		  // Handle cert password
    		  if (cl.hasOption((Option) utk.optionhash.get("password"))) {
    			  log.debug("Setting cert password..");
    			  utk.pKeyPassword = (String)cl.getValue((Option) utk.optionhash.get("password"));
    		  }
    		  else
    		  {
    			  log.debug("NOT setting cert password..");
    		  }
    	  
    	  
       
    		  if (cl.hasOption((Option) utk.optionhash.get("uri")))
    		  {
    			  try
    			  {
    				  log.debug("Beginning...");
    				  String s = utk.get((String) cl.getValue((Option) utk.optionhash.get("uri")));
    				  System.out.println(s);
    			  }
    			  catch ( ValidatorException  ve)
    			  {
    				  log.error("Server validation exception:");
    			  }
    			  catch (Exception ex) 
    			  {
    				  ex.printStackTrace();
    			  }
    		  } // end if hasOption "uri"
    	  }
    	  catch (OptionException oe)
    	  {
    		  System.out.println("Invalid option: " + oe.getMessage());
    		  return;
    	  } 
      } // end main()      
} // end URIToolkit