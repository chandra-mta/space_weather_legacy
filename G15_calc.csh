#! /usr/bin/env /bin/csh


set SPACE_Wdir=/data/mta/space_weather
set WEBdir=/data/mta/www/MIRROR

#set today=`date '+%y%m%d'`

# 01/14/02 BDS -SEC data problems, changed to www.sec.noaa.gov
#   old links marked with #sec

set file = ftp://ftp.sec.noaa.gov/pub/lists/particle/Gs_part_5m.txt

lynx -source $file >! $SPACE_Wdir/G15returned1

    tail -24 $SPACE_Wdir/G15returned1 | head -24 >! $SPACE_Wdir/G15returned

    #run nawkscript to calculate averages and mins
    gawk -F" " -f $SPACE_Wdir/G15_process.nawk $SPACE_Wdir/G15returned >! $SPACE_Wdir/G15data

#/data/mta4/space_weather/G15_yellow_viol.pl # check for violations
#/data/mta4/space_weather/G15_red_viol.pl # check for violations

#go collect the image 
# copy it over, instead of linking
lynx -source http://services.swpc.noaa.gov/images/satellite-env.gif >! $WEBdir/satenvBL.gif

#####################################################################

#go collect the second image image 
# copy it over, instead of linking
lynx -source http://services.swpc.noaa.gov/images/goes-proton-flux.gif >! $WEBdir/goes_pro_3d.gif
lynx -source http://services.swpc.noaa.gov/images/goes-xray-flux.gif >! $WEBdir/goes_Xray.gif

cat $SPACE_Wdir/G15header $SPACE_Wdir/G15data  $SPACE_Wdir/G15image $SPACE_Wdir/G15image2  $SPACE_Wdir/G15footer >! $WEBdir/G15.html

endif


