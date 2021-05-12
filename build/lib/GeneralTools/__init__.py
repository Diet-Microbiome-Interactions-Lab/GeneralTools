import sys


mypackage_version = '0.1-setup'

# Ensure the user is using python version >= 3
try:
    if sys.version_info.major != 3:
        sys.stderr.write(
            f"Your python version is not >= 3. You version is {sys.version_info.major}.")
        sys.exit(-1)
except Exception:
    sys.stderr.write("Failed to determine what python version is being used.")


main_help = "This is the documentation for the main help."

toolSets = ['fastaTools', 'annotationTools']

# Dictionaries for each executable script to find their programs

alignmentTools_programs = {
    'filterBamByReference': (
        {'help': ('ADD TO THIS')}
    ),
    'samThresholdFilter': (
        {'help': ('ADD TO THIS')}
    ),
}


annotationTools_programs = {
    'createVanillaGFF': (
        {'help': ('Given a multi - fasta file, create a < vanilla > GFF file '
                  'that can be utilized by programs like HTSeqCount to get'
                  'counts per feature.')}
    ),
    'gffMine': (
        {'help': 'This is the help for gffMine'}
    ),
    'trimGFFByFeature': (
        {'help': 'This is the help for trimGFFByFeature'}
    ),
    'writeFlaggedContigsNewBinID': (
        {'help': 'This is the help for writeFlaggedContigsNewBinID'}
    ),
    'writeModeGFFFeaturePerBin': (
        {'help': 'This is the help for writeModeGFFFeaturePerBin'}
    ),
    'writeTaxonRemovedFastas': (
        {'help': 'This is the help for gffMine'}
    ),
}


fastaTools_programs = {
    'changeBinNodeNames': (
        {'help': 'ADD TO THIS'}
    ),
    'compareTwoBinFiles': (
        {'help': 'ADD TO THIS'}
    ),
    'createBinID': (
        {'help': 'ADD TO THIS'}
    ),
    'fastaStats': (
        {'help': 'This is the help for fastaStats'}
    ),
    'filterAssembly': (
        {'help': 'ADD TO THIS'}
    ),
    'filterSeqlength': (
        {'help': 'ADD TO THIS'}
    ),
    'grabEntryDiffs': (
        {'help': 'ADD TO THIS'}
    ),
    'magBinMatrix': (
        {'help': 'ADD TO THIS'}
    ),
    'pfam_tigrfam_processing_anvio': (
        {'help': 'ADD TO THIS'}
    ),
    'split_multifasta': (
        {'help': 'ADD TO THIS'}
    ),
    'tetranucleotideFreq': (
        {'help': 'Help for tetranucleotideFreq'}
    ),
    'writeFastaFromBinID': (
        {'help': 'ADD TO THIS'}
    ),
    'writeLargestSequences': (
        {'help': 'ADD TO THIS'}
    ),
}


miscTools_programs = {
    'appendBinID': (
        {'help': 'ADD TO THIS'}
    ),
    'CatToBatOutputConverter': (
        {'help': 'ADD TO THIS'}
    ),
    'compare2BinIDs': (
        {'help': 'ADD TO THIS'}
    ),
    'constainsUniGCodeParser': (
        {'help': 'ADD TO THIS'}
    ),
    'convertTPM': (
        {'help': 'ADD TO THIS'}
    ),
    'dnaDiffCrawler': (
        {'help': 'ADD TO THIS'}
    ),
    'grabCheckMOut': (
        {'help': 'ADD TO THIS'}
    ),
    'KeggTranslator': (
        {'help': 'ADD TO THIS'}
    ),
    'mergeCounts': (
        {'help': 'ADD TO THIS'}
    ),
    'processMetaphlanOutput': (
        {'help': 'ADD TO THIS'}
    ),
    'recursivelyMoveFiles': (
        {'help': 'ADD TO THIS'}
    ),
    'subjectEncryption': (
        {'help': 'ADD TO THIS'}
    ),
    'vcf_filter': (
        {'help': 'ADD TO THIS'}
    ),
}
