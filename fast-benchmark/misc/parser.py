__author__ = 'Luis Villazon Esteban'

import json
import time
import sys
import os
import commands
from os import listdir
import xml.etree.ElementTree as ET
import argparse
import ipgetter
import SOAPpy

def extract_values(line):
    """Extract the values from the line and return a dictionary with the value, error, and unit"""

    values = line[line.find("(")+1:line.find(")")]
    value = values[:values.find("+")].strip()
    deviation = values[values.find("+/-")+3:].strip()
    unit = line[line.find(")")+1:].strip()
    if unit == 'ms':
            value = '%.5f' % (float(value)/1000)
            deviation = '%.5f' % (float(deviation)/1000)
            unit = 's'
    if float(deviation) == 0:
        return {'value': float(value), 'unit':unit}
    else:
        return {'value': float(value), 'error': float(deviation), 'unit':unit}


def fill_results(result, key, lines, i):
    entries = lines[i][lines[i].find("=")+1:lines[i].find(")")].strip()
    cpu = extract_values(lines[i+1])
    real = extract_values(lines[i+2])
    vmem = extract_values(lines[i+3])
    result.update({key: {'entries': int(entries),
                         'cpu': cpu,
                         'real': real,
                         'vmem': vmem
                        }
                   })


def fill_memory_results(result, key, lines, i):
    def extract_memory_value(line):
        value = line[line.find("INFO")+len("INFO"):]
        value = value[value.find(":")+2:].strip()
        unit = value[value.find(" ")+1:].strip()
        value = value[:value.find(" ")]
        return {'value': float(value), 'unit':unit}

    result.update({key:{ 'vm_data': extract_memory_value(lines[i+1]),
                    'vm_exe': extract_memory_value(lines[i+2]),
                    'VmHWM': extract_memory_value(lines[i+3]),
                    'VmLck': extract_memory_value(lines[i+4]),
                    'VmLib': extract_memory_value(lines[i+5]),
                    'VmPTE': extract_memory_value(lines[i+6]),
                    'VmPeak': extract_memory_value(lines[i+7]),
                    'VmRSS': extract_memory_value(lines[i+8]),
                    'VmSize': extract_memory_value(lines[i+9]),
                    'VmStk': extract_memory_value(lines[i+10]),
                    'VmSwap': extract_memory_value(lines[i+11])}})


def fill_memory_leak_results(result, key, lines, i):
    def extract_memory_value(line):
        value = line[line.find("INFO")+len("INFO"):]
        value = value[value.find(":")+2:].strip()
        unit = value[value.find(" ")+1:].strip()
        value = value[:value.find(" ")]
        if unit == 'ms':
            value = round(value/1000, 5)
            unit = 's'
        return {'value': float(value), 'unit':unit}
        return float(value)
    result.update({key: {'first-evt': extract_memory_value(lines[i+1]),
                         '10th -evt':extract_memory_value(lines[i+2]),
                         'last -evt':extract_memory_value(lines[i+3]),
                         'evt  2-20':extract_memory_value(lines[i+4]),
                         'evt 21-50':extract_memory_value(lines[i+5]),
                         'evt 51+':extract_memory_value(lines[i+6])} })


def parse_kv(rundir):
    result = {'kv': {'start': os.environ['init_kv_test'],
                     'end': os.environ['end_kv_test'],
                     'kv_tag': "KV-Bmk-%s" % args.cloud}}

    path = rundir+"/KV"
    file_name = None
    for f in listdir(path):
        if f.find("PerfMon_summary_") >= 0:
            file_name = "%s/%s" % (path, f)
            break

    if file_name is None:
        send_alert_email()
        return result

    file = open(file_name, "r")
    lines = file.read().split("\n")
    aux_result = None
    for i in range(0, len(lines)):
        line = lines[i]
        if line.find("## PerfMonFlags ##")> 0:
            thread = line[line.find("KV.thr.")+len("KV.thr.")]
            result['kv'].update({"thr_"+thread:{}})
            aux_result = result['kv']['thr_'+thread]
        if line.find("Statistics for 'ini'") > 0:
            fill_results(aux_result, 'initialization', lines, i)
        if line.find("Statistics for 'evt'") > 0:
            fill_results(aux_result, 'evt', lines, i)
        if line.find("Statistics for 'fin'") > 0:
            fill_results(aux_result, 'finalization', lines, i)
        if line.find("memory infos from") > 0:
            fill_memory_results(aux_result, 'memory', lines, i)
        if line.find("vmem-leak estimation") > 0:
            fill_memory_leak_results(aux_result, 'vmem-leak', lines, i)
    return result


def parse_phoronix():
    path = '/home/phoronix/.phoronix-test-suite/test-results'
    result = {'phoronix':{}}
    for f in listdir(path):
        if f.find('pts-results-viewer') < 0 and f[0] is not '.':
            try:
                tree = ET.parse("%s/%s/%s" % (path, f, "test-1.xml"))
                root = tree.getroot()
                metric = root.find('Result').find('Scale').text
                title = root.find('Result').find('Title').text
                value = float(root.find('Result').find('Data').find('Entry').find('Value').text)
                obj = {title: {'value':float(value), 'unit': metric}}

                if title.find('Zip') >= 0:
                    obj['start'] = os.environ['init_7zip']
                    obj['end'] = os.environ['end_7zip']
                elif title.find('LAME') >= 0:
                    obj['start'] = os.environ['init_mp3']
                    obj['end'] = os.environ['end_mp3']
                elif title.find('x264') >= 0:
                    obj['start'] = os.environ['init_x264']
                    obj['end'] = os.environ['end_x264']
                elif title.find('Kernel') >= 0:
                    obj['start'] = os.environ['init_build_linux_kernel']
                    obj['end'] = os.environ['end_build_linux_kernel']

                result['phoronix'].update(obj)
            except Exception:
                pass
    return result


