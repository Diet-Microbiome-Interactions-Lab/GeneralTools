
'''
This script is a general tool used to detect statistically significant
rows. ADD TO THIS
'''
import argparse
import json
import random
import time

import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import linregress


# Step 1 - Create a class to read in this file
class Abundance:

    __allowed = ("Input", "Output", "PValue", "Plot",
                 "Family", "Genus", "MAG", "KO")

    def __init__(self, **kwargs):
        # Take care of kwargs
        for k, v in kwargs.items():
            assert(k in self.__class__.__allowed), print(f"Error: {k}")
            setattr(self, k, v)

        # Init X
        self.time_x = [0, 0, 0] + [24] * 14 + [48] * 14
        self.sampling_x = ['0'] * 3 + ['Blank', 'Blank'] + \
            ['FOS', 'FOS'] + \
            ['Supernatant'] * 7 + ['Particle'] * 7 + \
            ['Supernatant'] * 7 + ['Particle'] * 7
        self.size_x = [180, 250, 300, 500, 850, 1000, 1700] * 4

        # Read in and subset dataframe
        self.df = pd.read_csv(self.Input, sep='\t')
        df_index = list(range(1, 36, 1)) + [38, 39, 40, 42]
        filt_df = self.df.iloc[:, df_index]
        if self.Family:
            filt_df = filt_df.loc[filt_df['Family'] == self.Family, ]
        if self.Genus:
            filt_df = filt_df.loc[filt_df['Genus'] == self.Genus, ]
        if self.MAG:
            filt_df = filt_df.loc[filt_df['MAG'] == self.MAG, ]
        if self.KO:
            filt_df = filt_df.loc[filt_df['KO'] == self.KO, ]
        self.filtered_df = filt_df
        self.total = len(self.filtered_df.index)

        self.OutputTemplate = {
            'Analysis': '',
            'Total': 0,
            'Signficant Proportion': 0,
            'MAG': {},
            'Family': {},
            'Genus': {},
            'KO': {},
        }

    @staticmethod
    def randomColor():
        return (random.random(), random.random(), random.random())

    def addheader(self, value):
        return [v for v in [value, self.Family, self.Genus, self.MAG, self.KO] if v]

    def passThreshold(self, linregressObj):
        '''
        Test a lingregress object for significance
        '''
        if linregressObj.pvalue < self.PValue:
            return True
        else:
            return False

    def reportSignificant(self, diction, line, regression):
        '''
        '''
        fam, gen, ko, mag = line

        diction['KO'].setdefault(ko, {'+': 0, '-': 0})
        diction['MAG'].setdefault(mag, {'+': 0, '-': 0})
        diction['Family'].setdefault(fam, {'+': 0, '-': 0})
        diction['Genus'].setdefault(gen, {'+': 0, '-': 0})

        if regression.slope > 0:
            diction['KO'][ko]['+'] += 1
            diction['MAG'][mag]['+'] += 1
            diction['Family'][fam]['+'] += 1
            diction['Genus'][gen]['+'] += 1
        else:
            diction['KO'][ko]['-'] += 1
            diction['MAG'][mag]['-'] += 1
            diction['Family'][fam]['-'] += 1
            diction['Genus'][gen]['-'] += 1

        return 0

    def plotValues(self, x, y):
        '''
        Plot values
        '''
        plt.scatter(x=x, y=y, color=self.randomColor(), alpha=0.25)

        return 0

    def analyze_time(self):
        '''
        Read in the file as a pandas dataframe and output subsets
        corresponding to various categorical analysis
        '''
        self.Time = self.OutputTemplate.copy()
        self.Time['Analysis'] = self.addheader('Time')
        sig = 0
        for index, row in self.filtered_df.iterrows():
            time_y = row.tolist()[0:31]
            # Test if line passes threshold to test
            line = row.tolist()[-4:]
            timeReg = linregress(self.time_x, time_y)
            if self.passThreshold(timeReg):
                sig += 1
                self.reportSignificant(self.Time, line, timeReg)
            else:
                continue
            if self.Plot:
                self.plotValues(self.time_x, time_y)

        if self.Plot:
            plt.title(
                '-'.join([v for v in ['Time', self.Family, self.Genus,
                                      self.MAG, self.KO] if v]))
            plt.show()

        self.Time['Total'] = self.total
        try:
            self.Time['Signficant Proportion'] = sig / self.total
        except ZeroDivisionError:
            self.Time['Signficant Proportion'] = "0 results found!"

        return self.Time

    def analyze_size(self):
        '''
        Analyze size values
        '''
        self.Size = self.OutputTemplate.copy()
        self.Time['Size'] = self.addheader('Size')
        sig = 0
        for index, row in self.filtered_df.iterrows():
            size_y = row.tolist()[7:35]
            line = row.tolist()[-4:]
            sizeReg = linregress(self.size_x, size_y)
            if self.passThreshold(sizeReg):
                sig += 1
                self.reportSignificant(self.Size, line, sizeReg)
            if self.Plot:
                self.plotValues(self.size_x, size_y)

        if self.Plot:
            plt.title(
                '-'.join([v for v in ['Size', self.Family, self.Genus,
                                      self.MAG, self.KO] if v]))
            plt.show()

        self.Size['Total'] = self.total
        try:
            self.Size['Signficant Proportion'] = sig / self.total
        except ZeroDivisionError:
            self.Size['Signficant Proportion'] = "0 results found!"

        return self.Size

    def analyze_sampling(self):
        '''
        Analyze sampling values
        '''
        self.Sampling = self.OutputTemplate.copy()
        self.Sampling['Analysis'] = self.addheader('Sampling')
        sig = 0
        for index, row in self.filtered_df.iterrows():
            sampling_y = row.tolist()[:35]
            line = row.tolist()[-4:]

            # Get coefficients
            zero = sum(sampling_y[0:3]) / 3
            sampling_y_adjusted = [val - zero for val in sampling_y]
            # New X and Y axis for testing
            reg_sampling_x = [0] * 7 + [1] * 7 + [0] * 7 + [1] * 7
            reg_sampling_y = sampling_y_adjusted[7:]

            # Test regression
            samplingReg = linregress(reg_sampling_x, reg_sampling_y)
            if self.passThreshold(samplingReg):
                sig += 1
                self.reportSignificant(self.Sampling, line, samplingReg)

            if self.Plot:
                self.plotValues(reg_sampling_x, reg_sampling_y)

        if self.Plot:
            plt.title(
                '-'.join([v for v in ['Sampling', self.Family, self.Genus,
                                      self.MAG, self.KO] if v]))
            plt.show()

        self.Sampling['Total'] = self.total
        try:
            self.Sampling['Signficant Proportion'] = sig / self.total
        except ZeroDivisionError:
            self.Sampling['Signficant Proportion'] = "0 results found!"

        return self.Sampling


