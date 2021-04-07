

import os


if snakemake.params["S"] == "y":

    #If there are short reads, KmerGenie should estimate the genome size and this number will be used as parameter for the assembly creation through Flye.
    os.system("ls "+snakemake.params["ShortR"]+"/trimmomatic_output/*.fastq* > "+snakemake.params["ShortR"]+"/trimmomatic_output/list_files")
    os.system("kmergenie "+snakemake.params["ShortR"]+"/trimmomatic_output/list_files -o "+snakemake.params["ShortR"]+"/trimmomatic_output/KmerGenie/KmerGenie")
    os.system("rm "+snakemake.params["ShortR"]+"/trimmomatic_output/list_files")

    with open(snakemake.params["ShortR"]+"/trimmomatic_output/KmerGenie/KmerGenie_report.html") as f:
        for line in f.readlines():
            if "Predicted assembly size" in line:
                N = [int(s) for s in line.split() if s.isdigit()]

    os.system("flye --nano-raw " + snakemake.input[1] + " -o " + snakemake.input[0]+"/Assemblies/Flye -t "+ str(snakemake.threads)+" -g " + str(N[0]))

else:
    #If there are no short reads, the genome size estimation is a hyperarameter.
    if snakemake.params["GSE"] == " ":
        print("You haven't provided any Genome Size Estimation number during configuration. Please try again.")
    else:
        os.system("flye --nano-raw " + snakemake.input[1] + " -o " + snakemake.input[0]+"/Assemblies/Flye -t "+ str(snakemake.threads)+" -g " + snakemake.params["GSE"])
