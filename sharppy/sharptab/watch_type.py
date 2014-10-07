from sharppy.sharptab import *
import numpy as np

def wind_chill(prof):
    # Needs to be tested
    # Equation from www.nws.noaa.gov/os/windchill/index.shtml
    #
    sfc_temp = thermo.ctof(prof.tmpc[prof.get_sfc()])
    sfc_wspd = utils.KTS2MPH(prof.wspd[prof.get_sfc()])

    wind_chill = 35.74 + (0.6215*sfc_temp) - (35.75*(sfc_wspd**0.16))\
               + 0.4275 * (sfc_temp) * (sfc_wspd**0.16)
    return wind_chill
    
def precip_type(prof):
    #
    # This function looks at the current SHARPPY profile (prof)
    # and makes a single guess of the precipitation type associated with
    # that profile.
    #
    # it would be nice to produce probabilites of the preciptation type using
    # different methods, but it's 12 AM now.
    #
    # it would also be nice to have BUFKIT's precpitation intensity and type algorithm

    # Step 1: Check for ice in a cloud (is there a cloud with temps of -10 to -18 C?)

    # if no ice in cloud, check surface temp
    # if surface temp > 0 C, it's rain
    # if surface temp < 0 C, it's freezing rain

    # if there is ice in the cloud, what are the temperatures below it?
    # if the temperature below is less than 0.5 C, it's snow, but ony if T_w <= 0 C
    # otherwise if T_w > 0 C in the lowest 100 meters, and sfc T_w > 33 F, it's rain

    # if the temperatures below the ice cloud are between 0.5 to 3 C, there will be melting
    # if T_w or T are <= 0C, it's a mix (if warm layer is near 1 C) or sleet ( if warm layer is near 3 C)
    # if T_w >= 0 C in lowest 100 m and T_w > 33F, it's rain or drizzle

    # if the temperatures below the ice cloud are > 3 C, there's total melting
    # if minimum cold layer temp is > -12 C and sfc_T <= 0 C, it's freezing rain
    # if minimum cold layer temp is > -12 C and sfc_T > 0 C, it's rain.
    # if minimum cold layer temp is < -12 C and sfc_T_w < 33 F, it's snow and sleet
    return

