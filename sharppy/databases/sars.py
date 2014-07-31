import numpy as np
import os

## original database and code provided by
## Ryan Jewell - NOAA Storm Prediction Center (hail)
## Rich Thompson - NOAA Storm Prediction Center (supercell)

## Routines implemented in Python by Greg Blumberg - CIMMS and Kelton Halbert (OU SoM)
## wblumberg@ou.edu, greg.blumberg@noaa.gov, kelton.halbert@noaa.gov

def sars_supercell(database_fn, mlcape, mllcl, h5temp, lr, shr, srh, shr3k, shr9k, srh3):
    # SARS for Supercells
    database_fn = os.path.join( os.path.dirname( __file__ ), database_fn)
    print database_fn, mlcape, mllcl, h5temp, lr, shr, srh, shr3k, shr9k, srh3
    print "MLCAPE:", mlcape
    print "MLLCL:", mllcl
    print "h5temp:", h5temp
    print "LR:", lr
    print "SHR06:", shr
    print "SRH01:", srh
    print "SHR03:", shr3k
    print "SHR09:", shr9k
    print "SRH03:", srh3

    supercell_database = np.loadtxt(database_fn, skiprows=1, dtype=str, comments="%%%%")

    # Set range citeria for matching soundings

    # MLCAPE ranges
    range_mlcape = 1300 # J/kg
    range_mlcape_t1 = mlcape * 0.25 # J/kg

    # MLLCL ranges
    range_mllcl = 50 # m
    range_mllcl_t1 = 200 # m

    # 0-6 km shear ranges (kts)
    range_shr = 14
    range_shr_t1 = 10

    # 0-1 km SRH Ranges (m2/s2)
    if np.abs(srh) < 50:
        range_srh = 100.
    else:
        range_srh = srh
    
    if np.abs(srh) < 100:
        range_srh_t1 = 50
    else:
        range_srh_t1 = np.abs(shr) * 0.30
    
    # 0-3 SRH tier 1 ranges (m2/s2)
    if np.abs(srh3) < 100:
        range_srh3_t1 = 50.
    else:
        range_srh3_t1 = np.abs(srh3) * 0.50

    # 500 mb temperature ranges
    range_temp = 7 # C
    range_temp_t1 = 5 # C

    # 700-500 mb lapse rate ranges (C/km)
    range_lr = 1.0
    range_lr_t1 = 0.8

    # 3 km and 9 km shear matching
    range_shr3k_t1 = 15
    range_shr9k_t1 = 25

    mat_category = np.asarray(supercell_database[:,1], dtype=float) # category of match (0=non, 1=weak, 2=sig)
    mat_mlcape = np.asarray(supercell_database[:,3], dtype=float)
    mat_mllcl = np.asarray(supercell_database[:,5], dtype=float)
    mat_shr = np.asarray(supercell_database[:,7], dtype=float) # 0-6 KM SHEAR
    mat_srh = np.asarray(supercell_database[:,6], dtype=float) # 0-1 KM SRH
    mat_srh3 = np.asarray(supercell_database[:,14], dtype=float) # 0-3 KM SRH
    mat_h5temp = np.asarray(supercell_database[:,9], dtype=float) # 500 MB TEMP C
    mat_lr75 = np.asarray(supercell_database[:,11], dtype=float) # 700-500 MB LAPSE RATE
    mat_shr3 = np.asarray(supercell_database[:,12], dtype=float) # 0-3 KM SHEAR
    mat_shr9 = np.asarray(supercell_database[:,13], dtype=float) # 0-9 KM SHEAR
    
    debug = np.where((mllcl >= (mat_mllcl - range_mllcl)) & (mllcl <= (mat_mllcl + range_mllcl)))
    #debug = np.where((mlcape >= (mat_mlcape - range_mlcape)) & (mlcape <= (mat_mlcape + range_mlcape)))
    #print mat_mllcl - range_mllcl, mat_mllcl + range_mllcl
    #print mat_mllcl[debug] 
    print supercell_database[:,0][debug]
    
    loose_match_idx = np.where((mlcape >= (mat_mlcape - range_mlcape)) & (mlcape <= (mat_mlcape + range_mlcape)) & \
                               (mllcl >= (mat_mllcl - range_mllcl)) & (mllcl <= (mat_mllcl + range_mllcl)) & \
                               (shr >= (mat_shr - range_shr)) & (shr <= (mat_shr + range_shr)) & \
                               (srh >= (mat_srh - range_srh)) & (srh <= (mat_srh + range_srh)) & \
                               (h5temp >= (mat_h5temp - range_temp)) & (h5temp <= (mat_h5temp + range_temp)) & \
                               (lr >= (mat_lr75 - range_lr)) & (lr <= (mat_lr75 + range_lr)))[0]
    loose_match_soundings = supercell_database[:,0][loose_match_idx]
    print loose_match_soundings
    
    num_matches = len(np.where(mat_category[loose_match_idx] > 0)[0]) #number of weak and sig matches in the loose matches
    
     
    # Probability for tornado
    tor_prob = num_matches / float(len(loose_match_idx))
    
    # Tier 1 matches (also known as the quality matches)
    quality_match_idx = np.where((mlcape >= (mat_mlcape - range_mlcape_t1)) & (mlcape <= (mat_mlcape + range_mlcape_t1)) & \
                               (mllcl >= (mat_mllcl - range_mllcl_t1)) & (mllcl <= (mat_mllcl + range_mllcl_t1)) & \
                               (shr >= (mat_shr - range_shr_t1)) & (shr <= (mat_shr + range_shr_t1)) & \
                               (srh >= (mat_srh - range_srh_t1)) & (srh <= (mat_srh + range_srh_t1)) & \
                               (h5temp >= (mat_h5temp - range_temp_t1)) & (h5temp <= (mat_h5temp + range_temp_t1)) & \
                               (lr >= (mat_lr75 - range_lr_t1)) & (lr <= (mat_lr75 + range_lr_t1)) & \
                               (shr3k >= (mat_shr3 - range_shr3k_t1)) & (shr3k <= (mat_shr3 + range_shr3k_t1)) & \
                               (shr9k >= (mat_shr9 - range_shr9k_t1)) & (shr9k <= (mat_shr9 + range_shr9k_t1)) & \
                               (srh3 >= (mat_srh3 - range_srh3_t1)) & (srh3 <= (mat_srh3 + range_srh3_t1)))[0]

    quality_match_soundings = supercell_database[:,0][quality_match_idx]
    quality_match_tortype = np.asarray(supercell_database[:,1][quality_match_idx], dtype='|S7')
    
    np.place(quality_match_tortype, quality_match_tortype=='2', 'SIGTOR')
    np.place(quality_match_tortype, quality_match_tortype=='1', 'WEAKTOR')
    np.place(quality_match_tortype, quality_match_tortype=='0', 'NONTOR')
    
    return tor_prob, len(loose_match_idx), quality_match_soundings, quality_match_tortype


