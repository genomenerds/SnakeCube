
import os

#Run Minimap2 and Racon as many times as the user has defined (iterations). Add to each output file the number of the iteration that has exported it.
#The last round generates the racon_consensus.fasta which serves as input for medaka. Tide the outputs.



for iteration in range(1,int(snakemake.params["i"])+1):

	if iteration == 1:
		os.system("minimap2 -ax map-ont "+snakemake.input[0]+" "+snakemake.input[1]+" > "+str(iteration)+"_mapping.sam")
		os.system("racon -m 8 -x -6 -g -8 -w 500 -t "+ str(snakemake.threads)+" "+snakemake.input[1]+" "+str(iteration)+"_mapping.sam "+snakemake.input[0]+" >racon_"+str(iteration)+".fasta")
		os.system("gzip "+str(iteration)+"_mapping.sam")


	elif iteration != (1 and int(snakemake.params["i"])):
		os.system("minimap2 -ax map-ont racon_"+str(iteration-1)+".fasta "+snakemake.input[1]+" > "+str(iteration)+"_mapping.sam")
		os.system("racon -m 8 -x -6 -g -8 -w 500 -t "+ str(snakemake.threads)+" "+snakemake.input[1]+" "+str(iteration)+"_mapping.sam racon_"+str(iteration-1)+".fasta >racon_"+str(iteration)+".fasta")
		os.system("gzip "+str(iteration)+"_mapping.sam")
		os.system("gzip racon_"+str(iteration-1)+".fasta")

	else:
		os.system("minimap2 -ax map-ont racon_"+str(iteration-1)+".fasta "+snakemake.input[1]+ " > "+str(iteration)+"_mapping.sam")
		os.system("racon -m 8 -x -6 -g -8 -w 500 -t "+ str(snakemake.threads)+" "+snakemake.input[1]+" "+str(iteration)+"_mapping.sam racon_"+str(iteration-1)+".fasta > racon_consensus.fasta")
		os.system("gzip "+str(iteration)+"_mapping.sam")
		os.system("gzip racon_"+str(iteration-1)+".fasta")



os.system("medaka_consensus -i "+snakemake.input[1]+" -d racon_consensus.fasta -t "+ str(snakemake.threads)+" -o "+snakemake.output[0][:-15])
os.system("mkdir "+snakemake.input[0][:-19]+"/Racon/")
os.system("mv *_mapping.sam* "+snakemake.input[0][:-19]+"/Racon/")
os.system("mv racon_* "+snakemake.input[0][:-19]+"/Racon/")

