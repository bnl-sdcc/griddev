import datetime
import os

from django import newforms as forms


FORMAT_CHOICES=(
                ('txt', 'csv/text'),
                ('graph','graph/png'),
                )



TYPE_CHOICES=(
              ('counts','counts'),
               ('events','events'),
               ('errors','errors'),             
              )
try:
    dirlist = os.listdir('/data/www/gridsite/daq')
    SITE_CHOICES=[]
    for d in dirlist:
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
    
    starttime = forms.DateTimeField( initial=YESTERDAY)
    endtime = forms.DateTimeField( initial=NOW)
    sitename = forms.ChoiceField(choices=SITE_CHOICES)
    format = forms.ChoiceField(choices=FORMAT_CHOICES, initial="txt")
    datatype = forms.ChoiceField(choices=TYPE_CHOICES, initial="counts")
