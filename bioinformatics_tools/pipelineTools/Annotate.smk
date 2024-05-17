import os
from datetime import datetime
tstamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S") 
configfile: os.environ['DEFAULT_CONFIG']
#configfile: "config.yaml"

assemblies, = glob_wildcards(f'{config["contigs"]}/{{samples}}.{config["extension"]}')

rule all:
    input:
        expand("GFF3-Final/{sample}.gff3", sample=assemblies),
        #expand("Annotations/Other/{dbs}.estimate_scgs", dbs=glob_wildcards(f'{config["contigdb"]}/{{value}}.db').value),

# INTERNAL PHASE
rule Reformat_Fasta:
    input:
        origin=f'{config["contigs"]}/{{sample}}.{config["extension"]}'
    output:
        final=f'{config["clean_contigs"]}/{{sample}}-SIMPLIFIED.{config["extension"]}'
    log: f'Logs/Reformat_Fasta__{{sample}}.{config["log_id"]}.log'
    group: "main"
    shell:
        """
        anvi-script-reformat-fasta {input.origin} -o {output.final} --simplify-names --seq-type NT &> {log}
        """

rule Create_Database:
    input:
        gen=f'{config["clean_contigs"]}/{{sample}}-SIMPLIFIED.{config["extension"]}'
    output:
        out=f'{config["contigdb"]}/{{sample}}.db'
    params:
        title='This is my project',
    log: f'Logs/Create_Database__{{sample}}.{config["log_id"]}.log'
    threads: config["threads"]
    group: "main"
    shell:
        """
        anvi-gen-contigs-database -T {threads} -f {input.gen} -n '{wildcards.sample} {params.title}' -o {output.out} &> {log}
        """

rule Run_HMMs:
    input:
        one=ancient(f'{config["contigdb"]}/{{sample}}.db'),
    output:
        touch("Annotations/HMMs/{sample}.run_hmm")
    log: f'Logs/Run_HMMs__{{sample}}.{config["log_id"]}.log'
    threads: config["threads"]
    group: "main"
    priority: 25
    shell:
        """
        anvi-run-hmms -c {input.one} -T {threads} --just-do-it --also-scan-trnas &> {log}
        """

rule Run_SCG_Taxonomy:
    input:
        db=ancient(f'{config["contigdb"]}/{{sample}}.db')
    output:
        estimate_out="Annotations/Other/{sample}.estimate_scgs",
    log:
        f'Logs/Run_SCGs__{{sample}}.{config["log_id"]}.log'
    priority: 90
    threads: config["threads"]
    shell:
        """
        anvi-run-scg-taxonomy -c {input.db} -T {threads} &> {log}
        anvi-estimate-scg-taxonomy -c {input.db} --output-file {output.estimate_out} -T {threads} --metagenome-mode
        """

rule Run_COGs:
    input:
        ancient(f'{config["contigdb"]}/{{sample}}.db') 
    output:
        touch("Annotations/Cog/{sample}.cog")
    log: f'Logs/Run_COGs__{{sample}}.{config["log_id"]}.log'
    threads: config["threads"]
    group: "main"
    priority: 25
    shell:
        """
        anvi-run-ncbi-cogs -T {threads} -c {input} &> {log}
        """

rule Run_Kegg:
    input:
        ancient(f'{config["contigdb"]}/{{sample}}.db')
    output:
        touch("Annotations/Kegg/{sample}.kegg")
    log: f'Logs/Run_Kegg__{{sample}}.{config["log_id"]}.log' 
    threads: config["threads"]
    group: "main"
    priority: 25
    shell:
        """
        anvi-run-kegg-kofams -c {input} -T {threads} --just-do-it &> {log}
        """

rule Run_PFams:
    input:
        ancient(f'{config["contigdb"]}/{{sample}}.db')
    output:
        touch("Annotations/Pfam/{sample}.pfam")
    log: f'Logs/Run_PFams__{{sample}}.{config["log_id"]}.log'
    threads: config["threads"]
    group: "main"
    priority: 25
    shell:
        """
        anvi-run-pfams -c {input} -T {threads} &> {log}
        """

# EXPORTING PHASE
rule Export_FAA:
    input:
        ancient(f'{config["contigdb"]}/{{sample}}.db')
    output:
        "FAAs/{sample}.faa"
    log: f'Logs/Export_FAA__{{sample}}.{config["log_id"]}.log'   
    group: "main"
    priority: 15
    shell:
        """
        anvi-get-sequences-for-gene-calls -c {input} --get-aa-sequences -o {output} &> {log}
        """

rule Export_Gene_Calls:
    input:
        ancient(f'{config["contigdb"]}/{{sample}}.db')
    output:
        "GeneCalls/{sample}.gff"
    log: f'Logs/Export_Gene_Calls__{{sample}}.{config["log_id"]}.log'   
    group: "main"
    priority: 15
    shell:
        """
        anvi-export-gene-calls -c {input} -o {output} --gene-caller prodigal &> {log}
        """

