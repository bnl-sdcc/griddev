#!/usr/bin/perl
# file: send_new_event.pl
# Sends a new MARIACHI scintillator event to the server
# Copyright 2006, Jeff Spahn
# Vesion 1.1
# Updated 4/18/06
#
use strict;
use LWP::UserAgent;
use HTTP::Request::Common;
use Getopt::Long;
use File::Basename;
use Time::Local;

my $lastfile = "last_event";                # the name of the file with the last event sent
my $url = "http://www-mariachi.physics.sunysb.edu/data/recv_new_event.php";   # the server's address
my $siteid = "";
my $eventfile = "";

# read in configuration parameters
my %config;
open(CONFIG, "site_params.txt") || die ("Couldn't open site_params.txt: $!\n");
while (<CONFIG>) {
    chomp;                  # no newline
    s/#.*//;                # no comments
    s/^\s+//;               # no leading white
    s/\s+$//;               # no trailing white
    next unless length;     # anything left?
    my ($var, $value) = split(/\s*=\s*/, $_, 2);
    $config{$var} = $value;
} 


# check that config file had siteid and eventfile
if (exists($config{"site"})) {
    $siteid = $config{"site"};
} else {
    &logmsg ("siteid not specified in site_params.txt");
    exit 0;
};  
if (exists($config{"eventfile"})) {
    $eventfile = $config{"eventfile"};
} else {
    &logmsg ("eventfile not specified in site_params.txt");
    exit 0;
};  

# Get the last event sent
my $lastsent = "";                          # the last event sent
unless (open (LFILE, $lastfile)) { 
    &logmsg ("Could not open $lastfile"); 
    die ("Couldn't open $lastfile : $!\n");
}

$lastsent = substr(readline(LFILE), 0, 34);     # the last event sent
close (LFILE);



# Get the last event in the event file
open (EFILE, $eventfile) || do {
    &logmsg ("Could not open $eventfile");
    exit 0;
};
my $lastevent = "";
while (<EFILE>) {$lastevent = $_;}              # assigns each line in turn to $_
close (EFILE);
$lastevent = substr($lastevent, 0, 34); 

# if the last event in the event file does not match the last event sent, send it
if ($lastevent ne $lastsent) {
    # convert last event time to UNIX seconds from epoch
    my $mon  = substr($lastevent,  0, 2) - 1;
    my $mday = substr($lastevent,  3, 2);
    my $year = substr($lastevent,  6, 4);
    my $hour = substr($lastevent, 13, 2);
    my $min  = substr($lastevent, 16, 2);
    my $sec  = substr($lastevent, 19, 2);

    my $timesec = timegm($sec, $min, $hour, $mday, $mon, $year);
    my $timestamp = sprintf("%010d", $timesec);

    # POST the new event
    my $ua  = LWP::UserAgent->new();
    # add proxy info here if needed
    if (exists($config{"proxy"})) {
        $ua->proxy('http', $config{"proxy"});
    }
    my $req = POST $url, 
        Content_Type => 'form-data',
        Content => [
        site_id => $siteid,
            event_time => $timestamp,
        submit => 1,
        ];

    my $response = $ua->request($req);
    unless ($response->is_success()) {          # log any errors
        &logmsg ($response->status_line);
        exit 0;
    }

     # update the last event sent
    open (LFILE, ">$lastfile") || do {
        &logmsg ("Could not open $lastfile to update");
        exit 0;
    };
    print (LFILE $lastevent, "\n");                  # the last event sent
    close (LFILE);
} 

exit;

#----------------------------------------------------------------------------

sub logmsg {
# logs status messages to send_new_event.log

    my $logfile = "send_new_event.log";                       # the name of the log file

    # Get the local time
    (my $sec,my $min,my $hour,my $mday,my $mon,my $year,my $wday,my $yday,my $isdst) = gmtime(time);
    $mon += 1;
    $year +=1900;
    my $tstamp = sprintf("%04d.%02d.%02d %02d:%02d:%02d  ", $year, $mon, $mday, $hour, $min, $sec);

    # append the message to the log file
    open (LOG, ">>$logfile") || Error('open', 'file');
    print (LOG $tstamp, @_, "\n");
    close (LOG);
}
