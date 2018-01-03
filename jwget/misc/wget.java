import java.io.*;
import java.net.*;
import java.util.Vector;

/** This class does a simple HTTP GET and writes the retrieved content to a local file
 * 
 * @author Brian Pipa - http://pipasoft.com
 * @version 1.0
 */
public class wget {

    static final String FS = File.separator;

    /** This method does the actual GET
     * 
     * @param theUrl The URL to retrieve
     * @param filename the local file to save to
     * @exception IOException 
     */
    public void get(String theUrl, String filename) throws IOException
    {
        try {
            URL gotoUrl = new URL(theUrl);
            InputStreamReader isr = new InputStreamReader(gotoUrl.openStream());
            BufferedReader in = new BufferedReader(isr);

            StringBuffer sb = new StringBuffer();
            String inputLine;
            boolean isFirst = true;
            
            //grab the contents at the URL
            while ((inputLine = in.readLine()) != null){
                sb.append(inputLine+"\r\n");
            }
            //write it locally
            createAFile(filename, sb.toString());
        }
        catch (MalformedURLException mue) {
            mue.printStackTrace();
        }
        catch (IOException ioe) {
            throw ioe;
        }
    }

    //creates a local file
    /** Writes a String to a local file
     * 
     * @param outfile the file to write to
     * @param content the contents of the file
     * @exception IOException 
     */
    public static void createAFile(String outfile, String content) throws IOException {
        FileOutputStream fileoutputstream = new FileOutputStream(outfile);
        DataOutputStream dataoutputstream = new DataOutputStream(fileoutputstream);
        dataoutputstream.writeBytes(content);
        dataoutputstream.flush();
        dataoutputstream.close();
    }

    /** The main method.
     * 
     * @param args 
     */
    public static void main(String[] args) {
        if (args.length != 2) {
            System.out.println("\nUsage: java wget URL localfilename");
            System.out.println("Example: java wget http://google.com google.html");
            System.exit(1);
        }
        try {
            wget httpGetter = new wget();
            httpGetter.get(args[0], args[1]);
        }
        catch (Exception ex) {
            ex.printStackTrace();
        }

    }
}