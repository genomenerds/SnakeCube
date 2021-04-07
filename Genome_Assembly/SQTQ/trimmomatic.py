
import os


#We give a list of files to be trimmed by passing them through the trimming function.
#The function takes the input and searches for complementary R1 and R2 files (paired-end Illumina).
#In the end, we delete everything but the trimmed fastq files. The parameteres and paths are essential.




def trimming(datadir, program, processed, log):

    ''' This function takes raw data and performs trimming.
        datadir must be the directory that contains the data.
        The output files are saved in a subfolder called "trimmomatic_output".'''

    for fileR1 in os.listdir(datadir):
        if ("R1" in fileR1):
            dividing = fileR1.split(".")
            fileR2 = fileR1.replace('R1', 'R2')
            if os.path.isfile(datadir + "/"+fileR2):
                dividing1 = fileR2.split(".")
                log1 = dividing[0]
                output1 = dividing[0]
                output2 = dividing1[0]
                os.system("java -jar " + program + " PE -threads "+str(snakemake.threads)+" -phred33 " + datadir + "/"+ fileR1 + " " + datadir + "/"+ fileR2 + " " + processed + "/"+ output1 + "_trimmed.fastq.gz " + processed + "/"+ output1 +"_output_forward_unpaired.fq.gz " + processed + "/"+ output2 + "_trimmed.fastq.gz " + processed + "/"+ output2 +"_output_reverse_unpaired.fq.gz " + " LEADING:"+ snakemake.params["leading"] + " TRAILING:"+ snakemake.params["trailing"] + " SLIDINGWINDOW:" + snakemake.params["sliding"]+ " MINLEN:" +snakemake.params["minlen"] + " AVGQUAL:" + snakemake.params["avg"] + " >" + log + log1 + "_trimmomatic.txt" + " 2>&1")
    return



os.system("mkdir " + snakemake.input[0]+"/logfile")
os.system("mkdir " + snakemake.output[0])
trimming(snakemake.input[0], "/opt/conda/envs/SQTQ/share/trimmomatic-0.39-1/trimmomatic.jar", snakemake.output[0], snakemake.input[0]+"/logfile/")


for f in os.listdir(snakemake.output[0]):
    if ("output") in f:
        f.strip("'")
        os.system("rm " + snakemake.output[0]+ "/"+f)

os.system("rm -r " + snakemake.input[0]+"/logfile")
