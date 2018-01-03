#!/usr/bin/perl
# file: send_status.pl
# Sends the site status to the server
# Copyright 2006, Jeff Spahn
# Version 1.2
# Updated 5/31/06
#
use strict;
use LWP::UserAgent;
use HTTP::Request::Common;
use Getopt::Long;
use File::Basename;
use Time::Local;

my $paramfile = "site_params.txt";                      # the name of the site parameters file
my $statusfile = "site_status";             # the name of the file with the status
my $tm4file = "TM4.txt";                # most recent TM4 messages
my $url = "http://www-mariachi.physics.sunysb.edu/data/recv_status.php";   # the server's address
my $siteid = "";

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


# check that config file had siteid
if (exists($config{"site"})) {
    $siteid = $config{"site"};
} else {
    &logmsg ("siteid not specified in site_params.txt");
    exit 0;
};

# Get the status from statusfile
open (LFILE, $statusfile) || do {
    &logmsg ("Could not open $statusfile");
    exit 0;
};
my $status = readline(LFILE);                   # the status
close (LFILE);

# Read the TM4 messages
my %param;
my $lastMsgTime;
my $hour  = 0;
my $min   = 0;
my $sec   = 0;
my $day   = 0;
my $month = 0;
my $year  = 0;

# get parameters
open(PARAM, $tm4file) || die ("Couldn't open $tm4file: $!\n");
while (<PARAM>) {
    chomp;                  # no newline
    s/#.*//;                # no comments
    s/^\s+//;               # no leading white
    s/\s+$//;               # no trailing white
    next unless length;     # anything left?
    my ($var, $value) = split(/\s*:\s*/, $_, 2);
    $param{$var} = $value;
} 
close PARAM;

# get date/time of last TM4 message
if (length($param{"date"}) >= 8) {
    $month = substr($param{"date"}, 0, 2);
    $day = substr($param{"date"}, 2, 2);
    $year = substr($param{"date"}, 4, 4);
    $hour = substr($param{"time"}, 0, 2);
    $min = substr($param{"time"}, 2, 2);
    $sec = substr($param{"time"}, 4, 2);
    $month -= 1;
    $lastMsgTime = timegm($sec, $min, $hour, $day, $month, $year);
}


# send the status
my $ua  = LWP::UserAgent->new();
# add proxy info here if needed
if (exists($config{"proxy"})) {
    $ua->proxy('http', $config{"proxy"});
}
my $req = POST $url, 
    Content_Type => 'form-data',
    Content => [
        site_id => $siteid,
        status => $status,
    lastMsgTime => $lastMsgTime,
    timingRef => $param{reference},
    timingStatus => $param{timing},
    antennaStatus => $param{antenna},
    ettStatus => $param{ettStatus},
    ettMsg => $param{ettMsg},
    submit => 1,
    ];

my $response = $ua->request($req);
unless ($response->is_success()) {      # log any errors
    &logmsg ($response->status_line);
    exit 0;
}


exit;

#----------------------------------------------------------------------------

sub logmsg {
# logs status messages to send_status.log

    my $logfile = "send_status.log";                       # the name of the log file

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
