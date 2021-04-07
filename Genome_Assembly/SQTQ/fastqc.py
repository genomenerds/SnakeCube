
import subprocess
import os

def quals(datadir, qr):

    ''' This function takes raw data and performs quality control.
        datadir must be the directory that contains the data
        The html files of the samples are also saved in a subfolder called "quals" for an upcoming multiqc run.'''

    os.chdir(datadir)
    os.system("mkdir " + qr)
    fqf = subprocess.run(["ls","-R"], stdout=subprocess.PIPE, check = True).stdout
    lof = [x.strip() for x in str(fqf).split('\\n')]
    for f in lof:
        if ("fastq") in f:
            subprocess.run(["fastqc", f, "-o", "./"+qr], stdout=subprocess.DEVNULL, check=True)
    return

quals(snakemake.input[0], snakemake.params["qr"])

