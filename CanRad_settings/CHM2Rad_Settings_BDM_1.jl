function CHM2Rad_Settings(basefolder,site="empty")

    par_in = Dict(
    "trunks" => false,

    "terrain_peri" => 10000,

    # terrain settings
    "terrain_highres" => true, # include high high resolution local terrain (1-5 m)
    "terrain_lowres" => false, # include low resolution regional terrain (> 25 m)
    "terrain_tile" => false, # calculate terrain_lowres once for the whole tile
    "horizon_line" => true, # use pre-calculated horizon line matrix
    # if true - make sure "hlmf" is specified below, terrain_lowres = false and terrain_tile = true
    # note this option is required for compatability with OSHD models

    "tilt" => false,

    "image_height" => 0.5, # enter float value

    "calc_trans" => true,
    "calc_swr" => 1, # 0 = off; 1 = potential swr (atm_trans = 1); 2 = real swr (needs swrf in dat_in)

    "season" => "summer",

    "t1"  => "01.10.2019 00:00:00", #"dd.mm.yyyy HH:MM:SS"
    "t2"  => "30.09.2020 23:50:00",
    "tstep" => 60,

    "time_zone" => 1,
    "coor_system" => "CH1903+",

    "save_images" => true,

    "surf_peri" => 100,

    "pt_corr" => true, # enable pt correction (if false, canopy is 100% opaque)

    "tolerance" => 1,

    "batch" => true,

    "progress" => true
    )

    dat_in = Dict(
    # chm
    "chmf" => "/home/malle/CanRad/Domains/BDM_1/input_data/chm_random_0.5_fm1_buffer0m.tif",
    # dtm
    "dtmf" => "/home/malle/CanRad/Datasets/swissALTI3D_5M_CHLV95_LN02_2020.tif",
    # dem
     "demf" => "/home/malle/CanRad/Datasets/dhm25_EPSG2056.tif",
    # mixed ratio data
    "mrdf" => "/home/malle/CanRad/Datasets/WMG2020_RF_Geobasisdatensatz_nomask_LV95.tif",
    # forest class data
    "fcdf" => "/home/malle/CanRad/Datasets/ForestClass.tif",
    # horizon line file
    "hlmf" => "/home/malle/CanRad/Datasets/BAFU_HLM_2020_250.nc",
    # buildings
    "bhmf" => "/home/malle/CanRad/Datasets/BHM_TLM2020.tif"
    )

    return dat_in, par_in

end
