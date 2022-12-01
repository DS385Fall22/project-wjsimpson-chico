#! /usr/bin/env python

from ajalab.snmp.wfmGetSetFunctions import WFM_GetSetFunctions

scopeip = '10.3.71.56'

wfm = WFM_GetSetFunctions(scopeip)

def writelogtiming(vidformat, f, refformat, r, logname):

    returnedVideoFormat = wfm.wfmGetVideoFormat()
    returnedRefFormat = wfm.wfmGetRefFormat()
    returnedHRefTiming = wfm.wfmGetHRefTiming()
    returnedVRefTiming = wfm.wfmGetVRefTiming()

    ### Will fail if reference isn't detected ###
    if returnedHRefTiming[0:4] == "Unlo":
        f_returned_h_ref_timing = 9.99
    else:
        f_returned_h_ref_timing = float(returnedHRefTiming[0:4])

    try:
        with open(logname, "a") as text_file:
            print(f"{refformat[r]},{vidformat[f]},{f_returned_h_ref_timing},{returnedVRefTiming}", file=text_file)
    except Exception:
        print('write log failed')


