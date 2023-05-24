#!/bin/bash

loc_all=("soil" "low" "high")
#sce='RCP26'
temp_in_all=("tmax")
month_in_all=("10") # "10")  #("6" "7" "8")
year_in_all=("1986" "1987" "1988" "1989" "1990" "1991" "1992" "1993" "1994" "1995")

for temp_in in ${temp_in_all[@]}; do
    echo "Temp: $temp_in"
    for loc in ${loc_all[@]}; do
        echo "Create ymonmean avg files for: $loc"
        basefolder_in=/storage/sulmonie/CH2018/model_output_predictions/${loc}_past/${temp_in}
        basefolder_out=/home/malle/micromap_nationwide/avg_micromaps/${loc}/${temp_in}
        mkdir -p $basefolder_out
        for year_in in ${year_in_all[@]}; do
            for month_in in ${month_in_all[@]}; do
                cd ${basefolder_in}
                list_files_all=$(ls *temp_${year_in}-${month_in}*.nc)
                out_all=${basefolder_out}/micromap_${loc}_${year_in}_${month_in}.nc
                if [ -f ${out_all} ]
                then
                    echo "File ${out_all} already exists, not running again"
                else
                    cdo --timestat_date last -z zip_5 monmean -mergetime ${list_files_all} ${out_all}
                fi
            done
        done
    done
done