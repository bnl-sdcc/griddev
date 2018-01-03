#!/bin/env python

import os
import random
import multiprocessing

UNITS = {'HS06': 1., 'SI00': 1. / 344.}


def getCPUNormalization(i, reference='HS06', iterations=1):
    """
    Get Normalized Power of the current CPU in [reference] units
    """
    if reference not in UNITS:
        print('Unknown Normalization unit %s' % str(reference))
    """
        return S_ERROR( 'Unknown Normalization unit %s' % str( reference ) )
    """
    try:
        iter = max(min(int(iterations), 10), 1)
    except (TypeError, ValueError), x:
        print(x)
    """
        return S_ERROR( x )
    """

    # This number of iterations corresponds to 360 HS06 seconds
    n = int(1000 * 1000 * 12.5)
    calib = 360.0 / UNITS[reference]

    m = 0L
    m2 = 0L
    p = 0
    p2 = 0
    # Do one iteration extra to allow CPUs with variable speed
    for i in range(iterations + 1):
        if i == 1:
            start = os.times()
        # Now the iterations
        for j in range(n):
            t = random.normalvariate(10, 1)
            m += t
            m2 += t * t
            p += t
            p2 += t * t

    end = os.times()
    cput = sum( end[:4] ) - sum( start[:4] )
    wall = end[4] - start[4]

    """
    if not cput:
        return S_ERROR( 'Can not get used CPU' )
    """

    return calib * iterations / cput
    """
    print( {'CPU': cput, 'WALL':wall, 'NORM': calib * iterations / cput, 'UNIT': reference } )
    return S_OK( {'CPU': cput, 'WALL':wall, 'NORM': calib * iterations / cput, 'UNIT': reference } )
    """


cores = multiprocessing.cpu_count()
pool = multiprocessing.Pool(processes=cores)
print float(sum(pool.map(getCPUNormalization, range(cores)))/cores)
