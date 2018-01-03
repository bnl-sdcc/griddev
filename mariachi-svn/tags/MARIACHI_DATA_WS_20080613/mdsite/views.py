import datetime
import sys
import os

from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render_to_response
from mdsite.forms import DataqueryForm

if os.path.exists('/home/jhover/devel/mariachi-data-ws'):
    sys.path.append('/home/jhover/devel/mariachi-data-ws')


from mariachiws.dataquery import django_query

MIMEHTML="text/html"
MIMETXT="text/plain"
MIMEJPG="image/jpeg"
MIMESGML="text/sgml"
MIMEPNG="image/png"
MIMEBMP="image/bmp"
MIMEPDF="appplication/pdf"



def current_datetime(request):
    now = datetime.datetime.now()
    #html="<html><body>It is now %s.</body></html>" % now
    t = get_template('mainpage.html')
    html = t.render(Context( {'current_date' : now }  ) )
    return HttpResponse(html)

def data_search(request):
    if request.method == 'GET':
        t = get_template('datapage.html')
        html = t.render(Context())
        return HttpResponse(html)
    elif request.method == 'POST':
        str = "sometextdata"
        return HttpResponse(str)
#
# Forms-based graphic data retreival app
#    
def dataquery_search(request):
    if request.method == 'GET':
        form = DataqueryForm()
        return render_to_response('dataquery.html', {'form' : form})

    elif request.method == 'POST':
        form = DataqueryForm(request.POST)
        if form.is_valid():
            starttime=form.clean_data['starttime']
            endtime=form.clean_data['endtime']
            sitename=form.clean_data['sitename']
            format=form.clean_data['format']
            datatype=form.clean_data['datatype']
            if format == 'txt':
                answer = django_query(
                                   starttime=starttime, 
                                   endtime=endtime, 
                                   sitename=sitename, 
                                   format=format,
                                   datatype=datatype
                                   )
                hr = HttpResponse(answer, mimetype=MIMETXT)
                return hr
            elif format == 'graph':
                #
                # Since rpy is just not working from within Django, we'll grab
                # the image via http:// and re-serve it. 
                #
                
                import urllib2
                width="800"
                TFORMAT="%Y-%m-%dT%H:%M:%S"
                url = "http://www.mariachi.stonybrook.edu/mariachi-ws/dataquery/query?site=%s&start=%s&end=%s&graph=1&width=%s" % (
                                sitename, 
                                starttime.strftime(TFORMAT),
                                endtime.strftime(TFORMAT),
                                width
                                )
                opener = urllib2.build_opener()
                graphimage = urllib2.urlopen( url )
                graphdata = graphimage.read()
                #f = open("/tmp/graphimage.png", 'w')
                #f.write(graphdata)
                #f.close()
                hr = HttpResponse(graphdata, mimetype=MIMEPNG)
                return hr
        else:
            return HttpResponse("Form not valid. Try again.", mimetype=MIMETXT)

def rpy_test(request):
    import rpy
    myr = rpy.r
    st = myr.r
    resp = HttpResponse("Rpy imported OK. %s" % st, mimetype=MIMETXT)
    
    
            