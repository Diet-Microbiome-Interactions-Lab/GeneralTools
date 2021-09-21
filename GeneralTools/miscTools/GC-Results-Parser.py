'''
'''
import os

import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import linregress


class GC_Entry:

    def __init__(self, entry):
        self.entry = entry
        # print(self.entry)
        complete = self.checkCompleteEntry()
        if complete:
            self.assertSelfAttributes()
            self.assignSelfAttributes()
            self.assignPeakTable()
            if self.checkPeaks():
                self.appendNormalizedPeaks()
        else:
            return None

    def checkCompleteEntry(self):
        if '[Compound Results(Ch1)]' in self.entry:
            return True
        else:
            return False

    def assertSelfAttributes(self):
        entries = [val.split('\t') for val in self.entry]
        assert entries[1][0] == 'Application Name', 'Invalid Line 2'
        assert entries[2][0] == 'Version', 'Invalid Line 3'
        assert entries[3][0] == 'Data File Name', 'Invalid Line 4'
        assert entries[4][0] == 'Output Date', 'Invalid Line 5'
        assert entries[5][0] == 'Output Time', 'Invalid Line 6'
        assert entries[16][0] == 'Acquired', 'Invalid line 17'
        assert entries[18][0] == 'Level', 'Invalid Line 19'
        assert entries[19][0] == 'Sample Name', 'Invalid Line 20'
        assert entries[79][0] == '# of Peaks', 'Invalid Line 80'

    def assignSelfAttributes(self):
        entries = [val.split('\t') for val in self.entry]
        self.ApplicationName = entries[1][1]
        self.Version = entries[2][1]
        self.DataFileName = entries[3][1]
        self.OutputDate = entries[4][1]
        self.OutputTime = entries[5][1]
        self.AcquiredTime = entries[16][1]
        self.Level = int(entries[18][1])
        self.SampleName = entries[19][1]
        self.NumberOfPeaks = int(entries[79][1])
        return 0

    def cleanupHeader(self, string):
        return [val.rstrip().replace('.', '').replace(' ', '_')
                for val in self.entry[80].split('\t')]

    def assignPeakTable(self):
        if self.NumberOfPeaks == 0:
            self.PeakTable = pd.DataFrame()
            return 0
        header = self.cleanupHeader(self.entry[80].split('\t'))
        tableValues = []
        for cnt, eachLine in enumerate(self.entry[81:]):
            if eachLine != '':
                currentPeakEntry = eachLine.split('\t')
                assert len(currentPeakEntry) == len(
                    header), 'Invalid Peak Entries'
                tableValues.append(currentPeakEntry)
            else:
                df = pd.DataFrame(tableValues, columns=header)
                df = df.replace(r'^\s*$', 'Unknown', regex=True)
                assert df.shape[1] == 21, 'Invalid columns'
                break
        self.PeakTable = df
        return 0

    def checkPeaks(self):
        if self.PeakTable.empty:
            # print(f'No peaks in {self.DataFileName}')
            self.isocupricArea = 0
            return False
        if 'Isocupric' not in list(self.PeakTable.Name):
            # print(f'No isocupric in {self.DataFileName}')
            self.isocupricArea = 0
            return False
        return True

    def appendNormalizedPeaks(self):
        pt = self.PeakTable.copy()
        self.isocupricArea = float(pt.loc[pt['Name'] == 'Isocupric', 'Area'])
        pt['Area'] = pt['Area'].astype(float, errors='raise')
        pt['NormalizedArea'] = pt['Area'] / self.isocupricArea
        self.PeakTable = pt
        return 0


