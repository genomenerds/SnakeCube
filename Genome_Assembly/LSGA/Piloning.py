
import os


#Pilon polishes the assembly with short reads. Minimap2 maps the reads, samtools makes the sam to bam conversion and indexes, and then the paths to the jar files are given for Pilon to run.
#The polishing rounds are decided as follows:
#After each Pilon round, a quality control of the assembly is made (BUSCO, QUAST). There is one mandatory round (round 0). After that, during each round, the code checks the quality summary made by Busco.
#If the "Missing" number is lowering, it means that the quality of the assembly is rising, and thus the polishing is working. If this number is the same or higher than the previous summary round, the polishing has reached its potentials and there is no use for polishing further.


def Missed(B,Rep):

    ''' Returns the "Missing" number if the polishing is working, or stops the procedure if there is something wrong with the summary file.'''

    path = B+'/short_summary_BUSCO'+str(Rep)+'.txt'
    if os.path.exists(path):

        with open(path) as f:
            datafile = f.readlines()

        for s in datafile[-2].split():
            if s.isdigit():
                Missing_N = int(s)
                return Missing_N
    else:
        print("This Busco file does not include the information asked.")
        global Missing
        Missing = False
        return




def N50(Q):

    ''' Returns the N50 number if the polishing is working, or stops the procedure if there is something wrong with the report file.'''

    path = Q +'/report.txt'
    if os.path.exists(path):

        with open(path) as f:
            datafile = f.readlines()

        for s in datafile[-5].split():
            if s.isdigit():
                N50 = int(s)
                return N50

    else:
        print("This Quast file does not include the information asked.")
        global Missing
        Missing = False
        return


def Polish_with_Pilon(Rep, Ldir, Sdir, FastaFile, OutDir, L):

    ''' Minimap2 and Samtools give input to Pilon. Each file is marked with the iteration number it was created by. '''

    os.system("minimap2 -ax sr " + FastaFile + " " + Sdir + "/trimmomatic_output/*.fastq* > " + str(Rep) + "_mapP.sam")
    os.system("samtools view -S -b -@" + str(snakemake.threads)+ " " + str(Rep) + "_mapP.sam > " + str(Rep) + "_mapP.bam &&\ ")
    os.system("samtools sort " + str(Rep) + "_mapP.bam -@" + str(snakemake.threads) + " > " + str(Rep) + "_Sorted_mapP.bam &&\ ")
    os.system("samtools index " + str(Rep) + "_Sorted_mapP.bam ")

    os.system("java -Xmx"+snakemake.params["XMX"]+" -jar /opt/conda/envs/Piloning/share/pilon-1.23-2/pilon-1.23.jar --genome " +FastaFile+ " --frags  " +str(Rep)+ "_Sorted_mapP.bam --outdir "+OutDir+ " --output " + str(Rep)+ "_pilon --fix all --changes --threads " +str(snakemake.threads))

    os.system("quast -o " + Ldir + "/Quast_Results/QA_Pilon"+str(Rep)+" "+OutDir+"/"+ str(Rep)+ "_pilon.fasta -t " + str(snakemake.threads))
    os.system("python3.6 /run_BUSCO.py -i " +OutDir+"/" +str(Rep)+"_pilon.fasta -o BUSCO"+str(Rep)+" -m geno -l "+L+" -c " +str(snakemake.threads)+ " -sp " +snakemake.params["SP"])

    os.system("mv run_BUSCO"+ str(Rep)+" "+Ldir+ "/Busco_Results/QA_Pilon"+str(Rep))
    os.system("mv *mapP.* " + OutDir)
    os.system("rm "+OutDir+"/*.sam")
    os.system("gzip -r " +OutDir+ "/*.bam*")
    
    return (OutDir+"/"+str(Rep)+ "_pilon.fasta", Ldir+ "/Busco_Results/QA_Pilon"+str(Rep), Ldir+ "/Quast_Results/QA_Pilon"+str(Rep))
    



L = snakemake.input[1][:-30]+snakemake.params["Lineage"]  #The lineage for BUSCO 
Missing = True # The variable (flag) that informs whether the BUSCO summary files are found each time or something went wrong.
Rep = 0 #The number of iterations

[FastaFile, Bfile, Qfile] = Polish_with_Pilon(Rep, snakemake.input[1][:-42], snakemake.input[0], snakemake.input[1],snakemake.output[0], L) #1st round, mandatory
First_Missing = Missed(Bfile,Rep) #The "Missing" number of the 1st round
First_N50 = N50(Qfile) #The N50 number of the 1st round

while Missing: #While the flag is TRUE, continue polishing.

    Rep = Rep+1
    [FastaFile, Bfile, Qfile] = Polish_with_Pilon(Rep, snakemake.input[1][:-42], snakemake.input[0], FastaFile,snakemake.output[0], L)
    Second_Missing = Missed(Bfile,Rep)
    Second_N50 = N50(Qfile)

    if ((First_Missing - Second_Missing)>=5) and ((First_N50 - Second_N50) >= 500000): #The conditions for breaking the loop
        First_Missing = Second_Missing
        First_N50 = Second_N50
    else:
        os.system("mv "+FastaFile+" "+snakemake.output[0]+"/final.fasta") #The last assembly is called final.fasta
        break




