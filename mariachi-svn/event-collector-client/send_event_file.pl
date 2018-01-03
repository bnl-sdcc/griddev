#!/usr/bin/perl
# file: send_event_file.pl
# Uploads MARIACHI scintillator event files to the server
# Copyright 2006, Jeff Spahn
# Version 1.1
# Updated 4/18/06
#
use strict;
use LWP::UserAgent;
use HTTP::Request::Common;
use Getopt::Long;
use File::Basename;

my $paramfile = "site_params.txt";                       # the name of the site parameters  file
my $url = "http://www-mariachi.physics.sunysb.edu/data/recv_event_file.php";   # the server's address
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


# Get the local time in UTC
(my $sec,my $min,my $hour,my $mday,my $mon,my $year,my $wday,my $yday,my $isdst) = gmtime(time);
$year = sprintf("%02d", $year % 100);
$mon += 1;
$mon = sprintf("%02d", $mon % 100);
$mday = sprintf("%02d", $mday % 100);
$hour = sprintf("%02d", $hour % 100);
$min = sprintf("%02d", $min % 100);

my $fname = $year . $mon . $mday . $hour . $min;        # the renamed event file  YYMMDDhhmm

# Rename the event file
if (rename($eventfile, $fname) != 1) {
    &logmsg ("Could not rename " . $eventfile . " to " . $fname);
    &logmsg ($eventfile . " does not exist.") unless -e $eventfile;
    exit 0;
};

# set up POST
my $ua  = LWP::UserAgent->new();
# add proxy info here if needed
if (exists($config{"proxy"})) {
    $ua->proxy('http', $config{"proxy"});
}
my $req = POST $url, 
    Content_Type => 'form-data',
    Content => [
    MAX_FILE_SIZE => 300000,
    site_id => $siteid,
    submit => 1,
    userfile =>  [ $fname ]
    ];
my $response = $ua->request($req);

# log the response from the POST
&logmsg ("POST ", $fname, "  ", $response->status_line);

if ($response->is_success()) { 
    exit; 
} else {
    exit 0;
}

#----------------------------------------------------------------------------

sub logmsg {
# logs status messages to send_event_file.log

    my $logfile = "send_event_file.log";                       # the name of the log file

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
