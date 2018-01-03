
package gov.bnl.racf.gridinfo;

import javax.servlet.Filter;
import javax.servlet.ServletContext;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.security.cert.X509Certificate;
import javax.security.auth.x500.X500Principal;
import java.math.BigInteger;
import java.util.Date;

public class SSLCertFilter implements Filter {
	
	static private ServletContext context;
	static private Logger log = LoggerFactory.getLogger(SSLCertFilter.class);    
	static private ThreadLocal<X509Certificate> certificate = new ThreadLocal<X509Certificate>();
	
	public void doFilter(javax.servlet.ServletRequest servletRequest,
			javax.servlet.ServletResponse servletResponse,
			javax.servlet.FilterChain filterChain) throws java.io.IOException,
			javax.servlet.ServletException {
		
		log.debug("Performing doFilter() in SSLCertFilter...");
		if ("https".equals(servletRequest.getScheme())) {
	        log.debug("This was an HTTPS request");
	      } else {
	        log.debug("This was not an HTTPS request so no client certificate is available.");
	      }
		
		if (servletRequest.getAttribute("javax.servlet.request.X509Certificate") != null) {
			log.debug("servlet X509Certificate is not null...");
			X509Certificate cert = ((X509Certificate[]) servletRequest
					.getAttribute("javax.servlet.request.X509Certificate"))[0];
			certificate.set(cert);  
		}
		log.debug("servlet X509Certificate is null...");
		filterChain.doFilter(servletRequest, servletResponse);
		
	}
	
	public void init(javax.servlet.FilterConfig filterConfig)
	throws javax.servlet.ServletException {
		context = filterConfig.getServletContext();
		log.debug("Performing init() in SSLCertFilter...");
	}
	
	
	public void destroy() {
	}
	
	public static String getClientSubject() {
		X509Certificate cert = certificate.get();
		String resp = "Unset";
		if (cert != null) {
			X500Principal xp = cert.getSubjectX500Principal();
			resp = xp.getName();
		}
		
		return resp;
	} // end getClientDn()
	
	public static String getClientIssuer() {
		X509Certificate cert = certificate.get();
		String resp = "Unset";
		if (cert != null) {
			X500Principal xp = cert.getIssuerX500Principal();
			resp = xp.getName();
		}
		
		return resp;
	} // end getClientDn()
	
	public static String getClientSerial() {
		X509Certificate cert = certificate.get();
		String resp = "Unset";
		if (cert != null) {
			BigInteger cs = cert.getSerialNumber();
			resp = cs.toString();
		}
		
		return resp;		
	} // end getClientSerial()

	public static String getClientNotBefore() {
		X509Certificate cert = certificate.get();
		String resp = "Unset";
		if (cert != null) {
			Date d = cert.getNotBefore();
			resp = d.toString();
		}
		return resp;		
	} // end getClientNotBefore()

	public static String getClientNotAfter() {
		X509Certificate cert = certificate.get();
		String resp = "Unset";
		if (cert != null) {
			Date d = cert.getNotAfter();
			resp = d.toString();
		}
		return resp;		
	} // end getClientNotAfter()
	
	
}