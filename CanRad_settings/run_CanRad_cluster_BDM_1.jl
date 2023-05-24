
site = "BDM_1"

basefolder = "/home/malle/CanRad/Domains/"*site

using CanRad, DelimitedFiles

# which tile?
dx = parse(Int,ARGS[1])

# input coordinates
inputs = readdlm(joinpath(basefolder,"Input.txt"))[dx]

# create points for tile here based on ll corner
tilesize = readdlm(basefolder*"/TileSize.txt")[1]

xllcorner = parse(Int,(split(inputs,"_")[1]))[1]
yllcorner = parse(Int,(split(inputs,"_")[2]))[1]
limits    = hcat(xllcorner, xllcorner+tilesize, yllcorner, yllcorner+tilesize)

# what resolution? [m]
sp = 10
# summer or winter? => to do: grap output from Settings file
season =  "summer"
run_purp = "050_fm1_0mbuffer"

ncols = Int(round(((limits[2] - limits[1]) / sp); digits=0))
nrows = Int(round(((limits[4] - limits[3]) / sp); digits=0))

ptsx = vec(((limits[1]:sp:limits[2]-sp)'  .* ones(nrows)) .+ sp/2)
ptsy = vec((ones(ncols)' .* (limits[3]:sp:limits[4]-sp)) .+ sp/2)
pts = hcat(ptsx,ptsy)

# define output directory
exdir = basefolder*"/CanRad_output/Output_CR_"*string(sp)*"m_"*season*"_"*run_purp

taskID = string(dx)*"_"*string(inputs)

# set 3rd input to false if not not running as batch
if !check_output(exdir,ptsx,true,taskID)

    include(basefolder*"/CHM2Rad_Settings_"*site*".jl")
    dat_in, par_in = CHM2Rad_Settings(basefolder)
    dat_in, par_in = CHM2Rad(pts,dat_in,par_in,exdir,taskID)
    write_metadata(exdir,dat_in,par_in)

    # write model run metadata
 #  if parse(Int,split(split(ARGS[1],"/")[end],".")[2]) .== 1
  #     write_metadata(exdir,dat_in,par_in)
  # end

else

    println("already done with: "*inputs[1])

end

