

import os
import os.path
from os import path


### BUSCO has many problems with its configuration files and paths, so everything it needs to run is manually tuned and imported into the image. Precisely:
# run_BUSCO.py is the basic BUSCO file, and it contains the path to the config file
# The config file is BUSCOconfig.ini and its copied into the image too. It contains the paths to all the programms for BUSCO etc. Notice that the paths may belong to specific environments.
# Lastly, there is a whole conifg dir that is needed by the programs. Its is copied into the image, once the image is run it is copied in the dir of the user for the programs to work, and it is deleted when the pipeline is done.
# The Singularity Definition file has also augustus-related paths exported to the $PATH of the conda super-environment for augustus to work. 


#Run Quast
os.system("quast -o "+ snakemake.output[0]+ " "+ snakemake.input[0]+" -t "+str(snakemake.threads))



#Run Busco
if path.exists(snakemake.output[0][:-18]+"Assemblies/"+snakemake.params["Lineage"]):  #If the Lineage already exists do not download it again (for later quality controls)
    os.system("python3.6 /run_BUSCO.py -i " + snakemake.input[0] + " -o BUSCO"+str(snakemake.output[1][-1:])+" -m geno -l " + snakemake.output[0][:-18]+"Assemblies/"+ snakemake.params["Lineage"] + " -c "+str(snakemake.threads)+" -sp "+snakemake.params["SP"])

else:
    if "odb9" in snakemake.params["Lineage"]:   #If it does not exist yet, download it, untar it and run BUSCO
        l = "https://busco-archive.ezlab.org/v3/datasets/"+ snakemake.params["Lineage"]+".tar.gz "
        os.system("wget -P " +snakemake.input[0][:-19] +" "+l)
    elif "odb10" in snakemake.params["Lineage"]:
        l = "https://busco-archive.ezlab.org/v3/datasets/prerelease/"+ snakemake.params["Lineage"]+".tar.gz "
        os.system("wget -P " +snakemake.input[0][:-19] +" "+l)
    else:
        print("You have not given a valid lineage base name.")
    os.system("tar -xf "+snakemake.input[0][:-19]+snakemake.params["Lineage"]+".tar.gz -C " +snakemake.input[0][:-19])
    os.system("python3.6 /run_BUSCO.py -i "+snakemake.input[0]+ " -o BUSCO"+str(snakemake.output[1][-1:])+" -m geno -l " +snakemake.input[0][:-19]+snakemake.params["Lineage"]+ " -c "+str(snakemake.threads)+" -sp "+snakemake.params["SP"])

os.system("mv run_BUSCO"+str(snakemake.output[1][-1:])+" "+snakemake.output[1])
