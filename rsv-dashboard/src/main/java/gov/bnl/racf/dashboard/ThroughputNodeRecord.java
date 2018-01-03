package gov.bnl.racf.dashboard;

import java.sql.Timestamp;

public class ThroughputNodeRecord
{  

    public String moduleName="ThroughputNodeRecord";

    public String source="";
    public String destination="";
    public String monitor="";

    public double throughput_min=0.0;
    public double throughput_max=0.0;
    public double throughput_avg=0.0;
    public double sigma=0.0;

    public String metricName=null;
    public ProbeStatus metricStatus = null; 
    public Timestamp timestamp = null;
    public String serviceType = null;
    public String serviceUri=null;
    public String gatheredAt=null;
    public String summaryData=null;
    public String detailsData = null;
    
    public ThroughputNodeRecord()
	{
	    
	}
}
