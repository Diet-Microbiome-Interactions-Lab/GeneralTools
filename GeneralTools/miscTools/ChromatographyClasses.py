'''
raise ValueError when invalid GC/HPLC file is found
- Need to return 
{type: GCFile, report: {}}
'''
import argparse
import base64
from datetime import datetime
import hashlib
import os
import pandas as pd
from pathlib import Path

from scipy.stats import linregress

def process_chromatography_file(input_source: Path | str, instrument: str, savefile=None):
    '''
    If a string, we expect it to be the file content, otherwise we expect a Path object.
    '''
    try:
        content = input_source.read_text()
        filename = input_source.stem
    except AttributeError as e:
        content = input_source
        filename = 'Unknown'

    current_instance = Chromatography_Experiment(filename, content, instrument, runall=True)

    return current_instance.report(save=savefile)

class Chromatography_Entry:
    HASHSIZE = 16

    def __init__(self, entry: list[str], instrument, detector, logfile='log.txt'):
        self.logfile = logfile
        self.entry = entry
        self.type_: str = instrument
        self.detector = detector
        self.instrument = instrument
        # TODO: Maybe complete isn't the best name?
        self.complete = self.checkCompleteEntry()
        print(f'Complete: {self.complete}')
        if self.complete:
            self.assignSelfAttributes()
            print(f'INFO: Assigned self attributes')
            self.assertEntryValues()
            print(f'INFO: Asserted entry values')
            
            self.hash_ = self.assignHash()  # Entry hash
            self.assignPeakTable()
            print(f'INFO: Assigned peak table')
            self.assignMongoDocumentAttributes()
            print(f'INFO: Assigned mongo document attributes')
        else:
            # raise ValueError('Incomplete entry found.')
            print(f'Incomplete file found')  # TODO: LOG
            # with open(self.logfile, 'a') as log:
            #     log.write(f'Incomplete entry for {entry}\n')
        print(f'Initialized Chromatography_Entry: {self.Sample_Name}\n')

    def __str__(self):
        try:
            return f'Chromatography_Entry({self.Sample_Name})'
        except ValueError:
            return f'Incomplete entry: {self.entry}'

    def checkCompleteEntry(self):
        # print(f'DEBUG: Checking complete entry\n{self.entry}')
        assert self.entry[0] == '[Header]', ValueError(
            'Error in Chromatography_Entry-checkCompleteEntry: Header')
        return True
        # assert self.entry[-1] == '', ValueError(
        #     'Error in Chromatography_Entry-checkCompleteEntry: Last line')
        # return True
        # if self.column_type in self.entry:
        #     return True
        # else:
        #     return False

    def assignSelfAttributes(self):
        self.header_values = []
        for cnt, e in enumerate(self.entry):
            evals = e.split('\t')
            # TODO: Below is ugly, figure out later
            if e.startswith(('Detector', '# of Channels')):
                evals = [evals[0], evals[1:]]
                # print(evals)
                # print('\n')
            elen = len(evals)
            # print(f'Elen == {elen}')

            if elen == 1:
                if e != '':
                    self.header_values.append(evals[0])
            elif elen == 2:
                evals[0] = '_'.join(evals[0].split(' '))
                if evals[0].startswith('#'):
                    evals[0] = evals[0].replace('#', 'Number')
                if '#' in evals[0]:
                    evals[0] = evals[0].replace('#', 'Number')
                # print(f'Evals: {evals}')
                if hasattr(self, evals[0]):
                    if getattr(self, evals[0]) < evals[1]:
                        setattr(self, evals[0], evals[1])
                    pass  # Want to write first occurence of everthing
                else:
                    setattr(self, evals[0], evals[1])
            else:
                pass
        return 0

    def setSampleName(self, sample_name):
        # use property on sample name so we don't have invalid sample names
        return None

    def assertEntryValues(self):
        attribute_list = ['Application_Name', 'Version', 'Data_File_Name',
                          'Output_Date', 'Output_Time', 'Type', 'Acquired',
                          'Sample_Type', 'Sample_Name', 'Level', 'Number_of_Peaks']
        for attribute in attribute_list:
            assert getattr(
                self, attribute), f'Did not find the attribute {attribute}'
        self.Sample_Type = self.Sample_Type.split(':')[-1]
        self.Level = int(self.Level)
        return 0

    def assignHash(self):
        string = '\n'.join([v for v in self.entry])
        return base64.b85encode(hashlib.shake_128(
            string.encode('ascii')).digest(self.HASHSIZE)).decode('utf-8')

    def characterKey(self, list_):
        values = list_.split('\t')
        for idx, value in enumerate(values):
            if '.' in value:
                values[idx] = values[idx].replace('.', '')
            if "'" in value:
                values[idx] = values[idx].replace("'", '')
            if ' ' in value:
                values[idx] = values[idx].replace(' ', '_')
            if '#' in value:
                values[idx] = values[idx].replace('#', 'Number')
            if '/' in value:
                values[idx] = values[idx].replace('/', '_')
            if '%' in value:
                values[idx] = values[idx].replace('%', 'Percent')
        values.append('Detector')
        return values

    def cleanupHeader(self):
        for value in self.entry:
            if value.startswith('Peak#'):
                return self.characterKey(value)
        raise ValueError(
            f'No header found starting with ID# for entry {self.Data_File_Name}\nPeaks={self.Number_of_Peaks}')

    def grabAllPeakTableLines(self):
        all_peaklines = {}

        entry_iter = iter(self.entry)
        for value in entry_iter:
            if value.startswith('[Peak Table'):
                peaklines = []
                detector = value[value.find("(") + 1:value.find(")")]
                num_peaks_line = next(entry_iter, None)
                num_peaks = int(num_peaks_line.strip().split('\t')[-1])

                if num_peaks == 0:
                    continue
                else:
                    header = next(entry_iter, None)
                    sub_value = next(entry_iter, None)

                    while not sub_value == '' or sub_value is None:
                        peaklines.append(sub_value)
                        sub_value = next(entry_iter, None)
                    all_peaklines[detector] = peaklines

        return all_peaklines

    def assignPeakTable(self, df_size=15):
        if int(self.Number_of_Peaks) == 0:
            #     # TODO: Log print(f'Sample {self.Sample_Name} has no peaks!')
            self.PeakTable = pd.DataFrame()
            return 0
        header = self.cleanupHeader()
        peaklines = self.grabAllPeakTableLines()

        tableValues = []
        for detector in peaklines:
            for each_line in peaklines[detector]:
                currentPeakEntry = each_line.split('\t')
                currentPeakEntry.append(detector)
                assert len(currentPeakEntry) == len(
                    header), 'Invalid Peak Entries'
                tableValues.append(currentPeakEntry)
        df = pd.DataFrame(tableValues, columns=header)
        df = df.replace(r'^\s*$', 'Unknown', regex=True)

        # TODO Can this shape change?
        # assert df.shape[1] == df_size, 'Invalid columns' # TODO: Need this?
        self.PeakTable = df
        return 0

    def assignPeakTables(self):
        pass

    def checkPeaks(self):
        if self.PeakTable.empty:
            # TODO LOG print(f'No peaks in {self.DataFileName}')
            return False
        return True

    def assignMongoDocumentAttributes(self):
        run_dict = self.__dict__.copy()
        for attrib in ['PeakTable', 'entry']:
            run_dict.pop(attrib, None)
        run_dict['id'] = self.hash_
        self.RunDocument = run_dict
        entry_str = '\n'.join([v for v in self.entry])
        self.FileDocument = {'id': self.hash_,
                             'entry': entry_str, 'hash_': self.hash_}
        self.PeakTableDocument = {
            'id': self.hash_, 'PeakTable': self.PeakTable.to_dict('records'),
            'hash_': self.hash_}


