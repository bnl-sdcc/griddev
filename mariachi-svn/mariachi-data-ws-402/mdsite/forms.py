import datetime
import os

from django import forms

FORMAT_CHOICES=(
                ('txt', 'csv/text'),
                ('graph','graph/png'),
                )

FILTER_CHOICES=(
                ('raw','none'),
                ('avg','averaged'),                
                )


DTYPE_CHOICES=(
              ('counts','counts'),
               ('events','events'),
               ('errors','errors'), 
               ('weather','weather'),             
              )

ATYPE_CHOICES=(
              ('counts','counts'),
               ('events','events'),
               ('errors','errors'), 
               ('weather','weather'),
               ('counts,weather','counts,weather'),             
              )

try:
    #
    # FIXME: This path should be pulled from a global config.
    #
    datadir = '/data/www/gridsite/daq'
    dirlist = os.listdir(datadir)
    dirlist.sort()
    SITE_CHOICES=[]
    for d in dirlist:
        fullpath = "%s/%s" % (datadir, d)
        if os.path.isdir(fullpath):
            SITE_CHOICES.append((d,d))
        
except OSError:
    SITE_CHOICES=(
              ('testsite','testsite'),
              ('testsite2','testsite2'),
              )


class DataqueryForm(forms.Form):
    
    FORMAT="%Y-%m-%d %H:%M:%S"
    td=datetime.datetime.utcnow()
    NOW=td.strftime(FORMAT)
    yd = datetime.datetime.utcnow() - datetime.timedelta(1)
    YESTERDAY=yd.strftime(FORMAT)
    
    starttime = forms.DateTimeField(label="Start Time", initial=YESTERDAY)
    endtime = forms.DateTimeField(label="End Time", initial=NOW)
    sitename = forms.ChoiceField(label="Site Name", choices=SITE_CHOICES)
    datatype = forms.ChoiceField(label="Data Type", choices=DTYPE_CHOICES, initial="counts")

    
    
class AnalysisForm(forms.Form):
    
    FORMAT="%Y-%m-%d %H:%M:%S"
    td=datetime.datetime.utcnow()
    NOW=td.strftime(FORMAT)
    yd = datetime.datetime.utcnow() - datetime.timedelta(1)
    YESTERDAY=yd.strftime(FORMAT)
    
    starttime = forms.DateTimeField(label="Start Time", initial=YESTERDAY)
    endtime = forms.DateTimeField(label="End Time", initial=NOW)
    sitename = forms.ChoiceField(label="Site Name", choices=SITE_CHOICES)
    format = forms.ChoiceField(label="Output Format", choices=FORMAT_CHOICES, initial="txt")
    datatype = forms.ChoiceField(label="Data Type" , choices=ATYPE_CHOICES, initial="counts")
    filtertype = forms.ChoiceField(label="Processing Type", choices=FILTER_CHOICES, initial="avg")
    interval = forms.IntegerField(label="Averaging Interval (minutes)", initial=30)
