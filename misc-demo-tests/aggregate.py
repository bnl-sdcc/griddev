#!/usr/bin/python
def _aggregateinfo( input):
        '''
        This takes a list of job status dicts, and aggregates them by queue,
        ignoring entries without match_apf_queue 
        Input:
        [ { 'match_apf_queue' : 'BNL_ATLAS_1',
            'jobStatus' : '2',
            'globusStatus': 4 },
          { 'match_apf_queue' : 'BNL_ATLAS_1',
            'jobStatus' : '1' }
        ]                        
        
        Output:
        { 'UC_ITB' : { 'jobStatus' : { '1': '17',
                                       '2' : '24',
                                       '3' : '17',
                                     },
                       'globusStatus' : { '1':'13',
                                          '2' : '26',
                                          }
                      },
        { 'BNL_TEST_1' :{ 'jobStatus' : { '1':  '7',
                                          '2' : '4',
                                          '3' : '6',
                                     },
                       'globusStatus' : { '1':'12',
                                          '2' : '46',
                                          }
                      },             
        '''
        queues = {}
        for item in input:
            if not item.has_key('match_apf_queue'):
                # This job is not managed by APF. Ignore...
                continue
            apfqname = item['match_apf_queue']
            # get current dict for this apf queue
            try:
                qdict = queues[apfqname]
            # Or create an empty one and insert it.
            except KeyError:
                qdict = {}
                queues[apfqname] = qdict    
            
            # Iterate over attributes and increment counts...
            for attrkey in item.keys():
                # ignore the match_apf_queue attrbute. 
                if attrkey == 'match_apf_queue':
                    continue
                attrval = item[attrkey]
                # So attrkey : attrval in joblist
                
                
                # Get current attrdict for this attribute from qdict
                try:
                    attrdict = qdict[attrkey]
                except KeyError:
                    attrdict = {}
                    qdict[attrkey] = attrdict
                
                try:
                    curcount = qdict[attrkey][attrval]
                    qdict[attrkey][attrval] = curcount + 1                    
                except KeyError:
                    qdict[attrkey][attrval] = 1
                    
        return queues
          
                        
def test():
    list =  [ { 'match_apf_queue' : 'BNL_ATLAS_1',
                'jobStatus' : '2' },
              { 'match_apf_queue' : 'BNL_ATLAS_1',
                'jobStatus' : '1' },
              { 'match_apf_queue' : 'BNL_ATLAS_1',
                'jobStatus' : '1' },
              { 'match_apf_queue' : 'BNL_ATLAS_2',
                'jobStatus' : '1' },
              { 'match_apf_queue' : 'BNL_ATLAS_2',
                'jobStatus' : '2' },
              { 'match_apf_queue' : 'BNL_ATLAS_2',
                'jobStatus' : '3' },
              { 'match_apf_queue' : 'BNL_ATLAS_2',
                'jobStatus' : '3' },
              { 'match_apf_queue' : 'BNL_ATLAS_2',
                'jobStatus' : '3' }
            ]
    out = _aggregateinfo(list)
    print(out)
    
if __name__ == '__main__':
    test()
    
     