class Chromatography_Experiment:

    acids = ['Butyrate', 'Acetate', 'Propionate', 'Isobutyrate',
                      'Isovalerate', 'Isocupric']
    HASHSIZE = 16
    
    def __init__(self, filename: str, file_content: str, instrument: str = 'gc', runall: bool=True, logfile='log.txt'):
        
        self.now = datetime.now().strftime('%d-%b-%Y')
        self.instrument = instrument

        self.filename = filename
        self.file_content = file_content

        self.logfile = logfile
        self.hash_exp = self.assignHash()

        # Below, now sure if we need this
        self.detector = 'example_detector'

        print(f'# ~~~~~ Parsing Chromatography Entries ~~~~~ #')
        # TODO: Try/Except: ValueError
        self.Chromatography_Entries = self.createChromatographyDic()
        print(f'INFO: Created Chromatography Entries\n\n')
        self.SampleNames, self.UnknownNames, self.StandardNames, self.Hashes = self.grabSampleNameList()
        print(f'INFO: Found:\nSamples: {self.SampleNames}\nUnknowns: {self.UnknownNames}\nStandards: {self.StandardNames}\n\n')
        if runall:
            self.standardEntries, self.unknownEntries, self.blankUnknownEntries, self.blankStandardEntries, self.miscEntries = self.grabGCStandardUnknownEntries()
            # TODO: It's okay to run all standards...
            print(f'INFO: Found {len(self.standardEntries)} standard entries and {len(self.unknownEntries)} unknown entries.')

            self.unk_flag = 0 if len(self.unknownEntries) > 0 else 1
            self.std_flag = 0 if len(self.standardEntries) > 0 else 1
            print(f'INFO: unk_flag={self.unk_flag}; std_flag={self.std_flag}')

            self.PeakTable = self.createUnknownPeakTable()
            print('INFO: Peak table finished successfully.')

            print(f'# ~~~ Standard Acid Analysis ~~~ #')
            self.Standards = self.grabStandardAcidValues()
            print('INFO: grabStandardAcidValues finished successfully.')
            self.calculateStandardAcidRegression()
            print('INFO: calculateStandardAcidRegression finished successfully.')
            self.StdPeakTable = self.createStandardPeakTable()
            print(f'INFO: Standard Peak Table finished successfully.')
            print(f'# ~~~ Standard Acid Analysis Complete ~~~ #\n\n')

            print(f'# ~~~ Final Table Cleanup ~~~ #')
            self.FinalTable = self.calculateAppendConcentration()
            print(f'INFO: Final Table finished successfully.')
            self.ModelTable = self.formatModelTable()
            print(f'INFO: Model Table finished successfully.')
            print(f'# ~~~ Success ~~~ #')

    def __str__(self):
        return f'Chromatography_Experiment:\n{self.Chromatography_Entry.keys()}\nEndstring\n'

    def assignHash(self):
        string = f'{self.filename}:{self.now}'
        return base64.b85encode(hashlib.shake_128(
            string.encode('ascii')).digest(self.HASHSIZE)).decode('utf-8')
        # self.hash_ = secrets.token_hex(16)

    def testEntryStart(self, line, open_file):
        while line == " " or line == "\n":
            # line = open_file.readline()
            line = next(line)

        assert line.startswith('[Header]'), ValueError(
            f'testEntryStart failed when finding the start of an entry.')
        return line.strip()

    def readUntilEntryEnd(self, line, open_file):
        entryLines = [line.strip()]
        line = next(line)

        print(f'Next line: {line}')
        while line and not line.startswith('[Header]'):
            entryLines.append(line.strip())
            line = open_file.readline()
        return entryLines, line

    def createChromatographyDic(self):
        rand_suffix = 0
        chromClassEntries = {}
        hash_list = []
        sample_names = []

        # for line in lines:
        print(f'File Content: {self.file_content.strip()}')
        try:
            wild_variable = self.file_content.strip().split('[Header]')[1:]
        except IndexError:
            raise 'GC File did not find the first Header'


        for entry_text in self.file_content.strip().split('[Header]')[1:]:

            entry_lines = ['[Header]'] + entry_text.split('\n')
            currentChromEntry = Chromatography_Entry(
                entry_lines, self.instrument, self.detector)
            hash_value = currentChromEntry.hash_
            sample_name = currentChromEntry.Sample_Name

            if currentChromEntry.complete:
                if hash_value not in hash_list:
                    if sample_name not in sample_names:
                        chromClassEntries[currentChromEntry.Data_File_Name] = currentChromEntry
                    else:
                        currentChromEntry.Sample_Name = f'{sample_name}_{rand_suffix}'
                        chromClassEntries[currentChromEntry.Data_File_Name] = currentChromEntry
                    hash_list.append(hash_value)
                    sample_names.append(sample_name)
                else:
                    print('Found a duplicate entry - not adding to analysis.')
            else:
                pass  # Something to report
            rand_suffix += 1
        return chromClassEntries

    def grabSampleNameList(self):
        samples, unknowns, stds = [], [], []
        hashes = []
        for entry in self.Chromatography_Entries:
            obj = self.Chromatography_Entries[entry]
            samples.append(obj.Sample_Name)
            hashes.append(obj.hash_)
            if obj.Sample_Type == 'Unknown':
                unknowns.append(obj.Sample_Name)
            elif obj.Sample_Type == 'Standards':
                stds.append(obj.Sample_Name)
        samples.sort()
        unknowns.sort()
        stds.sort()
        return samples, unknowns, stds, hashes

    def checkUsefulEntry(self, chromEntry):
        if chromEntry.PeakTable.empty:
            return False
        # if self.column_type in self.gc_columns:
        if self.instrument == 'gc':
            if 'Isocupric' not in chromEntry.PeakTable['Name'].values.tolist():
                return False
        return True

    def grabGCStandardUnknownEntries(self):
        standardEntries = []
        unknownEntries = []
        blankUnknownEntries = []
        blankStandardEntries = []
        miscEntries = []
        for datafile in self.Chromatography_Entries:
            chromEntry = self.Chromatography_Entries[datafile]
            # if chromEntry.Level != 0 and chromEntry.Sample_Type == 'Standard':
            # TODO: Above, give this a warning if they didn't label as standard, perhaps?
            if chromEntry.Level != 0:
                if self.checkUsefulEntry(chromEntry):
                    standardEntries.append(chromEntry)
                else:
                    blankStandardEntries.append(chromEntry)
            elif chromEntry.Level == 0 and chromEntry.Sample_Type == 'Unknown':
                if self.checkUsefulEntry(chromEntry):
                    unknownEntries.append(chromEntry)
                else:
                    blankUnknownEntries.append(chromEntry)
            else:
                miscEntries.append(chromEntry)
        return [standardEntries, unknownEntries,
                blankUnknownEntries, blankStandardEntries, miscEntries]

    def grabStandardAcidValues(self):
        # if self.column_type in self.gc_columns:
        if self.instrument == 'gc':
            return GC_Standard(self.standardEntries, self.hash_exp)
        # elif self.column_type in self.hplc_columns:
        elif self.instrument == 'hplc':
            return HPLC_Standard(self.standardEntries, self.hash_exp)
        else:
            raise ValueError(
                'Do not recognize the chromatography column type.')

    def calculateStandardAcidRegression(self):
        df = self.Standards.DF
        if df.empty:
            self.Standards.Models = None
            self.Standards.ModelPoints = None
            print(f'INFO: Not running calculateStandardAcidRegression due to empty dataframe.')
            return 1

        self.Standards.Models = {}
        self.Standards.ModelPoints = {}
        for acid in df['Name'].unique():
            print(f'\nINFO: Analyzing STANDARD ({acid})')
            if acid.title() not in self.acids:
                print(f'DEBUG: Acid {acid} not in list of acids...skipping')
                continue
            cur_df = df.loc[df['Name'] == acid, [
                'Normalized_Area', 'Concentration']]
            x = cur_df['Concentration'].values.tolist()
            y = cur_df['Normalized_Area'].values.tolist()
            x.insert(0, 0)
            y.insert(0, 0)
            model = linregress(x, y)
            self.Standards.Models[acid] = model
            self.Standards.ModelPoints[acid] = [x, y]
            print(f'Successful loop of {acid}\n')
        return 0

    def formatModelTable(self):
        '''
        Would be nice to have an N in the table for the number of replicates.
        '''
        if self.std_flag != 0 or self.Standards.Models is None:
            return pd.DataFrame()

        header = ['Name', 'Slope', 'Intercept', 'Rvalue',
                  'Pvalue', 'StdErr', 'Int_StdErr', 'hash_exp']
        models = self.Standards.Models
        lines = []
        for acid in models:
            print(f'INFO: Formatting Model Table for {acid}\n')
            m = models[acid]
            line = [acid, m.slope, m.intercept, m.rvalue, m.pvalue, m.stderr,
                    m.intercept_stderr, self.hash_exp]
            lines.append(line)
        df = pd.DataFrame(lines, columns=header)
        return df

    def createUnknownPeakTable(self):
        print(f'INFO: Creating unknown peak table...')
        if self.unk_flag != 0:
            return pd.DataFrame()

        for unknown_entry in self.unknownEntries:
            print(f'INFO: Unknown Processing --> Creating peak table for {unknown_entry.Sample_Name}')
            cur_df = unknown_entry.PeakTable
            cur_df['Sample_Name'] = unknown_entry.Sample_Name
            cur_df['Level'] = unknown_entry.Level
            cur_df['hash_sample'] = unknown_entry.hash_
            cur_df['hash_exp'] = self.hash_exp
            cur_df['Area'] = cur_df['Area'].astype(float, errors='raise')
            # if self.column_type in self.gc_columns:
            if self.instrument == 'gc':
                isocupric_val = cur_df.loc[cur_df['Name']
                                           == 'Isocupric', 'Area'].values[0]
            else:
                isocupric_val = 1
            cur_df['Normalized_Area'] = round(cur_df['Area'] / int(isocupric_val), 3)
            cur_df['Isocupric_Val'] = isocupric_val
            print(f"INFO: Unknown ({unknown_entry.Sample_Name}) Finished.")

        df = pd.concat(
            [v.PeakTable for v in self.unknownEntries], ignore_index=True)
        df = df.rename(columns={'Peak#': 'Peak_Number'})
        return df

    def createStandardPeakTable(self):
        if self.std_flag != 0:
            print(f'Returning empty dataframe!')
            return pd.DataFrame()
        for standard_entry in self.standardEntries:
            # TODO: Filter out duplicate Acids popping up and grab largest?
            standard_entry.PeakTable['Sample_Name'] = standard_entry.Sample_Name
        df = pd.concat([v.PeakTable for v in self.standardEntries])
        df['Area'] = df['Area'].astype(float, errors='raise')
        df['Level'] = df['Level'].astype(int, errors='raise')
        df = df[df.Area != 0]
        df = df.rename(columns={'Peak#': 'Peak_Number'})
        first_columns = ['Level', 'Sample_Name', 'Name', 'Concentration', 'Area']
        new_columns = first_columns + [col for col in df.columns if col not in first_columns]
        df = df[new_columns].sort_values(by=['Level', 'Sample_Name', 'Name'])
        return df

    def calculateAppendConcentration(self):
        if self.unk_flag != 0:
            return pd.DataFrame()
        df = self.PeakTable

        for index, row in df.iterrows():
            acid = row['Name']
            area = float(row['Normalized_Area'])
            try:
                model = self.Standards.Models[acid]
                df.loc[index, 'Concentration'] = round((
                    area - model.intercept) / model.slope, 3)
            except (KeyError, TypeError):
                df.loc[index, 'Concentration'] = None
        first_columns = ['Sample_Name', 'Name', 'Area', 'Isocupric_Val', 'Normalized_Area', 'Concentration']
        new_columns = first_columns + [col for col in df.columns if col not in first_columns]
        df = df[new_columns].sort_values(by=['Sample_Name', 'Name'])

        return df

    def report(self, save=False):
        if save:
            self.write_final_out()
        return {
            'type': 'GCFile',  # 'HPLCFile
            'report': {
                'FinalTable': self.FinalTable.to_dict(orient='records'),
                'StdPeakTable': self.StdPeakTable.to_dict(orient='records'),
                'ModelTable': self.ModelTable.to_dict(orient='records'),
                'Standards': self.Standards.MeanDF.to_dict(orient='records'),
            },
        }

    def write_final_out(self):
        output_path = f'./output-{self.now}'
        if not os.path.exists(output_path):
            print(f'\nCreating path...{output_path}\n\n')
            os.makedirs(output_path)
        self.FinalTable.to_csv(f'{output_path}/FinalTable-{self.now}.csv', index=False)
        self.StdPeakTable.to_csv(f'{output_path}/StdPeakTable-{self.now}.csv', index=False)
        self.ModelTable.to_csv(f'{output_path}/ModelTable-{self.now}.csv', index=False)
        self.Standards.MeanDF.to_csv(f'{output_path}/StandardsMeanDF-{self.now}.csv', index=False)