def possible_watch(prof):
    #
    # This function looks at the current SHARPPY profile (prof)
    # and creates a list of possible watch types from this profile
    # using critera for the different watches, as well as some
    # subjectively determined thresholds.
    #
    # (it would be nice if someone made a database of soundings and watch types
    # to find which indices corresponded to which types of watches)
    #
    # Watch types covered in this code:
    # - Tornado Watch
    # - PDS Tornado Watch
    # - Severe Thunderstorm Watch
    # - PDS Severe Thunderstorm Watch
    # - Flash Flood Watch
    # - Blizzard Watch
    # - Winter Storm Watch
    # - Wind Chill Watch
    # - Fire Weather Watch
    # - Excessive Heat Watch
    # - Freeze Watch
    
    """
        Updated on 10/6/2014 - Added Rich Thompson's code
    
        Requires these calculations to already be in the profile object:
        STP_EFF
        MLCAPE
        SHIP

    """
        
    watch_types = []
    colors = []
    

    """BEGIN RICH'S DECISION TREE CODE"""
    lr1 = params.lapse_rate( prof, 0, 1000, pres=False )
    stp_eff = prof.stp_cin
    stp_fixed = prof.stp_fixed
    if stp_eff >= 3 and stp_fixed >= 3 and prof.srh1km >= 200 and prof.right_esrh >= 200 and prof.srw_4_6km >= 15.0 and \
        prof.sfc_8km_shear > 45.0 and prof.sfcpcl.lclhght < 1000. and prof.mlpcl.lclhght < 1200 and lr1 >= 5.0 and \
        prof.mlpcl.bminus > -50 and prof.ebottom == 0:
        watch_types.append("PDS TOR")
        colors.append("#FF0000")
    elif (stp_eff >= 3 or stp_fixed >= 4) and prof.mlpcl.bminus > -125. and prof.ebottom == 0:
        watch_types.append("TOR")
        colors.append("#FF0000")
    elif (stp_eff >= 1 or stp_fixed >= 1) and (prof.srw_4_6km >= 15.0 or prof.sfc_8km_shear >= 40) and \
        prof.mlpcl.bminus > -50 and prof.ebottom == 0:
        watch_types.append("TOR")
        colors.append("#FF0000")
    elif (stp_eff >= 1 or stp_fixed >= 1) and ((prof.low_rh + prof.mid_rh)/2. >= 60) and lr1 >= 5.0 and \
        prof.mlpcl.bminus > -50 and prof.ebottom == 0:
        watch_types.append("TOR")
        colors.append("#FF0000")
    elif (stp_eff >= 1 or stp_fixed >= 1) and prof.mlpcl.bminus > -150 and prof.ebottom == 0:
        watch_types.append("mrgl TOR")
        colors.append("#FF0000")
    elif (stp_eff >= 0.5 and prof.right_esrh >= 150) or (stp_fixed >= 0.5 and prof.srh1km >= 150) and \
        prof.mlpcl.bminus > -50 and prof.ebottom == 0:
        watch_types.append("mrgl TOR")
        colors.append("#FF0000")

    #SVR LOGIC
    if (stp_fixed >= 1.0 or prof.right_scp >= 4.0 or stp_eff >= 1.0) and prof.mupcl.bminus >= -50:
        colors.append("#FFFF00")
        watch_types.append("SVR")
    elif prof.right_scp >= 2.0 and (prof.ship >= 1.0 or prof.dcape >= 750) and prof.mupcl.bminus >= -50:
        colors.append("#FFFF00")
        watch_types.append("SVR")
    elif prof.sig_severe >= 30000 and prof.mmp >= 0.6 and prof.mupcl.bminus >= -50:
        colors.append("#FFFF00")
        watch_types.append("SVR")
    elif prof.mupcl.bminus >= -75.0 and (prof.wndg >= 0.5 or prof.ship >= 0.5 or prof.right_scp >= 0.5):
        colors.append("#0099CC")
        watch_types.append("MRGL SVR")
    """END RICH'S CODE"""
    
    # Flash Flood Watch PWV is larger than normal and cloud layer mean wind speeds are slow
    # This is trying to capture the ingredients of moisture and advection speed, but cannot
    # handle precipitation efficiency or vertical motion
    pw_climo_flag = prof.pwv_flag
    pwat = prof.pwat
    upshear = utils.comp2vec(prof.upshear_downshear[0],prof.upshear_downshear[1])
    if pw_climo_flag >= 2 and upshear[1] < 25:
        watch_types.append("FLASH FLOOD")
        colors.append("#5FFB17")
    #elif pwat > 1.3 and upshear[1] < 25:
    #    watch_types.append("FLASH FLOOD")
    #    colors.append("#5FFB17")
    
    # Blizzard Watch if sfc winds > 35 mph and precip type detects snow
    sfc_wspd = utils.KTS2MPH(prof.wspd[prof.get_sfc()])
    if sfc_wspd > 35. and prof.tmpc[prof.get_sfc()] <= 32:
        watch_types.append("BLIZZARD")
        colors.append("#3366FF")
    # Winter Storm Watch if precip type is snow, ice, or sleet
    
    # Wind Chill Watch (if wind chill gets below -20 F)
    if wind_chill(prof) < -20.:
        watch_types.append("WIND CHILL")
        colors.append("#3366FF")
    
    # Fire WX Watch (sfc RH < 30% and sfc_wind speed > 15 mph)
    if sfc_wspd > 15. and thermo.relh(prof.pres[prof.get_sfc()], prof.tmpc[prof.get_sfc()], prof.tmpc[prof.get_sfc()]) < 30. :
        watch_types.append("FIRE WEATHER")
        colors.append("#FF9900")
    
    # Excessive Heat Watch (if Max_temp > 105 F and sfc dewpoint > 75 F)
    if thermo.ctof(prof.dwpc[prof.get_sfc()]) > 75. and thermo.ctof(params.max_temp(prof)) >= 105.:
        watch_types.append("EXCESSIVE HEAT")
        colors.append("#CC33CC")
    
    # Freeze Watch (checks to see if dewpoint is below freezing and temperature isn't and wind speeds are low)
    if thermo.ctof(prof.dwpc[prof.get_sfc()]) < 32. and thermo.ctof(prof.tmpc[prof.get_sfc()]) > 32. and prof.wspd[prof.get_sfc()] < 5.:
        watch_types.append("FREEZE")
        colors.append("#3366FF")
    
    watch_types.append("NONE")
    colors.append("#FFCC33")
    
    return np.asarray(watch_types), np.asarray(colors)

