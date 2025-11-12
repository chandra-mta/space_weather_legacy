#!/proj/sot/ska3/flight/bin/python
"""
**update_stereo_data.py**: download stereo data from ftp site

:Author: t. isobe (tisobe@cfa.harvard.edu)
:Maintainer: W. Aaron (william.aaron@cfa.harvard.edu)
:Last Updated: Mar 16, 2021

"""
import os
import sys
import re
import string
import random
import operator
import time
import random
#
#--- reading directory list
#
path = '/data/mta4/Space_Weather/house_keeping/dir_list'

f= open(path, 'r')
data = [line.strip() for line in f.readlines()]
f.close()

for ent in data:
    atemp = re.split(':', ent)
    var  = atemp[1].strip()
    line = atemp[0].strip()
    exec("%s = %s" %(var, line))
#for writing out files in test directory
if (os.getenv('TEST') == 'TEST'):
    os.system('mkdir -p TestOut')
    test_out = os.getcwd() + '/TestOut'
#
#--- append  pathes to private folders to a python directory
#
sys.path.append('/data/mta/Script/Python3.10/MTA/')
#
#--- import several functions
#
import mta_common_functions as mcf
#
#--- temp writing file name
#
rtail  = int(time.time() * random.random())
zspace = '/tmp/zspace' + str(rtail)
#
#--- set data sources and directories
#
stereo_ftp = 'ftp://ftp.swpc.noaa.gov/pub/lists/stereo/sta_impact_5m.txt'
stereo_gif = 'https://services.swpc.noaa.gov/experimental/images/stereo/impact_A_5m_7d.gif'
data_dir   = stereo_dir + 'Data/'
web_dir    = html_dir   + 'STEREO/'

#---------------------------------------------------------------------------------------------------
#-- update_stereo_data: download stereo data from ftp site                                        --
#---------------------------------------------------------------------------------------------------

def update_stereo_data():
    """
    download stereo data from ftp site
    input: none, but read from ftp://ftp.swpc.noaa.gov/pub/lists/stereo/sta_impact_5m.txt
    output: <data_dir>/stereoAdata
            <web_dir>STEREO/Plot/mpact_A_5m_7d.gif
    """
    cmd = 'mkdir -p ' + web_dir + 'Plots/'
    os.system(cmd)
#
#--- copy the data from ftp site
#
    cmd  = 'wget -q -O' + data_dir + 'stereoAdata ' + stereo_ftp 
    os.system(cmd)
#
#--- copy STEREO plot image, if there are enough data points
#
    ifile = data_dir + 'stereoAdata'
    data  = mcf.read_data_file(ifile)

    if len(data)> 28:
        outimg =  web_dir + '/Plots/impact_A_5m_7d.gif'
        #for writing out files in test directory
        if (os.getenv('TEST') == 'TEST'):
            outimg = test_out + "/" + os.path.basename(outimg)
        cmd = 'wget -q -O' + outimg + ' ' + stereo_gif
        os.system(cmd)
#
#--- reversing the image color so that we can get a white background
#
        cmd = 'convert -negate ' + outimg + ' ' + outimg
        os.system(cmd)
#
#--- update html page
#
    cmd = 'cat ./Template/header ' + data_dir +  'stereoAdata  ./Template/imageA  ./Template/footer > ' 
    #for writing out files in test directory
    if (os.getenv('TEST') == 'TEST'):
        cmd = cmd + test_out + "/stereo.html"
    else:
        cmd = cmd +  web_dir + 'stereo.html'
    os.system(cmd)
    
#
#--- stereo B data is not available anymore...
#
#    file = 'ftp://ftp.sec.noaa.gov/pub/lists/stereo/stb_impact_5m.txt'

#---------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    update_stereo_data()
