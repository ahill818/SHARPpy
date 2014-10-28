from StringIO import StringIO
import sharppy.sharptab.profile as profile
import urllib
import time as gmtime
import datetime
import sys
import numpy as np


## get the current utc time and format it into
## a string that can be used for the SPC url.
if sys.argv[1] != "test":
    gmtime = datetime.datetime.utcnow()
    t_str = str( gmtime )
    year = t_str[2:4]
    month = t_str[5:7]
    day = t_str[8:10]
    hour = t_str[11:13]
    if int( hour ) > 12:
        current_ob = '12'
    else:
        current_ob = '00'
        
    obstring = year + month + day + current_ob
    obstime = datetime.datetime.strptime( obstring, '%y%m%d%H')
    delta1 = datetime.timedelta( hours=12 )
    delta2 = datetime.timedelta( hours=24 )
    obs12 = obstime - delta1
    obs24 = obstime - delta2
        
    t_str = str( obs12 )
    year = t_str[2:4]
    month = t_str[5:7]
    day = t_str[8:10]
    hour = t_str[11:13]
    obstring2 = year + month + day + hour

        
    url = urllib.urlopen('http://www.spc.noaa.gov/exper/soundings/LATEST/' + str( sys.argv[1] ).upper() + '.txt')
    data = np.array(url.read().split('\n'))
    title_idx = np.where( data == '%TITLE%')[0][0]
    start_idx = np.where( data == '%RAW%' )[0] + 1
    finish_idx = np.where( data == '%END%')[0]
    plot_title = data[title_idx + 1] + ' (Observed)'
    full_data = '\n'.join(data[start_idx : finish_idx][:])
    sound_data = StringIO( full_data )
    p, h, T, Td, wdir, wspd = np.genfromtxt( sound_data, delimiter=',', comments="%", unpack=True )
    prof = profile.create_profile( profile='convective', pres=p, hght=h, tmpc=T, dwpc=Td,
                                wdir=wdir, wspd=wspd, location=sys.argv[1])