class GC_Experiment:

    def __init__(self, ProjectFile):
        self.ProjectFile = ProjectFile
        self.AcidConcentrations = {'Acetate': [7.5, 15, 30, 60, 120],
                                   'Propionate':  [1.875, 3.75, 7.5, 15, 30],
                                   'Isobutyrate': [0.9375, 1.875, 3.75, 7.5, 15],
                                   'Butyrate':    [1.875, 3.75, 7.5, 15, 30],
                                   'Isovalerate': [0.9375, 1.875, 3.75, 7.5, 15],
                                   'Isocupric':   [0.998, 0.999, 1, 1.001, 1.002]}
        self.GC_Entries = self.createGCList()
        self.standardEntries, self.unknownEntries = self.grabGCStandardUnknownEntries()
        self.standardNormalizedAcids = self.grabStandardAcidValues()
        self.meanStandardNormalizedAcids = self.calculateMeanStandardAcidValues()
        self.standardAcidModels = self.calculateStandardAcidRegression()
        self.FinalTable = self.appendNormalizedConcentration()

    def testEntryStart(self, line):
        assert line.startswith('[Header]'), 'Invalid entry'

    def readUntilEntryEnd(self, open_file, current_line):
        entryLines = [current_line.strip()]
        line = open_file.readline()
        while line and not line.startswith('[Header]'):
            entryLines.append(line.strip())
            line = open_file.readline()
        return entryLines, line

    def createGCList(self):
        '''
        '''
        n = 0  # Keep track of the order
        gcClassEntries = []
        with open(self.ProjectFile) as openFile:
            line = openFile.readline()
            while line:
                self.testEntryStart(line)
                currentEntryLines, line = self.readUntilEntryEnd(
                    openFile, line)
                currentGCEntry = GC_Entry(currentEntryLines)
                currentGCEntry.Order = n
                gcClassEntries.append(currentGCEntry)
                n += 1

        return gcClassEntries

    def checkUsefulEntry(self, gcEntryObject):
        if gcEntryObject.PeakTable.empty:
            return False
        elif gcEntryObject.isocupricArea == 0:
            return False
        return True

    def grabGCStandardUnknownEntries(self):
        standardEntries = []
        unknownEntries = []
        for gcEntry in self.GC_Entries:
            if gcEntry.Level != 0:
                standardEntries.append(gcEntry)
            else:
                unknownEntries.append(gcEntry)
        return standardEntries, unknownEntries

    def checkAllAcidsInStandard(self):
        # ALSO CHECK ALL STANDARD LEVELS PER ACID!
        acceptableAcids = ['Acetate', 'Propionate', 'Isobutyrate',
                           'Isovalerate', 'Butyrate', 'Isocupric']
        for standardEntry in self.standardEntries:
            if all(acid in standardEntry.PeakTable.tolist() for acid in acceptableAcids):
                return True
        else:
            raise IndexError(f"GC Standard entry does not contain all acids!")

    def grabStandardAcidValues(self):
        standardNormalizedAcids = {}
        for standardEntry in self.standardEntries:
            CPT = standardEntry.PeakTable  # CPT == current peak table (abbr.)
            for acid in self.AcidConcentrations.keys():
                acidNormValue = CPT['NormalizedArea'][CPT['Name'] == acid]
                standardNormalizedAcids.setdefault(acid, {})
                standardNormalizedAcids[acid].setdefault(
                    standardEntry.Level, [])
                standardNormalizedAcids[acid][standardEntry.Level].append(acidNormValue.tolist()[
                                                                          0])
        return standardNormalizedAcids

    def calculateMeanStandardAcidValues(self):
        SNA = self.standardNormalizedAcids
        # SNA == standardNormalizedAcids (abbr.)
        meanSNA = {}
        for acid in SNA:
            for level in SNA[acid]:
                currentMean = sum(
                    SNA[acid][level]) / len(SNA[acid][level])
                meanSNA.setdefault(acid, [])
                meanSNA[acid].append(currentMean)
        return meanSNA

    def calculateStandardAcidRegression(self):
        # MSNA == meanStandardNormalizedAcids
        MSNA = self.meanStandardNormalizedAcids
        MSNARegression = {}
        for acid in MSNA:
            MSNA[acid].sort(reverse=False)
            print(acid)
            print(self.AcidConcentrations[acid])
            print(MSNA[acid])
            model = linregress(
                self.AcidConcentrations[acid], MSNA[acid])
            MSNARegression[acid] = model
        return MSNARegression

    def calculateAppendConcentration(self, peakTable):
        pt = peakTable.copy()
        pt['Concentration'] = None
        for acid in self.standardAcidModels:
            slope = self.standardAcidModels[acid].slope
            intercept = self.standardAcidModels[acid].intercept
            pt['Concentration'][pt['Name'] == acid] = (
                pt['NormalizedArea'] / slope) - intercept
        return pt

    def appendNormalizedConcentration(self):
        FinalTable = []
        for entry in self.GC_Entries:
            if self.checkUsefulEntry(entry):
                entry.FinalPeakTable = self.calculateAppendConcentration(
                    entry.PeakTable)
                entry.FinalPeakTable['Sample'] = entry.SampleName
                FinalTable.append(entry.FinalPeakTable)
        FinalTable = pd.concat(FinalTable)
        # self.FinalTable.to_excel('FinalData.xlsx')
        return FinalTable

    def plotStandardCurves(self):
        fig, axs = plt.subplots(len(self.AcidConcentrations))
        for cnt, acid in enumerate(self.standardAcidModels):
            m = self.standardAcidModels[acid].slope
            b = self.standardAcidModels[acid].intercept
            acidConcentrations = self.AcidConcentrations[acid]
            regressionLine = [(val * m) + b for val in acidConcentrations]
            meanStandardValue = self.meanStandardNormalizedAcids[acid]
            axs[cnt].scatter(acidConcentrations, regressionLine, label=acid)
            axs[cnt].scatter(acidConcentrations, meanStandardValue)
            axs[cnt].legend()
        plt.show()

    def analyzeInternalStandard(self):
        fig, axs = plt.subplots(2)
        isocupricAll = []
        Order = []
        time = []
        for entry in self.GC_Entries:
            isocupricAll.append(entry.isocupricArea)
            Order.append(entry.Order)
            time.append(entry.AcquiredTime)
        axs[0].scatter(Order, isocupricAll)
        axs[0].tick_params(labelrotation=90, size=5)
        isocupricAll.sort()
        self.isocupricAll = isocupricAll
        model = linregress(Order,
                           isocupricAll)
        y = [(v * model.slope) + model.intercept for v in Order]
        axs[1].plot(Order, y)
        axs[1].scatter(Order, isocupricAll)
        plt.show()
        data = {}
        data['AcquiredTime'] = time
        data['Isocupric'] = isocupricAll
        df = pd.DataFrame(data)
        df.to_excel('Isocupric-Standard-Analysis.xlsx')


# filename = 'BSM-Donor1-Results-25May21.txt'
# filename = 'Jayani_donor1.txt'
filename = 'Donor2-Jayani.txt'
# gcfiles = createGCList(filename)
GCProject = GC_Experiment(filename)
# GCProject.plotStandardCurves()
# GCProject.analyzeInternalStandard()
print(GCProject.FinalTable)