class GC_Standard:

    def __init__(self, standardEntries, hash_exp):
        self.now = datetime.now().strftime('%d-%b-%Y')
        self.standardEntries = standardEntries
        self.hash_exp = hash_exp
        self.AcidConcentrations = {'Acetate': [7.5, 15, 30, 60, 120],
                                   'Propionate':  [1.875, 3.75, 7.5, 15, 30],
                                   'Isobutyrate': [0.9375, 1.875, 3.75, 7.5, 15],
                                   'Butyrate':    [1.875, 3.75, 7.5, 15, 30],
                                   'Isovalerate': [0.9375, 1.875, 3.75, 7.5, 15],
                                   'Isocupric':   [0.998, 0.999, 1, 1.001, 1.002]}
        self.acceptableAcids = ['Acetate', 'Propionate', 'Isobutyrate',
                                'Isovalerate', 'Butyrate', 'Isocupric']
        if len(self.standardEntries) == 0:
            self.DF = pd.DataFrame()
            self.MeanDF = pd.DataFrame()
            self.acidList = None
            # TODO: Log that there was no standard found
            # raise ValueError(
            #     f'No standards found in this file! Unable to calculate concentration.')
        else:
            self.checkAllAcidsInStandards()
            print(f'INFO: Acid check is complete.\n\n')
            assert len(self.standardEntries) > 3, ValueError(
                'Less than 3 standards passed.')
            df = self.createStandardTable()
            first_columns = ['Level', 'Sample_Name', 'Name', 'Area', 'Isocupric_Val', 'Normalized_Area', 'Concentration']
            new_columns = first_columns + [col for col in df.columns if col not in first_columns]
            self.DF = df[new_columns].sort_values(by=['Sample_Name', 'Name'])
            self.MeanDF = self.DF.groupby(['Name', 'Level', 'Concentration']).agg(
                {'Area': ['mean', 'std', 'count']}).reset_index()
            self.acidList = self.MeanDF['Name'].unique()
            print(f'# ~~~ INFO: GC_Standard init complete ~~~ #\n\n')

    def checkAllAcidsInStandards(self):
        # TODO: Make this more robust
        for idx, standardEntry in enumerate(self.standardEntries):
            SPT = standardEntry.PeakTable
            if all(acid in SPT['Name'].tolist() for acid in self.acceptableAcids):
                pass
            else:
                print(f'{standardEntry} does not contain all standard acids.')
                print(f'Removing the standard from further analysis...')
                self.standardEntries.pop(idx)
                # raise IndexError(
                #     f"GC Standard entry does not contain all acids!")
        # TODO: If not at least 1 of each Standard Entry (or some other number)
        # then do not add concentration information.

    def createStandardTable(self):
        acid_data = []
        for standardEntry in self.standardEntries:
            SPT = standardEntry.PeakTable
            SPT['Area'] = SPT['Area'].astype('int')
            SPT['Sample_Name'] = standardEntry.Sample_Name
            SPT['Level'] = standardEntry.Level
            isocupric_val = SPT.loc[SPT['Name']
                                    == 'Isocupric']['Area'].values[0]
            SPT['hash_sample'] = standardEntry.hash_
            SPT['hash_exp'] = self.hash_exp
            SPT['Isocupric_Val'] = isocupric_val
            SPT['Normalized_Area'] = round(SPT['Area'] / int(isocupric_val), 3)
            SPT['Concentration'] = ''

            for acid in SPT['Name']:
                if acid in self.acceptableAcids:
                    lvl = int(standardEntry.Level)
                    conc = round(self.AcidConcentrations[acid][lvl - 1], 3)
                    SPT.loc[SPT['Name'] == acid, 'Concentration'] = conc

            acid_data.append(SPT)
        return pd.concat(acid_data).reset_index()


