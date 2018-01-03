import datetime
import sys
import os

from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render_to_response
from mdsite.forms import DataqueryForm, AnalysisForm

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
# Forms-based data analysis and graphing app
#    
def dataquery_analysis(request):
    if request.method == 'GET':
        form = AnalysisForm()
        return render_to_response('analysis.html', {'form' : form})
    elif request.method == 'POST':
        form = AnalysisForm(request.POST)
        if form.is_valid():
            starttime=form.clean_data['starttime']
            endtime=form.clean_data['endtime']
            sitename=form.clean_data['sitename']
            format=form.clean_data['format']
            datatype=form.clean_data['datatype']
            filtertype=form.clean_data['filtertype']
            interval=form.clean_data['interval']
            if format == 'txt':
                if filtertype == 'avg':
                    #
                    # Since rpy is just not working from within Django, we'll grab
                    # the image via http:// and re-serve it. 
                    #
                    import urllib2
                    TFORMAT="%Y-%m-%dT%H:%M:%S"
                    hostport="www.mariachi.stonybrook.edu"
                    url = "http://%s/mariachi-ws/dataquery/analysis?site=%s&start=%s&end=%s&datatype=%s&interval=%d" % (
                                    hostport,
                                    sitename, 
                                    starttime.strftime(TFORMAT),
                                    endtime.strftime(TFORMAT),
                                    datatype,
                                    interval
                                    )
                    opener = urllib2.build_opener()
                    txtdata = urllib2.urlopen( url )
                    data = txtdata.read()
                    #(fd, graphfile) = mkstemp()
                    #f = open("/tmp/graphimage.png", 'w')
                    #f = open(graphfile, 'w')
                    #f.write(graphdata)
                    #f.close()
                    hr = HttpResponse(data, mimetype=MIMETXT)
                    return hr
                    
                    
                elif filtertype == 'raw':
                    answer = django_query(
                                       starttime=starttime, 
                                       endtime=endtime, 
                                       sitename=sitename, 
                                       format=format,
                                       datatype=datatype
                                       )
                if answer:
                    hr = HttpResponse(answer, mimetype=MIMETXT)
                else:
                    hr = HttpResponse("No data for this interval.", mimetype=MIMETXT)
                return hr
            
            elif format == 'graph':
                #
                # Since rpy is just not working from within Django, we'll grab
                # the image via http:// and re-serve it. 
                #
                import urllib2
                TFORMAT="%Y-%m-%dT%H:%M:%S"
                #hostport = request.environ['HTTP_HOST']
                hostport="www.mariachi.stonybrook.edu"
                url = "http://%s/mariachi-ws/dataquery/query?site=%s&start=%s&end=%s&datatype=%s&graph=1" % (
                                hostport,
                                sitename, 
                                starttime.strftime(TFORMAT),
                                endtime.strftime(TFORMAT),
                                datatype,
                                )
                #return HttpResponse("info: %s" % url, mimetype=MIMETXT)

                opener = urllib2.build_opener()
                graphimage = urllib2.urlopen( url )
                graphdata = graphimage.read()
                #(fd, graphfile) = mkstemp()
                #f = open("/tmp/graphimage.png", 'w')
                #f = open(graphfile, 'w')
                #f.write(graphdata)
                #f.close()
                hr = HttpResponse(graphdata, mimetype=MIMEPNG)
                return hr
        else:
            return HttpResponse("Form not valid. Try again.", mimetype=MIMETXT)
    



#
# Forms-based raw data retrieval app
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
            datatype=form.clean_data['datatype']
            answer = django_query(
                               starttime=starttime, 
                               endtime=endtime, 
                               sitename=sitename, 
                               datatype=datatype,
                               format='txt'
                               )
            if answer:
                hr = HttpResponse(answer, mimetype=MIMETXT)
            else:
                hr = HttpResponse("No data for this interval.", mimetype=MIMETXT)
            return hr
        else:
            return HttpResponse("Form not valid. Try again.", mimetype=MIMETXT)

def rpy_test(request):
    import rpy
    myr = rpy.r
    st = myr.r
    resp = HttpResponse("Rpy imported OK. %s" % st, mimetype=MIMETXT)
    
    
            