else:
	sound = '''
        1000.00,     34.00,  -9999.00,  -9999.00,  -9999.00,  -9999.00
        965.00,    350.00,     27.80,     23.80,    150.00,     23.00
        962.00,    377.51,     27.40,     22.80,  -9999.00,  -9999.00
        936.87,    610.00,     25.51,     21.72,    145.00,     29.99
        925.00,    722.00,     24.60,     21.20,    150.00,     33.99
        904.95,    914.00,     23.05,     20.43,    160.00,     42.00
        889.00,   1069.78,     21.80,     19.80,  -9999.00,  -9999.00
        877.00,   1188.26,     22.20,     17.30,  -9999.00,  -9999.00
        873.90,   1219.00,     22.02,     16.98,    175.00,     50.00
        853.00,   1429.46,     20.80,     14.80,  -9999.00,  -9999.00
        850.00,   1460.00,     21.00,     14.00,    180.00,     50.00
        844.00,   1521.47,     21.40,     11.40,  -9999.00,  -9999.00
        814.51,   1829.00,     19.63,      8.65,    195.00,     47.01
        814.00,   1834.46,     19.60,      8.60,  -9999.00,  -9999.00
        805.00,   1930.24,     18.80,     13.80,  -9999.00,  -9999.00
        794.00,   2048.59,     18.00,     13.50,  -9999.00,  -9999.00
        786.13,   2134.00,     17.57,     12.72,    200.00,     46.00
        783.00,   2168.27,     17.40,     12.40,  -9999.00,  -9999.00
        761.00,   2411.82,     16.40,      7.40,  -9999.00,  -9999.00
        758.66,   2438.00,     16.49,      5.16,    210.00,     50.00
        756.00,   2467.98,     16.60,      2.60,  -9999.00,  -9999.00
        743.00,   2615.49,     16.00,     -1.00,  -9999.00,  -9999.00
        737.00,   2684.28,     15.40,     -0.60,  -9999.00,  -9999.00
        731.90,   2743.00,     14.64,      2.45,    210.00,     50.00
        729.00,   2776.65,     14.20,      4.20,  -9999.00,  -9999.00
        710.00,   2999.06,     12.20,      4.20,  -9999.00,  -9999.00
        705.87,   3048.00,     11.99,      3.99,    210.00,     54.99
        702.00,   3094.10,     11.80,      3.80,  -9999.00,  -9999.00
        700.00,   3118.00,     11.60,      2.60,    215.00,     50.99
        697.00,   3153.92,     11.60,      0.60,  -9999.00,  -9999.00
        682.00,   3335.50,     10.40,      2.40,  -9999.00,  -9999.00
        675.00,   3421.38,     10.00,      1.00,  -9999.00,  -9999.00
        655.96,   3658.00,      7.97,     -2.38,    225.00,     48.00
        647.00,   3771.67,      7.00,     -4.00,  -9999.00,  -9999.00
        635.00,   3925.19,      6.00,    -12.00,  -9999.00,  -9999.00
        632.14,   3962.00,      5.72,    -12.99,    230.00,     43.01
        623.00,   4080.90,      4.80,    -16.20,  -9999.00,  -9999.00
        608.51,   4267.00,      3.10,    -17.37,    230.00,     44.00
        563.33,   4877.00,     -2.48,    -21.19,    230.00,     46.00
        500.00,   5820.00,    -11.10,    -27.10,    245.00,     52.00
        496.00,   5881.65,    -11.50,    -26.50,  -9999.00,  -9999.00
        482.28,   6096.00,    -13.14,    -28.14,    245.00,     48.00
        481.00,   6116.34,    -13.30,    -28.30,  -9999.00,  -9999.00
        472.00,   6259.91,    -14.30,    -33.30,  -9999.00,  -9999.00
        464.00,   6389.52,    -14.50,    -39.50,  -9999.00,  -9999.00
        460.00,   6455.17,    -14.30,    -30.30,  -9999.00,  -9999.00
        457.00,   6504.79,    -14.50,    -29.50,  -9999.00,  -9999.00
        443.00,   6739.75,    -16.50,    -27.50,  -9999.00,  -9999.00
        431.00,   6945.77,    -17.90,    -28.90,  -9999.00,  -9999.00
        423.00,   7085.70,    -18.70,    -37.70,  -9999.00,  -9999.00
        410.00,   7317.63,    -20.50,    -33.50,  -9999.00,  -9999.00
        400.00,   7500.00,    -21.70,    -41.70,    250.00,     52.00
        396.00,   7573.79,    -22.10,    -45.10,  -9999.00,  -9999.00
        393.50,   7620.00,    -22.52,    -44.19,    250.00,     52.99
        383.00,   7817.58,    -24.30,    -40.30,  -9999.00,  -9999.00
        365.00,   8165.50,    -27.30,    -52.30,  -9999.00,  -9999.00
        353.00,   8404.47,    -29.70,    -41.70,  -9999.00,  -9999.00
        346.00,   8546.60,    -30.90,    -41.90,  -9999.00,  -9999.00
        327.00,   8943.91,    -33.90,    -52.90,  -9999.00,  -9999.00
        317.73,   9144.00,    -35.59,    -53.82,    255.00,     47.01
        315.00,   9204.06,    -36.10,    -54.10,  -9999.00,  -9999.00
        300.00,   9540.00,    -38.90,    -49.90,    250.00,     48.00
        290.00,   9772.78,    -40.90,    -50.90,  -9999.00,  -9999.00
        278.01,  10058.00,    -43.14,    -54.39,    255.00,     50.99
        262.00,  10458.87,    -46.30,    -59.30,  -9999.00,  -9999.00
        250.00,  10770.00,    -49.10,    -62.10,    260.00,     48.00
        238.00,  11090.28,    -51.90,    -63.90,  -9999.00,  -9999.00
        231.10,  11278.00,    -52.95,    -65.12,    260.00,     31.00
        210.06,  11887.00,    -56.35,    -69.07,    265.00,     46.00
        200.00,  12200.00,    -58.10,    -71.10,    265.00,     42.00
        190.76,  12497.00,    -59.78,    -73.55,    280.00,     42.00
        188.00,  12588.32,    -60.30,    -74.30,  -9999.00,  -9999.00
        175.00,  13035.70,    -60.30,    -74.30,  -9999.00,  -9999.00
        173.03,  13106.00,    -60.66,    -74.88,    265.00,     50.99
        164.72,  13411.00,    -62.20,    -77.38,    255.00,     39.01
        158.00,  13668.93,    -63.50,    -79.50,    245.00,     43.01
        157.00,  13707.98,    -63.50,    -79.50,  -9999.00,  -9999.00
        154.00,  13827.08,    -61.90,    -77.90,  -9999.00,  -9999.00
        150.00,  13990.00,    -62.30,    -77.30,    250.00,     49.01
        149.25,  14021.00,    -62.25,    -77.25,    250.00,     52.99
        147.00,  14114.55,    -62.10,    -77.10,  -9999.00,  -9999.00
        142.11,  14326.00,    -56.43,    -73.39,    270.00,     36.00
        142.00,  14330.93,    -56.30,    -73.30,  -9999.00,  -9999.00
        141.00,  14375.74,    -56.10,    -74.10,  -9999.00,  -9999.00
        137.00,  14557.96,    -56.90,    -73.90,  -9999.00,  -9999.00
        132.00,  14791.84,    -58.90,    -75.90,  -9999.00,  -9999.00
        129.02,  14935.00,    -58.40,    -77.07,    260.00,     29.00
        125.00,  15133.97,    -57.70,    -78.70,  -9999.00,  -9999.00
        122.90,  15240.00,    -58.70,    -79.70,    225.00,     18.01
        118.00,  15493.97,    -61.10,    -82.10,  -9999.00,  -9999.00
        117.03,  15545.00,    -61.23,    -81.59,    215.00,     14.01
        115.00,  15653.42,    -61.50,    -80.50,  -9999.00,  -9999.00
        110.00,  15928.24,    -61.70,    -80.70,  -9999.00,  -9999.00
        109.00,  15984.92,    -59.90,    -78.90,  -9999.00,  -9999.00
        108.00,  16042.38,    -59.70,    -79.70,  -9999.00,  -9999.00
        100.00,  16520.00,    -61.90,    -81.90,    240.00,     31.99
        92.80,  16982.30,    -62.70,    -84.70,  -9999.00,  -9999.00
        87.20,  17369.21,    -59.90,    -83.90,  -9999.00,  -9999.00
        87.13,  17374.00,    -59.92,    -83.92,    175.00,      4.99
        83.20,  17662.07,    -61.30,    -85.30,  -9999.00,  -9999.00
        82.99,  17678.00,    -61.03,    -85.21,    220.00,     16.01
        80.90,  17837.57,    -58.30,    -84.30,  -9999.00,  -9999.00
        75.32,  18288.00,    -58.43,    -85.08,    240.00,      6.99
        72.50,  18528.36,    -58.50,    -85.50,  -9999.00,  -9999.00
        71.76,  18593.00,    -58.15,    -85.73,    220.00,     10.00
        70.00,  18750.00,    -57.30,    -86.30,    205.00,      6.99
        66.20,  19102.50,    -56.50,    -86.50,  -9999.00,  -9999.00
        62.08,  19507.00,    -57.97,    -88.58,      0.00,      2.00
        59.60,  19763.34,    -58.90,    -89.90,  -9999.00,  -9999.00
        51.16,  20726.00,    -56.29,    -88.16,    140.00,     13.00
        50.00,  20870.00,    -55.90,    -87.90,    100.00,     12.00
        47.30,  21223.20,    -55.30,    -87.30,  -9999.00,  -9999.00
        46.47,  21336.00,    -55.71,    -87.71,    130.00,     14.01
        45.30,  21497.82,    -56.30,    -88.30,  -9999.00,  -9999.00
        44.29,  21641.00,    -56.10,    -88.21,    130.00,     12.00
        42.22,  21946.00,    -55.67,    -88.02,    140.00,     15.00
        40.25,  22250.00,    -55.24,    -87.83,    115.00,     14.01
        38.37,  22555.00,    -54.80,    -87.63,    100.00,     18.01
        37.10,  22769.50,    -54.50,    -87.50,  -9999.00,  -9999.00
        34.90,  23165.00,    -52.26,    -85.69,    115.00,     25.00
        33.29,  23470.00,    -50.53,    -84.29,    105.00,     24.01
        32.20,  23686.07,    -49.30,    -83.30,  -9999.00,  -9999.00
        30.00,  24150.00,    -48.70,    -82.70,    125.00,     17.00
        29.30,  24305.84,    -48.10,    -82.10,  -9999.00,  -9999.00
        28.95,  24384.00,    -48.34,    -82.34,    135.00,     13.00
        27.90,  24628.73,    -49.10,    -83.10,  -9999.00,  -9999.00
        26.70,  24918.79,    -47.90,    -82.90,  -9999.00,  -9999.00
        26.40,  24994.00,    -47.91,    -82.86,     80.00,     19.00
        21.95,  26213.00,    -48.06,    -82.26,    105.00,     25.00
        20.90,  26538.29,    -48.10,    -82.10,  -9999.00,  -9999.00
        20.02,  26822.00,    -46.93,    -81.91,    115.00,     24.01
        20.00,  26830.00,    -46.90,    -81.90,    115.00,     24.01
        19.20,  27100.93,    -45.70,    -80.70,  -9999.00,  -9999.00
        19.12,  27127.00,    -45.73,    -80.73,    100.00,     19.00
        18.27,  27432.00,    -46.02,    -81.02,    105.00,     19.00
        17.50,  27717.04,    -46.30,    -81.30,  -9999.00,  -9999.00
        17.45,  27737.00,    -46.23,    -81.24,    115.00,     20.01
        16.67,  28042.00,    -45.08,    -80.37,     95.00,     19.00
        14.80,  28839.52,    -42.10,    -78.10,  -9999.00,  -9999.00
        13.91,  29261.00,    -41.98,    -77.98,    105.00,     20.01
        12.71,  29870.00,    -41.80,    -77.80,    100.00,     17.00
        12.10,  30202.29,    -41.70,    -77.70,  -9999.00,  -9999.00
        11.62,  30480.00,    -39.91,    -76.69,     80.00,     20.01
        11.11,  30785.00,    -37.95,    -75.58,     70.00,     19.00
        10.90,  30916.58,    -37.10,    -75.10,  -9999.00,  -9999.00
        10.00,  31510.00,    -38.50,    -75.50,     80.00,     27.00
        9.00,  32234.97,    -37.70,    -75.70,  -9999.00,  -9999.00
        8.40,  32713.14,    -35.10,    -73.10,  -9999.00,  -9999.00
        8.10,  32968.30,    -31.90,    -71.90,  -9999.00,  -9999.00
        7.81,  33223.00,    -31.90,    -71.90,     90.00,     39.01
        7.80,  33234.86,    -31.90,    -71.90,  -9999.00,  -9999.00
'''
	sound_data = StringIO( sound )
	p2, h2, T2, Td2, wdir2, wspd2 = np.genfromtxt( sound_data, delimiter=',', comments="%", unpack=True )
	test = profile.create_profile(profile='convective',  pres=p2, hght=h2, tmpc=T2, dwpc=Td2, wdir=wdir2,
                                  wspd=wspd2, location='OAX' )
