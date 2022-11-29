from GCResultsParser import GC_Experiment
import pandas as pd


def convertToExcel(data):
    gc = GC_Experiment(data)
    all_dfs = []
    for val in gc.GC_Entries:
        val.PeakTable['Sample'] = val.SampleName
        all_dfs.append(val.PeakTable)
    appended_data = pd.concat(all_dfs)
    appended_data.to_excel('ARO_Donor3-Table.xlsx')
    return 0
