configfile: os.environ['DEFAULT_CONFIG']

assemblies, = glob_wildcards(f'{config["assembly"]}/{{samples}}.{config["assembly_extension"]}')
#print(f'Assemblies: {assemblies}')

pe_fqs, = glob_wildcards(f'{config["fastq"]}/{{fq_samples}}_1.{config["fq_extension"]}')
print(pe_fqs)
print('Now to the se...')
se_fqs, = glob_wildcards(f'{config["fastq"]}/{{fq_samples}}.{config["fq_extension"]}')
se_fqs = [f for f in se_fqs if '_1' not in f]
se_fqs = [f for f in se_fqs if '_2' not in f]
#print(se_fqs)

rule all:
    input:
        expand(f"{config['clean_assembly']}/{{sample}}-SIMPLIFIED.1.bt2", sample=assemblies),
        expand("Bams/PE_{sample}-{fq}.sorted.bam.bai", fq=pe_fqs, sample=assemblies),
        expand("Bams/SE_{sample}-{fq}.sorted.bam.bai", fq=se_fqs, sample=assemblies),
        expand("Abundances/PE_{sample}-{fq}.abundance.txt", fq=pe_fqs, sample=assemblies),
        "Abundances/Abundance_List.txt",
        "Depths/Depth_List.txt",
        expand("Beds/{sample}.coverage_table.tsv", sample=assemblies)

rule Reformat_Fasta:
    input:
        f'{config["assembly"]}/{{sample}}.{config["assembly_extension"]}'
    output:
        f'{config["clean_assembly"]}/{{sample}}-SIMPLIFIED.fasta'
    log: f'Logs/Reformat_Fasta/{{sample}}.{config["log_id"]}.log' 
    group: "Indexing"
    priority: 100
    shell:
        """
        anvi-script-reformat-fasta {input} -o {output} --simplify-names --seq-type NT &> {log}
        """

rule Create_Index:
    input:
        f'{config["clean_assembly"]}/{{sample}}-SIMPLIFIED.fasta'
    output:
        f'{config["clean_assembly"]}/{{sample}}-SIMPLIFIED.1.bt2'
    log: f'Logs/Create_Index/{{sample}}.{config["log_id"]}.log'
    params:
        prefix=f'{config["clean_assembly"]}/{{sample}}-SIMPLIFIED'
    group: "Indexing"
    priority: 100
    threads: config["threads"]
    shell:
        """
        bowtie2-build --threads {threads} -f {input} {params.prefix} &> {log}
        """

rule Align_PE_Bams:
    input:
        index=f'{config["clean_assembly"]}/{{sample}}-SIMPLIFIED.1.bt2',
        pe1=f'{config["fastq"]}/{{fq}}_1.fastq.gz',
        pe2=f'{config["fastq"]}/{{fq}}_2.fastq.gz'
    output:
        bam=temp("Bams/PE_{sample}-{fq}.bam")
    log: f'Logs/Align_PE_Bams/{{sample}}-{{fq}}.{config["log_id"]}.log'
    params:
        index=f"{config['clean_assembly']}/{{sample}}-SIMPLIFIED"
    group: "Aligning"
    priority: 100
    threads: config["threads"]
    shell:
        """
        bowtie2 --threads {threads} -k 5 -x {params.index} -1 {input.pe1} -2 {input.pe2} | samtools view -b -o {output.bam} &> {log}
        """

rule Align_SE_Bams:
    input:
        index=f'{config["clean_assembly"]}/{{sample}}-SIMPLIFIED.1.bt2',
        se=f'{config["fastq"]}/{{fq}}.fastq.gz'
    output:
        bam=temp("Bams/SE_{sample}-{fq}.bam")
    log: f'Logs/Align_SE_Bams/{{sample}}-{{fq}}.{config["log_id"]}.log'
    params:
        index=f'{config["clean_assembly"]}/{{sample}}-SIMPLIFIED'
    group: "Aligning"
    threads: config["threads"]
    priority: 100 
    shell:
        """
        bowtie2 --threads {threads} -k 5 -x {params.index} -U {input.se} | samtools view -b -o {output.bam} &> {log}
        """

rule Sort_Bams:
    input:
        bam="Bams/{ended}_{sample}-{fq}.bam",
    output:
        sort="Bams/{ended}_{sample}-{fq}.sorted.bam"
    log: f'Logs/Sort_Bams/{{ended}}-{{sample}}-{{fq}}.{config["log_id"]}.log'
    group: "Aligning"
    threads: config["threads"]
    priority: 100 
    shell:
        """
        samtools sort -@{threads} -m1G -o {output.sort} {input.bam} &> {log}
        """

rule Index_Bams:
    input:
        sort="Bams/{ended}_{sample}-{fq}.sorted.bam"
    output:
        bai="Bams/{ended}_{sample}-{fq}.sorted.bam.bai"
    log: f'Logs/Index_Bams/{{ended}}-{{sample}}-{{fq}}.{config["log_id"]}.log'
    group: "Aligning"
    threads: config["threads"]
    priority: 100 
    shell:
        """
        samtools index -@{threads} {input.sort} &> {log}
        """

checkpoint BBMap_Count:
    input:
        sort="Bams/{ended}_{sample}-{fq}.sorted.bam"
    output:
        out="Abundances/{ended}_{sample}-{fq}.abundance.txt",
    log: f'Logs/BBMap_Count/{{ended}}-{{sample}}-{{fq}}.{config["log_id"]}.log'
    params:
        init_out="Abundances/{ended}_{sample}-{fq}.coverage.txt"
    priority: 100
    group: "Aligning"
    shell:
        """
        pileup.sh in={input.sort} out={params.init_out}
        cut -f 1,5 {params.init_out} | grep -v '^#' > {output}
        """


rule Abundance_List:
    input:
        infiles = expand("Abundances/{abund_file}-{fq}.abundance.txt", zip,
                         abund_file=glob_wildcards("Abundances/{sam}-{tmp}.abundance.txt").sam,
                         fq=pe_fqs),
    output:
        "Abundances/Abundance_List.txt"
    priority: 50
    group: "Counting"
    script:
        "/depot/lindems/data/Dane/CondaEnvironments/SnakeStuff/scripts/make_abund_list.py"

rule Depth_List:
    input:
        bams=expand("Bams/{sample}.sorted.bam",
                    sample=glob_wildcards("Bams/{filename}.sorted.bam").filename)
    output:
        "Depths/Depth_List.txt"
    priority: 50
    group: "Counting"
    shell:
        """
        jgi_summarize_bam_contig_depths --outputDepth {output} {input.bams}
        """

rule Coverage_List:
    input:
        assembly=f'{config["clean_assembly"]}/{{sample}}-SIMPLIFIED.fasta'
    output:
        bedfile="Beds/{sample}_10k.bed",
        coverage="Beds/{sample}.coverage_table.tsv"
    params:
        fasta="Beds/{sample}_10k.fasta",
        bams=expand("Bams/{sample}.sorted.bam",                                 
                    sample=glob_wildcards("Bams/{filename}.sorted.bam").filename)
    priority: 50
    group: "Counting"
    shell:
        """
        cut_up_fasta.py {input.assembly} -c 10000 -o 0 --merge_last -b {output.bedfile} > {params.fasta}
        concoct_coverage_table.py {output.bedfile} {params.bams} > {output.coverage}
        """
