
import subprocess
import os


def unite_quals(trimmed):

    ''' Performs multiqc on all html generated files from fastqc.
    After the multiqc report is generated, the extra html files are removed.
    The final reports (html and dir info of seqs) are saved in the dir of the raw samples.'''

    if trimmed:
        subprocess.run(["multiqc", snakemake.input[0], "-o", snakemake.output[0]], stdout=subprocess.DEVNULL, check=True)
        os.system("rm -R " + snakemake.input[0])
    else:
        subprocess.run(["multiqc", snakemake.input[0], "-o", snakemake.output[0]], stdout=subprocess.DEVNULL, check=True)
        os.system("rm -R " + snakemake.input[0])
    return

unite_quals(snakemake.params["trimmed"])
