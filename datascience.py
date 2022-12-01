import os
import time
import subprocess
import sys
from sys import platform as _platform

from datascience_formats import *
from datascience_logger import *

sourceBoard = '1'
syncBoard = '0'

FNULL = open(os.devnull, 'w')

if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
    # linux & Mac
    appstart = "./"

elif _platform == "win32":
    appstart = ""


def playloop(vidformat, refformat, logname):
    for f in range(len(vidformat)):

        for r in range(len(refformat)):

            #print("qasource", "-b", str(syncBoard), "-VNTV2_FORMAT_" + str(refformat[r]), "-c1", "-x10", "&")

            #print("qasource", "-b", str(sourceBoard), "-VNTV2_FORMAT_"+str(vidformat[f]), "-c1", "-x0", "-r", "&")

            playsync = subprocess.Popen([appstart + "qasource", "-b", str(syncBoard), "-VNTV2_FORMAT_"+str(refformat[r]), "-c1", "-x10", "&"], stdout=FNULL)
            time.sleep(5)

            playsource1 = subprocess.Popen([appstart + "qasource", "-b", str(sourceBoard), "-VNTV2_FORMAT_"+str(vidformat[f]), "-c1", "-x0", "-r", "&"], stdout=FNULL)
            time.sleep(5)

            writelogtiming(vidformat, f, refformat, r, logname)

            #input('Check all channels and Press Enter')

            time.sleep(1)

            playsource1.kill()

            time.sleep(1)

            playsync.kill()

            subprocess.Popen([appstart + "qakillac", "-b", str(sourceBoard), "-c0", "-n"], stdout=FNULL)

            subprocess.Popen([appstart + "qakillac", "-b", str(syncBoard), "-c0", "-n"], stdout=FNULL)

            # playsource2 = subprocess.Popen([appstart + "qasource", "-b", str(sourceBoard), "-VNTV2_FORMAT_625_5000", "-c1", "-x0", "&"], stdout=FNULL)
            #
            # time.sleep(2)
            #
            # playsource2.kill()
            #
            # time.sleep(1)
            #
            # subprocess.Popen([appstart + "qakillac", "-b", str(sourceBoard), "-c0", "-n"], stdout=FNULL)

def main(args):

    loopcount = 10

    logname = "log_ref_timing.csv"

    try:

        file = open(str(logname), "a")
        file.writelines('Ref_Format,Video_Format,H_Timing,V_Timing\n')
        file.close()

    except Exception:
        print('write log failed')

    for x in range(loopcount):
        playloop(ntscfractionalvidformat, ntscfractionalref, logname)
        time.sleep(2)
        playloop(palvidformat, palref, logname)

if __name__ == '__main__':
    main(sys.argv[1:])