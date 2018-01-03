package gov.bnl.racf.gridinfo;


import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import gov.bnl.racf.gridinfo.SSLCertFilter;

public class GridInfo {
	
	static private Logger log = LoggerFactory.getLogger(GridInfo.class);
	
	public String getClientSubject() {
		log.debug("Retrieving current user DN...");
		String dn =  SSLCertFilter.getClientSubject();
		log.info("User: '" + dn + "' connected.");
		return dn;
		// return "Dummy DN";
	}
	
	public String getClientIssuer() {
		log.debug("Retrieving current user CA Chain...");
		String ca =  SSLCertFilter.getClientIssuer();
		log.info("User CA is: " + ca );
		return ca;
		
	}
	
	public String getClientSerial() {
		log.debug("Retrieving current user cert serial...");
		String s =  SSLCertFilter.getClientSerial();
		log.info("User Cert serial: " + s );
		return s;
	}
	
	public String getClientNotBefore() {
		log.debug("Retrieving current user cert notBefore...");
		String s =  SSLCertFilter.getClientNotBefore();
		log.info("User Cert notBefore: " + s );
		return s;
	}
	
	public String getClientNotAfter() {
		log.debug("Retrieving current user cert notAfter...");
		String s =  SSLCertFilter.getClientNotAfter();
		log.info("User Cert notAfter: " + s );
		return s;
	}
	
	public String getVersion() {
		log.debug("Retrieving version string.");
		return "1.0";
	}
	
	
}