# EXTERNAL ANNOTATION
rule RAST_Run:
    input:
        "FAAs/{sample}.faa"
    output:
        "Annotations/RAST/{sample}-RAST-FAA.txt"
    #log: f'Logs/RAST_Run__{{sample}}.{config["log_id"]}.log'
    group: "main"
    priority: 10
    shell:
        """
        svr_assign_using_figfams < {input} > {output}
        """

rule RAST_Reformat:
    input:
        "Annotations/RAST/{sample}-RAST-FAA.txt"
    output:
         "Annotations/RAST/{sample}-RAST-FAA.txt.anvio"
    log: f'Logs/RAST_Reformat__{{sample}}.{config["log_id"]}.log'
    group: "main"
    priority: 10
    shell:
        """
        rast-table.py {input} {output} &> {log}
        """

rule RAST_Import:
    input:
        db=ancient(f'{config["contigdb"]}/{{sample}}.db'),
        imp="Annotations/RAST/{sample}-RAST-FAA.txt.anvio"
    output:
        touch("Annotations/RAST/{sample}.rast_added")
    log: f'Logs/RAST_Import__{{sample}}.{config["log_id"]}.log' 
    group: "main"
    priority: 10
    shell:
        """
        anvi-import-functions -c {input.db} -i {input.imp} &> {log}
        """

rule TigrFam_Run:
    input:
        "FAAs/{sample}.faa"
    output:
        one="Annotations/TigrFamResults/{sample}.hmmer.TIGR.hmm",
        two="Annotations/TigrFamResults/{sample}.hmmer.TIGR.tbl"
    log: f'Logs/TigrFam_Run__{{sample}}.{config["log_id"]}.log' 
    threads: config["threads"]
    group: "main"
    priority: 10
    shell:
        """
        hmmsearch -o {output.one} --tblout {output.two} --cpu {threads} /depot/lindems/data/Databases/TIGRFams/AllTigrHmms.hmm {input} &> {log}
        """

rule TigrFam_Reformat:
    input:
        "Annotations/TigrFamResults/{sample}.hmmer.TIGR.tbl"
    output:
        "Annotations/TigrFamResults/{sample}.hmmer.TIGR.anvio.tbl"
    params:
        tfam="/depot/lindems/data/Dane/CondaEnvironments/SnakeStuff/scripts/TFAM-Roles.txt"
    log: f'Logs/TigrFam_Reformat__{{sample}}.{config["log_id"]}.log'
    group: "main"
    priority: 10
    shell:
        """
        tigrfam-table.py {input} {params.tfam} {output} &> {log}
        """

rule TigrFam_Import:
    input:
        db=ancient(f'{config["contigdb"]}/{{sample}}.db'),
        imp="Annotations/TigrFamResults/{sample}.hmmer.TIGR.anvio.tbl"
    output:
        touch("Annotations/TigrFamResults/{sample}.tigr_added")
    log: f'Logs/TigrFam_Import__{{sample}}.{config["log_id"]}.log'
    group: "main"
    priority: 10
    shell:
        """
        anvi-import-functions -c {input.db} -i {input.imp}  &> {log}
        """

# EXPORTING ANNOTATIONS
rule Export_Annotations:
    input:
        db=ancient(f'{config["contigdb"]}/{{sample}}.db'),
        hmms="Annotations/HMMs/{sample}.run_hmm",
        cogs="Annotations/Cog/{sample}.cog",
        kegg="Annotations/Kegg/{sample}.kegg",
        pfams="Annotations/Pfam/{sample}.pfam",
        figfams="Annotations/RAST/{sample}.rast_added",
        tigrfams="Annotations/TigrFamResults/{sample}.tigr_added",
    output:
        out="Annotations/Annotations-Exported/{sample}.gff3"
    log: f'Logs/Export_Annotations__{{sample}}.{config["log_id"]}.log' 
    params:
        annotations="FigFams,KEGG_Module,COG20_PATHWAY,TIGRFAM,KOfam,KEGG_Class,COG20_FUNCTION,Pfam,COG20_CATEGORY"
    group: "exporting"
    priority: 0
    shell:
        """
        anvi-export-functions -c {input.db} --annotation-sources {params.annotations} -o {output.out} &> {log}
        """

rule Reformat_Gff3:
    input:
        anvio_annotations="Annotations/Annotations-Exported/{sample}.gff3",
        gene_calls="GeneCalls/{sample}.gff",
    output:
        gff3_final="GFF3-Final/{sample}.gff3"
    log: f'Logs/Reformat_Gff3__{{sample}}.{config["log_id"]}.log'
    group: "exporting"
    priority: 0
    shell:
        """
        combineFunctionsAndGeneCalls.py {input.gene_calls} {input.anvio_annotations} {output.gff3_final} &> {log}
        """

# OTHER ANNOTATIONS

