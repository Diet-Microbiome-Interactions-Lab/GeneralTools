configfile: os.environ['DEFAULT_CONFIG']

assemblies, = glob_wildcards(f'{config["assembly"]}/{{samples}}.{config["assembly_extension"]}')

rule all:
    input:
        expand("Binning/Maxbin/{sample}/bins.summary", sample=assemblies),
        expand("Binning/Metabat/{sample}/Complete.tkn", sample=assemblies),
        expand("Binning/Concoct/{sample}/clustering_gt2000.csv", sample=assemblies),
        expand("Binning/Semibin/{sample}/data.csv", sample=assemblies),
        expand("Binning/BinIds/{sample}__Complete.tkn", sample=assemblies),
        expand("Binning/Dastool/{sample}_DASTool.log", sample=assemblies)


rule Run_Maxbin:
    input:
        abund="Abundances/Abundance_List.txt",
        contigs=f'{config["clean_assembly"]}/{{sample}}-SIMPLIFIED.fasta'
    output:
        out="Binning/Maxbin/{sample}/bins.summary",
        tkn="Binning/Maxbin/{sample}/Complete.tkn"
    params:
        pref=directory("Binning/Maxbin/{sample}")
    threads: config["threads"]
    priority: 100
    group: "Binning" 
    shell:
        """
        run_MaxBin.pl -contig {input.contigs} -out {params.pref}/bins -abund_list {input.abund} -thread {threads} -min_contig_length 2000
        touch {output.tkn}
        """

rule Run_Metabat:
    input:
        depth="Depths/Depth_List.txt"
    params:
        pref="Binning/Metabat/{sample}/bin",
        contigs=f'{config["clean_assembly"]}/{{sample}}-SIMPLIFIED.fasta'
    output:
        touch("Binning/Metabat/{sample}/Complete.tkn")
        #directory("Binning/Metabat/{sample}")
    threads: config["threads"]
    priority: 100
    group: "Binning" 
    shell:
        """
        metabat2 -i {params.contigs} -a {input.depth} -o {params.pref} --minContig 2000 -t {threads}
        """

rule Run_Concoct:
    input:
        coverage="Beds/{sample}.coverage_table.tsv"
    params:
        pref="Binning/Concoct/{sample}",
        contigs=f'{config["clean_assembly"]}/{{sample}}-SIMPLIFIED.fasta',
        splits="Beds/{sample}_10k.fasta"
    output:
        clustering="Binning/Concoct/{sample}/clustering_gt2000.csv",
        merged="Binning/Concoct/{sample}/clustering_merged.csv",
        tkn="Binning/Concoct/{sample}/Complete.tkn"
    threads: config["threads"]
    priority: 100
    group: "Binning" 
    shell:
        """
        concoct --composition_file {params.splits} --coverage_file {input.coverage} -b {params.pref} --threads {threads} -l 2000
        merge_cutup_clustering.py {output.clustering} > {output.merged}
        extract_fasta_bins.py {params.contigs} {output.merged} --output_path {params.pref}
        touch {output.tkn}
        """

rule Run_Semibin:
    input:
        contigs=f'{config["clean_assembly"]}/{{sample}}-SIMPLIFIED.fasta',
        bams=expand("Bams/{sample}.sorted.bam",sample=glob_wildcards("Bams/{filename}.sorted.bam").filename)
    params:
        pref=directory("Binning/Semibin/{sample}/")
    output:
        out="Binning/Semibin/{sample}/data.csv",
        tkn="Binning/Semibin/{sample}/Complete.tkn"
    threads: config["threads"]
    priority: 100 
    group: "Binning"
    shell:
        """
        SemiBin single_easy_bin -i {input.contigs} -b {input.bams} -o {params.pref} --environment human_gut -t {threads}
        touch {output.tkn}
        """

rule Make_Binids:
    input:
        concoct=expand("Binning/Concoct/{{sample}}/{bin_number}.fa",
                bin_number=glob_wildcards("Binning/Concoct/{sample}/{value}.fa").value),
        maxbin=expand("Binning/Maxbin/{{sample}}/{bin_number}.fasta",
                bin_number=glob_wildcards("Binning/Maxbin/{sample}/{value}.fasta").value),
        semibin=expand("Binning/Semibin/{{sample}}/output_bins/{bin_number}.fa",
                bin_number=glob_wildcards("Binning/Semibin/{sample}/output_bins/{value}.fa").value),
        metabat=expand("Binning/Metabat/{{sample}}/{bin_number}.fa",
                bin_number=glob_wildcards("Binning/Metabat/{sample}/{value}.fa").value),
        cnc_tkn="Binning/Concoct/{sample}/Complete.tkn",
        mxb_tkn="Binning/Maxbin/{sample}/Complete.tkn",
        smb_tkn="Binning/Metabat/{sample}/Complete.tkn",
        mtb_tkn="Binning/Semibin/{sample}/Complete.tkn"
    output:
        concoct="Binning/BinIds/Concoct-{sample}.txt",
        maxbin="Binning/BinIds/Maxbin-{sample}.txt",
        metabat="Binning/BinIds/Metabat-{sample}.txt",
        semibin="Binning/BinIds/Semibin-{sample}.txt",
        tkn="Binning/BinIds/{sample}__Complete.tkn"
    priority: 50
    group: "Binning"
    shell:
        """
        fastaTools createBinID -f {input.concoct} -o {output.concoct}
        fastaTools createBinID -f {input.maxbin} -o {output.maxbin}
        fastaTools createBinID -f {input.semibin} -o {output.semibin}
        fastaTools createBinID -f {input.metabat} -o {output.metabat}
        touch {output.tkn}
        """

rule Run_Dastool:
    input:
        contigs=f'{config["clean_assembly"]}/{{sample}}-SIMPLIFIED.fasta',
        concoct="Binning/BinIds/Concoct-{sample}.txt",
        maxbin="Binning/BinIds/Maxbin-{sample}.txt",
        metabat="Binning/BinIds/Metabat-{sample}.txt",
        semibin="Binning/BinIds/Semibin-{sample}.txt"
    params:
        sources="Concoct,Maxbin2,Metabat2,Semibin",
        pref="Binning/Dastool/{sample}"
    output:
        "Binning/Dastool/{sample}_DASTool.log"
    priority: 50
    group: "Binning"
    shell:
        """
        DAS_Tool -i {input.concoct},{input.maxbin},{input.metabat},{input.semibin} -c {input.contigs} \
                -o {params.pref} --write_bins --write_bins_evals -t {threads} -l {params.sources} \
                --search_engine diamond --write_unbinned
        """


