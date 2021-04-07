
import os


def trimming(datadir):

    ''' This function takes raw data and performs trimming.
        datadir must be the directory that contains the data.
        The output file is saved in a file (since the input for a genome assembly is a single file too) with the prefix "porechop_output".'''

    for f in os.listdir(datadir):
        if ("fastq" in f):
            os.system("porechop -i " + datadir +"/"+f +  " -o " + datadir+"/porechop_output.fastq -v 0  --discard_middle -t "+str(snakemake.threads))
            os.system("gzip "+ datadir+"/porechop_output.fastq" )

    return


trimming(snakemake.input[0])