def parse_metadata(id, ip, cloud, vo):
    start_time = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime(int(os.environ['init_tests'])))

    result = {'metadata':{}}
    result.update({'_id': "%s_%s" % (id, start_time)})
    result.update({'_timestamp': start_time})
    result['metadata'].update({'ip': ip})
    result['metadata'].update({'classification': os.environ['HWINFO']})
    result['metadata'].update({'cloud': cloud})
    result['metadata'].update({'UID': id})
    result['metadata'].update({'VO': vo})
    try:
        result['metadata'].update({'pnode': get_pnode()})
    except Exception as e:
        pass
    result['metadata'].update({'osdist':commands.getoutput("lsb_release -d 2>/dev/null").split(":")[1][1:]})
    result['metadata'].update({'pyver': sys.version.split()[0]})
    result['metadata'].update({'cpuname': commands.getoutput("cat /proc/cpuinfo | grep '^model name' | tail -n 1").split(':')[1].lstrip()})
    result['metadata'].update({'cpunum' : int(commands.getoutput("cat /proc/cpuinfo | grep '^processor' |wc -l"))})
    result['metadata'].update({'bogomips': float(commands.getoutput("cat /proc/cpuinfo | grep '^bogomips' | tail -n 1").split(':')[1].lstrip())})
    result['metadata'].update({'meminfo': float(commands.getoutput("cat /proc/meminfo | grep 'MemTotal:'").split()[1])})
    return result


def get_pnode():
    import socket
    user=os.environ['OS_USERNAME']
    password=os.environ['OS_PASSWORD']
    type="NICE"
    endpoint = "https://network.cern.ch/sc/soap/soap.fcgi?v=5"
    ns = "http://network.cern.ch/NetworkService"
    SOAPserver=SOAPpy.SOAPProxy(endpoint, namespace=ns)
    #Get the auth token
    atoken=SOAPserver.getAuthToken(user,password,type)
    #Build the auth header
    authStruct=SOAPpy.structType(data = {"token" :atoken})
    #authStruct._ns1=("ns1","urn:NetworkService")
    authHeader=SOAPpy.headerType(data = {"Auth":authStruct})
    hostname = os.environ['HOSTNAME']
    SOAPserver.header=authHeader
    return SOAPserver.vmGetInfo(hostname).VMParent


def generate_rkv(document):
    rkv = {}
    for thread in document['profiles']['kv']:
        for type in document['profiles']['kv'][thread]:
            if type not in ['evt', 'initialization', 'finalization']: continue;
            if type not in rkv:
                rkv[type] = {}
            entries = 0
            for metric in document['profiles']['kv'][thread][type]:
                if metric == 'entries':
                    entries += document['profiles']['kv'][thread][type]['entries']

                if metric not in ['cpu', 'real']: continue;
                if "%s_values" % metric not in rkv[type]:
                    rkv[type]["%s_values" % metric] = []
                rkv[type]["%s_values" % metric].append(document['profiles']['kv'][thread][type][metric]['value'])
            rkv[type]["entries"] = entries
    return rkv


def send_alert_email():
    try:
        import smtplib
        from email.message import Message
        msg = Message()
        msg['Subject'] = "Error parsing KV benchmark in %s" % parser.id
        msg['From'] = os.environ['MESSAGE_FROM']
        msg['To'] = os.environ['MESSAGE_TO']

        s = smtplib.SMTP(os.environ['SMTP'])
        s.starttls()
        s.login(os.environ['SMTP_USER'], os.environ['SMTP_PASSWORD'])
        s.sendmail(msg['From'], [msg['To']], msg.as_string())
        s.quit()
    except Exception as e:
        #No variables defined to send email
        pass

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--id", nargs='?', help="VM identifier")
    parser.add_argument("-p", "--ip", nargs='?', help="VM Public IP")
    parser.add_argument("-v", "--vo", nargs='?', help="VO")
    parser.add_argument("-c", "--cloud", nargs='?', help="Cloud")
    parser.add_argument("-f", "--file", nargs='?', help="File to store the results", default="result_profile.json")
    parser.add_argument("-d", "--rundir", nargs='?', help="Directory where bmks ran")
    args = parser.parse_args()

    result = parse_metadata(args.id, args.ip, args.cloud, args.vo)
    result.update({'profiles': {}})
    try:
        result['profiles'].update(parse_phoronix())
    except:
        pass
    try:
        result['profiles'].update(parse_kv(args.rundir))
    except:
        pass
    try:
        result['profiles'].update({'rkv': generate_rkv(result)})
    except:
        pass
    try:
        if os.environ['FASTBMK'] != '':
            result['profiles'].update({'fastBmk': {'value': os.environ['FASTBMK'], 'unit': 'HS06'}})
    except Exception as ex:
        pass

    open(args.file, 'w').write(json.dumps(result))
