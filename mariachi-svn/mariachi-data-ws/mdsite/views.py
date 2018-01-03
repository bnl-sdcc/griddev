import datetime
import sys
import os
import commands

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
MIMEDOWNLOAD="application/x-msdownload"



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
        #info = ','.join(dir(request.POST))
        #info = "\n".join(request.POST.keys())
        #return HttpResponse(info, mimetype=MIMETXT)
        answer = None
        form = AnalysisForm(request.POST)
        if form.is_valid():
            starttime=form.cleaned_data['starttime']
            endtime=form.cleaned_data['endtime']
            sitename=form.cleaned_data['sitename']
            format=form.cleaned_data['format']
            datatype=form.cleaned_data['datatype']
            filtertype=form.cleaned_data['filtertype']
            interval=form.cleaned_data['interval']
            
            fnstart=str(starttime).replace('-', '')
            fnstart=fnstart.replace(':', '')
            fnstart=fnstart.replace(' ', '-')
            fnend=str(endtime).replace('-', '') 
            fnend=fnend.replace(':', '') 
            fnend=fnend.replace(' ', '-')
            
            dlfilename="%s-%s-%s--%s" % ( sitename, 
                                         datatype,
                                         fnstart,
                                         fnend
                                     )

            if format == 'txt':
                if filtertype == 'avg':
                    #
                    # Since rpy is just not working from within Django, we'll grab
                    # the info via http:// and re-serve it. 
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
                    answer = txtdata.read()

                elif filtertype == 'raw':
                    answer = django_query(
                                       starttime=starttime, 
                                       endtime=endtime, 
                                       sitename=sitename, 
                                       format=format,
                                       datatype=datatype
                                       )
                if answer:
                    if 'display' in request.POST.keys():
                        hr = HttpResponse(answer, mimetype=MIMETXT)
                    elif 'download' in request.POST.keys():
                        hr = HttpResponse(answer, mimetype=MIMEDOWNLOAD)
                        #  self.headers = {'Content-Type': mimetype}
                        cdisp = 'attachment; filename=%s.txt' % dlfilename
                        hr['Content-disposition'] = str(cdisp)
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
                if 'display' in request.POST.keys():
                    hr = HttpResponse(graphdata, mimetype=MIMEPNG)
                elif 'download' in request.POST.keys():
                     hr = HttpResponse(graphdata, mimetype=MIMEDOWNLOAD)
                     cdisp = 'attachment; filename="%s.png"' % dlfilename
                     hr['Content-disposition'] = str(cdisp)
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
            starttime=form.cleaned_data['starttime']
            endtime=form.cleaned_data['endtime']
            sitename=form.cleaned_data['sitename']
            datatype=form.cleaned_data['datatype']
            
            fnstart=str(starttime).replace('-', '')
            fnstart=fnstart.replace(':', '')
            fnstart=fnstart.replace(' ', '-')
            fnend=str(endtime).replace('-', '') 
            fnend=fnend.replace(':', '') 
            fnend=fnend.replace(' ', '-')
            
            dlfilename="%s-%s-%s--%s" % ( sitename, 
                                             datatype,
                                             fnstart,
                                             fnend
                                     )
            answer = django_query(
                               starttime=starttime, 
                               endtime=endtime, 
                               sitename=sitename, 
                               datatype=datatype,
                               format='txt'
                               )
            if answer:
                if 'display' in request.POST.keys():
                    hr = HttpResponse(answer, mimetype=MIMETXT)
                elif 'download' in request.POST.keys():
                     hr = HttpResponse(answer, mimetype=MIMEDOWNLOAD)
                     cdisp = 'attachment; filename="%s.txt"' % dlfilename
                     hr['Content-disposition'] = str(cdisp)
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

     

    
    
def _get_site_context():
    pass            