if __name__ == '__main__':
    start_time = time.time()

    def parse_args():
        parser = argparse.ArgumentParser(description="Parser")
        parser.add_argument("-i", "--Input",
                            help="Input abundance file", required=True,
                            default='CHANGEME.txt')
        parser.add_argument("-p", "--PValue",
                            help="P-value threshold", required=False,
                            default=0.05)
        parser.add_argument("-f", "--Family",
                            help="Family", required=False,
                            default=False)
        parser.add_argument("-g", "--Genus",
                            help="Genus", required=False,
                            default=False)
        parser.add_argument("-m", "--MAG",
                            help="MAG", required=False,
                            default=False)
        parser.add_argument("-k", "--KO",
                            help="KO Number", required=False,
                            default=False)
        parser.add_argument("-z", "--Plot",
                            help="Make a plot!", required=False,
                            action='store_true', default=False)
        parser.add_argument("-o", "--Output",
                            help="Output prefix to write summary to (JSON format)",
                            required=True, default=False)
        return parser

    parser = parse_args()
    args = vars(parser.parse_args())

    # Init the class
    myclass = Abundance(**args)
    time_ = myclass.analyze_time()
    with open(f"{args['Output']}-Time.json", 'w') as out:
        out.write(json.dumps(time_))
    size_ = myclass.analyze_size()
    with open(f"{args['Output']}-Size.json", 'w') as out:
        out.write(json.dumps(size_))
    sampling_ = myclass.analyze_sampling()
    with open(f"{args['Output']}-Sampling.json", 'w') as out:
        out.write(json.dumps(sampling_))

    # Get the time
    print(time.time() - start_time)
