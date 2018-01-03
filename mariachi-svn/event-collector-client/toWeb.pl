#!/usr/bin/perl -w
#
#
#

use Time::Local;
use strict;

my $paramfile = "site_params.txt";  # the name of the site parameters file
my $tm4file = "TM4.txt";


# read in tm4 parameters
my %param;
my $time;
my $hour  = 0;
my $min   = 0;
my $sec   = 0;
my $day   = 0;
my $month = 0;
my $year  = 0;
my @abbr = qw( Jan Feb Mar Arp May Jun Jul Aug Sep Oct Nov Dec );
my $dateString = "";

for (;;) {
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

# Write HTML
    open (WEB, "+>tm4.html");
    print (WEB "<html><head>");
    print (WEB '<meta http-equiv="refresh" content="30">');
    print (WEB '<meta http-equiv="Content-Language" content="en-us">');
    print (WEB '<meta http-equiv="Content-Type" content="text/html; charset=windows-1252">');
    print (WEB "<title>TM4 Status</title>");
    print (WEB "</head><body>");
    print (WEB "<h1>TM4 Status</h1>");

    print (WEB "<table border='0' width='250' cellpadding='1' cellspacing='1'>");
    print (WEB "<tr>");
    print (WEB "<td width='100'>Current time:</td>");
    print (WEB "<td width='150'>");
    ($sec, $min, $hour, $day, $month, $year) = localtime();
    $year = $year - 100;

    if ($hour < 12) {
        $dateString = sprintf ("%3s   %2d %2d:%02d:%02dam", $abbr[$month], $day, $hour, $min, $sec);
    } else {
        $dateString = sprintf ("%3s   %2d %2d:%02d:%02dpm", $abbr[$month], $day, $hour - 12, $min, $sec);
    }
    print (WEB $dateString);
    print (WEB "</td>");
    print (WEB "</tr><tr>");

    print (WEB "<td width='110'>Last time stamp:</td>");
    print (WEB "<td width='140'>");
    if (length($param{"date"}) >= 8) {
    $month = substr($param{"date"}, 0, 2);
    $day = substr($param{"date"}, 2, 2);
    $year = substr($param{"date"}, 4, 4);
    $hour = substr($param{"time"}, 0, 2);
    $min = substr($param{"time"}, 2, 2);
    $sec = substr($param{"time"}, 4, 2);

    $month -= 1;
    $time = timegm($sec, $min, $hour, $day, $month, $year);

    ($sec, $min, $hour, $day, $month, $year) = localtime($time);
    $year = $year - 100;

    if ($hour < 12) {
        $dateString = sprintf ("%3s   %2d %2d:%02d:%02dam", $abbr[$month], $day, $hour, $min, $sec);
    } else {
        $dateString = sprintf ("%3s   %2d %2d:%02d:%02dpm", $abbr[$month], $day, $hour - 12, $min, $sec);
    }
    print (WEB $dateString);
    }
    print (WEB "</td>");
    print (WEB "</tr></table><p>");

    print (WEB "<table border='0' width='190' cellpadding='1' cellspacing='1'>");
    print (WEB "<tr>");

    # compare last date/time in file to current date/time.  If too much difference (5 minutes), error
    my $x = time();
    print (WEB "<td width='110'>read_TM4</td>");
    if ((time() - $time) <= 300) {    
    print (WEB "<td width='60' bgcolor='#00FF00' align='center'>running</td>");
    } else {
    print (WEB "<td width='60' bgcolor='#FF0000' align='center'>down</td>");
    }
    print (WEB "</tr><tr>");

    print (WEB "<td width='110'>Timing Reference</td>");
    if ($param{reference} eq "ready") {    
    print (WEB "<td width='60' bgcolor='#00FF00' align='center'>$param{reference}</td>");
    } else {
    print (WEB "<td width='60' bgcolor='#FF0000' align='center'>$param{reference}</td>");
    }
    print (WEB "</tr><tr>");

    print (WEB "<td width='110'>Time</td>");
    if ($param{timing} eq "valid") {    
    print (WEB "<td width='60' bgcolor='#00FF00' align='center'>$param{timing}</td>");
    } else {
    print (WEB "<td width='60' bgcolor='#FF0000' align='center'>$param{timing}</td>");
    }
    print (WEB "</tr><tr>");

    print (WEB "<td width='110'>Antenna</td>");
    if ($param{antenna} eq "okay") {    
    print (WEB "<td width='60' bgcolor='#00FF00' align='center'>$param{antenna}</td>");
    } else {
    print (WEB "<td width='60' bgcolor='#FF0000' align='center'>$param{antenna}</td>");
    }
    print (WEB "</tr><tr>");

    print (WEB "<td width='110'>ETT Status</td>");
    if ($param{ettStatus} eq "on") {    
    print (WEB "<td width='60' bgcolor='#00FF00' align='center'>$param{ettStatus}</td>");
    } else {
    print (WEB "<td width='60' bgcolor='#FF0000' align='center'>$param{ettStatus}</td>");
    }
    print (WEB "</tr>");

    print (WEB "</table>");

    if (length($param{ettMsg}) >= 1) {
        print (WEB "<p>Last ETT: ", $param{ettMsg}, "\n");
    }

    print (WEB "</body></html>");

    close (WEB);

# wait
    sleep 30

}