class HPLC_Standard:

    def __init__(self, standardEntries, hash_exp):
        self.standardEntries = standardEntries
        self.hash_exp = hash_exp
        self.AcidConcentrations = {'Fructose': [10, 50, 100, 250, 500],
                                   'Glucose': [10, 50, 100, 250, 500],
                                   'Sucrose': [10, 50, 100, 250, 500],
                                   'Kestone': [10, 50, 100, 250, 500],
                                   'Maltose': [10, 50, 100, 250, 500],
                                   'Maltotriose': [10, 50, 100, 250, 500],
                                   'Kestose': [10, 50, 100, 250, 500],
                                   'Xylose': [10, 50, 100, 250, 500],
                                   'Rhamnose': [10, 50, 100, 250, 500]}
        if len(self.standardEntries) == 0:
            self.DF = pd.DataFrame()
            self.MeanDF = pd.DataFrame()
            self.acidList = None
            print(f'Returning all empty standard data.')
        else:
            self.DF = self.createStandardTable()
            if not self.DF.empty:
                self.MeanDF = self.DF.groupby(['Name', 'Level', 'Concentration']).agg(
                    {'Area': ['mean', 'std']}).reset_index(level=0)
                self.acidList = self.MeanDF['Name'].unique()
            else:
                # TODO: Support here
                print(f'Error matching acids up to standards, hmm... :-(')
                self.MeanDF = pd.DataFrame()
                self.acidList = None

    def createStandardTable(self):
        normalization_val = 1
        acid_data = []
        for standardEntry in self.standardEntries:
            SPT = standardEntry.PeakTable
            SPT['Area'] = SPT['Area'].astype('int')
            SPT['Sample_Name'] = standardEntry.Sample_Name

            acid = self.chooseAcid(standardEntry.Sample_Name)
            # Support for acid not found where it should be
            if acid not in SPT['Name'].values:
                # print(
                #     f'Acid ({acid}) not found in sample {standardEntry.Sample_Name}')
                continue

            cur_entry = SPT.loc[SPT['Name'] == acid].values[0].tolist()
            lvl = standardEntry.Level
            cur_entry.append(lvl)
            cur_entry.append(standardEntry.hash_)
            cur_entry.append(self.hash_exp)
            # Below, adding this pseudo value to match GC standard
            # SPT['Normalized_Area'] = SPT['Area'] / normalization_val
            norm_area = SPT.loc[SPT['Name'] == acid,
                                'Area'].values[0] / normalization_val
            cur_entry.append(norm_area)

            lvlConc = self.AcidConcentrations[acid][lvl - 1]
            cur_entry.append(lvlConc)
            acid_data.append(cur_entry)
        columns = SPT.columns.tolist() + \
            ['Level', 'hash_sample', 'hash_exp',
                'Normalized_Area', 'Concentration']
        if len(acid_data) == 0:
            print(f'Did not match acids to their tables :-(')
            return pd.DataFrame()
        return pd.DataFrame(acid_data, columns=columns).reset_index(drop=True)

    def chooseAcid(self, name):
        if name.startswith('Fru'):
            return 'Fructose'
        if name.startswith('Glc'):
            return 'Glucose'
        if name.startswith('Suc'):
            return 'Sucrose'
        if name.startswith('Mal0'):
            return 'Maltose'
        if name.startswith('Mal30'):
            return 'Maltotriose'
        if name.startswith('Kes'):
            return 'Kestose'
        if name.startswith('Xyl'):
            return 'Xylose'
        if name.startswith('Rha'):
            return 'Rhamnose'

        return 'UnknownStandard'


if __name__ == "__main__":
    def parse_args():
        parser = argparse.ArgumentParser(description="Parser")
        parser.add_argument("-f", "--File",
                            help="GC/HPLC Text File",
                            required=True)
        parser.add_argument("-i", "--Instrument",
                            help="Instrument",
                            required=False, default='gc')
        parser.add_argument("-s", "--Save",
                            help="Save tables",
                            default=False, action='store_true')
        return parser

    parser = parse_args()
    args = parser.parse_args()
    file = Path(args.File).expanduser().absolute()

    process_chromatography_file(file, args.Instrument, savefile=args.Save)