def sars_hail(database_fn, mumr, mucape, h5_temp, lr, shr6, shr9, shr3, srh):
    '''
        INPUT:
        mumr - most unstable parcel mixing ratio (g/kg)
        mucape - most unstable CAPE (J/kg)
        h5_temp - 500 mb temperature (C)
        lr - 700-500 mb lapse rate (C/km)
        shr6 - 0-6 km shear (m/s)
        shr9 - 0-9 km shear (m/s)
        shr3 - 0-3 km shear (m/s)
        srh - 0-3 Storm Relative Helicity (m2/s2)
    
        OUTPUT:
        quality_matches_dates - dates of the quality matches
        quality_matches_sizes - hail sizes of the quality matches
        num_loose_matches - number of loose matches
        num_sig_reports - number of significant hail reports (>= 2 inches)
        prob_sig_hail - SARS sig. hail probability
    '''
    # SARS for HAIL
    database_fn = os.path.join( os.path.dirname( __file__ ), database_fn )

    hail_database = np.loadtxt(database_fn, skiprows=1, dtype=str)
    
    #Set range criteria for matching soundings
    
    # MU Mixing Ratio Ranges
    range_mumr = 2.0 # g/kg
    range_mumr_t1 = 2.0 # g/kg

    # MUCAPE Ranges (J/kg)
    range_mucape = mucape*.30
    if mucape < 500.:
        range_mucape_t1 = mucape * .50
    elif mucape >= 500. and mucape < 2000.:
        range_mucape_t1 = mucape * .25
    else:
        range_mucape_t1 = mucape * .20

    # 700-500 mb Lapse Rate Ranges
    range_lr = 2.0 # C/km
    range_lr_t1 = 0.4 # C/km

    # 500 mb temperature ranges 
    range_temp = 9 # C
    range_temp_t1 = 1.5 # C

    # 0-6 km shear ranges
    range_shr6 = 12 # m/s
    range_shr6_t1 = 6 # m/s

    # 0-9 km shear ranges
    range_shr9 = 22 # m/s
    range_shr9_t1 = 15 # m/s

    # 0-3 km shear ranges
    range_shr3 = 10
    range_shr3_t1 = 8

    # 0-3 SRH Ranges
    range_srh = 100
    if srh < 50:
        range_srh_t1 = 25
    else:
        range_srh_t1 = srh * 0.5

    #Get database variables and make them floats
    matmr = np.asarray(hail_database[:,4], dtype=float) # MU Mixing Ratio
    matcape = np.asarray(hail_database[:,3], dtype=float) # MUCAPE
    matlr = np.asarray(hail_database[:,7], dtype=float) # 700-500 mb lapse rate
    mattemp = np.asarray(hail_database[:,5], dtype=float) # 500 mb temp
    matshr6 = np.asarray(hail_database[:,10], dtype=float) # 0-6 shear
    matshr9 = np.asarray(hail_database[:,11], dtype=float) # 0-9 shear
    matshr3 = np.asarray(hail_database[:,9], dtype=float) # 0-3 shear
    matsrh = np.asarray(hail_database[:,12], dtype=float) # 0-3 SRH

    # Find the loose matches
    loose_match_idx = np.where((mumr >= (matmr - range_mumr)) & (mumr <= (matmr + range_mumr)) & \
                               (mucape >= (matcape - range_mucape)) & (mucape <= (matcape + range_mucape)) & \
                               (lr >= (matlr - range_lr)) & (lr <= (matlr + range_lr)) & \
                               (h5_temp >= (mattemp - range_temp)) & (h5_temp <= (mattemp + range_temp)) & \
                               (shr6 >= (matshr6 - range_shr6)) & (shr6 <= (matshr6 + range_shr6)) & \
                               (shr9 >= (matshr9 - range_shr9)) & (shr9 <= (matshr9 + range_shr9)) & \
                               (shr3 >= (matshr3 - range_shr3)) & (shr3 <= (matshr3 + range_shr3)))[0]
    num_loose_matches = float(len(loose_match_idx))
    hail_sizes = np.asarray(hail_database[:,2], dtype=float)
    num_sig_reports = float(len(np.where(hail_sizes[loose_match_idx] >= 2.)[0]))
    # Calculate the Probability of significant hail
    if num_loose_matches > 0:
        prob_sig_hail = num_sig_reports / num_loose_matches
        # Calculate the average hail size from the loose matches
        avg_hail_size = np.mean(hail_sizes[loose_match_idx])
    else:
        prob_sig_hail = 0


    # Find the quality matches    
    quality_match_idx = np.where((mumr >= (matmr - range_mumr_t1)) & (mumr <= (matmr + range_mumr_t1)) & \
                               (mucape >= (matcape - range_mucape_t1)) & (mucape <= (matcape + range_mucape_t1)) & \
                               (lr >= (matlr - range_lr_t1)) & (lr <= (matlr + range_lr_t1)) & \
                               (h5_temp >= (mattemp - range_temp_t1)) & (h5_temp <= (mattemp + range_temp_t1)) & \
                               (shr6 >= (matshr6 - range_shr6_t1)) & (shr6 <= (matshr6 + range_shr6_t1)) & \
                               (shr9 >= (matshr9 - range_shr9_t1)) & (shr9 <= (matshr9 + range_shr9_t1)) & \
                               (shr3 >= (matshr3 - range_shr3_t1)) & (shr3 <= (matshr3 + range_shr3_t1)) & \
                               (srh >= (matsrh - range_srh_t1)) & (srh <= (matsrh + range_srh_t1)))[0]
    quality_match_dates = hail_database[quality_match_idx,0]
    quality_match_sizes = np.asarray(hail_database[quality_match_idx,2], dtype=float)

    # This filtering was in the sars.f file so the graphical output wasn't overrun by historical quality matches
    max_quality_matches = 15
    quality_match_dates = quality_match_dates[:max_quality_matches]
    quality_match_sizes = quality_match_sizes[:max_quality_matches]
    return quality_match_dates, quality_match_sizes, num_loose_matches, num_sig_reports, prob_sig_hail

