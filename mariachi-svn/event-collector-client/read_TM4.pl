#!/usr/bin/perl -w
#
# Reads events from the TM4 on a COM port
# Copyright 2006, Jeff Spahn
# Version 1.3
# Updated 5/31/06
#

use strict;

use Win32::SerialPort;

sub logmsg($);
sub openPort($);
sub closePort($);
sub readLine($);
sub readMsg($);


my $paramfile = "site_params.txt";  # the name of the site parameters file
my $eventfile = "logfile.txt";
my $tm4file = "TM4.txt";
my $DEVICE = "COM1";

my $msgNum;
my $msgText;
my $ettString = "";

my $tm4Date = "";
my $tm4Time = "";
my $timingStatus = "";
my $alarmStatus = "";
my $ettStatus = "";
my $refStatus = "";

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
close CONFIG;

if (exists($config{"eventfile"})) {
    $eventfile = $config{"eventfile"};
};

if (exists($config{"port"})) {
    $DEVICE = $config{"port"};
};

&logmsg("read_TM4.pl started");

my $serial = openPort($DEVICE); 

$serial->are_match("\n");       # possible end strings
$serial->lookclear;         # empty buffers


# set up TM4
$serial->write("#13,51");       # request date/time
$serial->write("#22,1,+");      # set ETT on, positive polarity


# read TM4 messages forever
for (;;) {
    ($msgNum, $msgText) = readMsg($serial);

    if ($msgNum eq "51") {      # date and time
        $tm4Date = substr($msgText, 0, 8);
        $tm4Time = substr($msgText, 9, 6);

    } elsif ($msgNum eq "61") {     # timing status
    if (substr($msgText, 0, 1) eq "0") {
        $timingStatus = "not_valid";
    } else {
        $timingStatus = "valid";
    }

    } elsif ($msgNum eq "62") {     # event time-tag
        $ettString = substr($msgText, 0, 2) . "/" . substr($msgText, 2, 2) . "/" . substr($msgText, 4, 4) . "   ";
        $ettString .= substr($msgText, 9, 2) . ":" . substr($msgText, 11, 2) . ":" . substr($msgText, 13, 10) . "  UTC\n";

        open  (EFILE, ">>$eventfile") || &logmsg("Could not open event file $eventfile");
        print (EFILE $ettString);
        close (EFILE);

    } elsif ($msgNum eq "64") {     # oscillator tuning mode
        if (substr($msgText, 0, 1) eq "4") {
            $refStatus = "ready";
        } elsif (substr($msgText, 0, 1) eq "5") {
            $refStatus = "ready";
        } else {
        $refStatus = "not_ready";
    }

    } elsif ($msgNum eq "65") {     # alarm status
        if (substr($msgText, 2, 1) ne "0") {
            $alarmStatus = "fault";
        } else {
            $alarmStatus = "okay";
        }

    } elsif ($msgNum eq "73") {     # ETT status
    if (substr($msgText, 0, 1) eq "0") {
        $ettStatus = "off";
    } else {
        $ettStatus = "on";
    }

    }

    open (TM4LOG, "+>$tm4file") || Error('open', 'file');
    print (TM4LOG "date: ", $tm4Date, "\n");
    print (TM4LOG "time: ", $tm4Time, "\n");
    print (TM4LOG "timing: ", $timingStatus, "\n");
    print (TM4LOG "antenna: ", $alarmStatus, "\n");
    print (TM4LOG "reference: ", $refStatus, "\n");
    print (TM4LOG "ettStatus: ", $ettStatus, "\n");
    print (TM4LOG "ettMsg: ", $ettString, "\n");
    close (TM4LOG);

}


closePort($serial);


#----------------------------------------------------------------------------

sub logmsg($) {
# logs status messages to send_status.log

    my $logfile = "read_TM4.log";                       # the name of the log file

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

#**************************************************************************
#*  Serial functions
#**************************************************************************

#* Open raw serial port using:
#*    8 data bits
#*    1 stop bit
#*    9600 bps
#*    no parity
sub openPort($)  {
    my ($device) = @_;
    my $serial = Win32::SerialPort->new ($device, 1); # on Windows
    die "Can't open serial port $serial: $^E\n" unless ($serial);

    $serial->user_msg(1);
    $serial->databits(8);
    $serial->baudrate(9600);
    $serial->parity("none");
    $serial->stopbits(1);
    $serial->handshake("rts");

    return $serial;
}

sub closePort($)  {
    my ($serial) = @_;
    $serial->close();
}

sub readLine($)  {
    my ($serial) = @_;
    my $gotit = "";

    until ("" ne $gotit) {
        $gotit = $serial->streamline;       # poll until data ready
        last if ($gotit);
        sleep 1;                # polling sample time
    }   

    return $gotit;
}

sub readMsg($) {
    my $msgNum = "0";
    my $msgText = "";
    my ($serial) = @_;

    my $line = readLine($serial);

    my $first = substr $line, 0, 1;
    if ($first eq "#") {
        $msgNum = substr $line, 1, 2;
        $msgText = substr $line, 4, 200;
    }
        
    return ($msgNum, $msgText);
}
