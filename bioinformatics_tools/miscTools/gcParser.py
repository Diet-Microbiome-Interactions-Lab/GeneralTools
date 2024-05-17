'''
Author: Dane
Date: 10Dec20
Modified: 06Jan21
Purpose: Program designed to automate GC analysis
Outline:
i.) Read each GC file from a directory into a 'GC' object.
ii.) Given a set of GC objects, run calc_standard_curve() to infer
which samples are standards and calculate standard curves
iii.) Given the standard information, compare each sample to the
standards and match them each curve to the known acid. Next, normalize
these values.
iv.) Calculate SCFA concentrations by comparing samples to the
standard curve.

Dependencies:
-matplotlib
-numpy
-scipy
-shapely

Example usage:
$ python gcParser.py --Directory <path/to/GC/files> --WindowSize 3000 \
--MinHeight 30 --NumWindows 2 --Verbose
'''
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from shapely.geometry import Polygon


class GC:
    def __init__(self, file, L, m, n):
        self.name = file
        self.sample = os.path.basename(os.path.splitext(self.name)[0])
        self.condition = os.path.basename(file).split('-')[0]
        self.number = self.sample.split('-')[1].split('.')[0][:-1]
        self.replicate = self.sample.split('-')[1].split('.')[0][-1]
        self.x, self.y = self.get_coordinates()
        self.forward_slopes = self.find_slope(L, m, n)
        self.reverse_slopes = self.find_slope(L, m, n, reverse=True)
        self.acid_list = ['Acetate', 'Propionate', 'Isobutyrate',
                          'Butyrate', 'Isovalerate', 'Internal']
        self.acid_concs = {'Acetate':     [7.5, 15, 30, 60, 120],
                           'Propionate':  [1.875, 3.75, 7.5, 15, 30],
                           'Isobutyrate': [0.9375, 1.875, 3.75, 7.5, 15],
                           'Butyrate':    [1.875, 3.75, 7.5, 15, 30],
                           'Isovalerate': [0.9375, 1.875, 3.75, 7.5, 15],
                           'Internal':    [0.998, 0.999, 1, 1.001, 1.002]}
        self.AUCs, self.Peaks = self.calc_AUCs()

    def get_coordinates(self):
        '''
        Simply capture the x and y values from the file.
        '''
        x = []
        y = []
        with open(self.name) as i:
            line = i.readline().strip()
            while line:
                time = line.split('\t')[0]
                value = line.split('\t')[1]
                x.append(float(time))
                y.append(float(value))
                line = i.readline().strip()
        return x, y

    def compute_slopes(self, x, y, L, m, n, reverse=False):
        '''
        Computing slopes is a function dependent on 3 parameters:
        L: length of the sliding window.
        m: minimal height (relative to baseline) the slope must exceed.
        n: number of increasing sliding windows in a row to record
        the start of a slope.
        '''
        if reverse:
            x.reverse()
            y.reverse()
        moving_up = False
        slope_starts = []
        slope_coords = []

        start_value = 0
        start = y[0]
        running_total = 0

        for i in range(0, len(x) - (L - 1), L):
            mean = sum(y[i:i + L]) / L  # L tunes sensitivity as well
            if mean > (start + m):  # Tuning sensitivity param
                if not moving_up:
                    running_total += 1
                    if running_total == 1:
                        start_value = x[i]  # Capture initial incline/decline
                        start_coord = i
                    elif running_total > n:  # n tunes how fast slope goes up
                        slope_starts.append(start_value)
                        slope_coords.append(start_coord)
                        moving_up = True
                else:
                    pass
            else:
                moving_up = False
                running_total = 0
            start = mean

        if reverse:
            slope_starts.reverse()
            slope_coords.reverse()
            for cnt, val in enumerate(slope_coords):
                new_val = len(x) - val
                slope_coords[cnt] = new_val
        return [slope_starts, slope_coords]

    def find_slope(self, L, m, n, reverse=False):
        '''
        Return the list of lists: [[slope_starts], [slope_coords]]
        where starts = time and coords = index
        '''
        x, y = self.x, self.y

        slopes = self.compute_slopes(
            x, y, L, m, n, reverse)
        return slopes

    def calc_AUCs(self):
        '''
        Return 2 dictionaries giving AUC information.
        AUC_Dic = {
                   str(startCoord-endCoord): float(AUC)
                   }
        Acid_Dic = {
                    Acetate: [AUC, str(start_val), str(end_val), #Stand
                              str(start_coord), str(end_coord)],
                    0:       [AUC, str(start_val), str(end_val), #Sample
                              str(start_coord), str(end_coord)]
                   }
        '''
        acids = self.acid_list
        starts = self.forward_slopes
        ends = self.reverse_slopes

        start_index = sorted(starts[1])
        end_index = sorted(ends[1])
        self.x.reverse()
        self.y.reverse()

        AUC_Dic = {}
        Acid_Dic = {}

        if self.condition == 'Standard':
            for acid, start_val, end_val in zip(acids, start_index, end_index):
                x_range = self.x[start_val:end_val]
                y_range = self.y[start_val:end_val]
                auc_input = [(x, y) for x, y in zip(x_range, y_range)]
                polygon = Polygon(auc_input)

                key = f"{start_val}-{end_val}"
                auc = polygon.area
                AUC_Dic[key] = auc
                Acid_Dic[acid] = [auc, start_val, end_val,
                                  self.x[start_val], self.x[end_val]]
        elif self.condition == 'Sample':
            for cnt, (start_val, end_val) in enumerate(zip(start_index, end_index)):
                x_range = self.x[start_val:end_val]
                y_range = self.y[start_val:end_val]
                auc_input = [(x, y) for x, y in zip(x_range, y_range)]
                polygon = Polygon(auc_input)

                key = f"{start_val}-{end_val}"
                auc = polygon.area
                AUC_Dic[key] = auc
                Acid_Dic[cnt] = [auc, start_val, end_val,
                                  self.x[start_val], self.x[end_val]]

        return AUC_Dic, Acid_Dic


def calc_standard_curve(filepath):
    '''
    Go through a directory and extract all standard files
    and add to a list.
    '''
    standards = []

    std_levels = set()
    for file in os.listdir(filepath):
        if file.endswith('.txt'):
            full_name = os.path.join(filepath, file)
            gc = GC(full_name, 30, 5000, 2)
            if gc.condition == 'Standard':
                standards.append(gc)
                std_levels.add(gc.number)

    acid_list = gc.acid_list  # Grab the acid list for down the road
    acid_concs = gc.acid_concs

    # Loop through each standard level and create the mean
    master_dic = {}
    std_levels = sorted(list(std_levels))  # Going from 1-5 in increasing
                                           # order makes more sense
    for level in std_levels:
        _dic = {}
        cnt = 0
        for gc in standards:
            if gc.number == level:
                cnt += 1  # This keeps track of how many replicates
                for acid in gc.Peaks.keys():
                    if acid in _dic:
                        _dic[acid] += gc.Peaks[acid][0]
                    else:
                        _dic[acid] = gc.Peaks[acid][0]
            else:
                pass
        # Now get the mean of each acid
        _dic = {k: v / cnt for k, v in _dic.items()}
        master_dic[level] = _dic

    # Lastly, calculate the standard curve from the n points
    raw_regression_dic = {}
    for level in master_dic.keys():
        for acid in acid_list:
            if acid in raw_regression_dic:
                raw_regression_dic[acid].append(master_dic[level][acid])
            else:
                raw_regression_dic[acid] = [master_dic[level][acid]]

    # Repeat the above but with start and stop of curves
    _start = {}
    _end = {}
    cnt = 0
    for gc in standards:
        cnt += 1  # This keeps track of how many replicates
        for acid in gc.Peaks.keys():
            if acid in _start:
                _start[acid] += gc.Peaks[acid][3]
                _end[acid] += gc.Peaks[acid][4]
            else:
                _start[acid] = gc.Peaks[acid][3]
                _end[acid] = gc.Peaks[acid][4]
    # Now get the mean of each acid
    _start = {k: v / cnt for k, v in _start.items()}
    _end = {k: v / cnt for k, v in _end.items()}

    # Lastly, find regression line for each SCFA
    regression_dic = {}
    norm_regression_dic = {}
    mean_internal = sum(
        raw_regression_dic['Internal']) / len(raw_regression_dic['Internal'])
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'violet']

    def objective(xvals, a, b):  # Removed arg 'c'
        return [a * x + b for x in xvals]
        # return [a * x + b * x**2 + c for x in xvals]

    for cnt, acid in enumerate(raw_regression_dic.keys()):
        # print(f"Acid:\t{acid}\n\n")
        norm_regression_dic[acid] = [(val / mean_internal)
                                      for val in raw_regression_dic[acid]]
        # print(norm_regression_dic)
        x = sorted(norm_regression_dic[acid])
        # x = list(range(1, len(y) + 1))
        y = acid_concs[acid]
        # print(len(y))
        # model = np.polyfit(x, y, 1)
        # All STUFF FOR PLOTTING
        model, _ = curve_fit(objective, x, y)
        # print(model)
        a, b = model
        # print(f"A: {a}, B: {b}, C: {c}")
        x_line = np.arange(min(x), max(x), 0.01)
        y_line = objective(x_line, a, b)
        plt.scatter(x, y, label=acid, color=colors[cnt])  # Here
        # reg = [(val*model[0] + model[1]) for val in x]
        plt.plot(x_line, y_line, label=acid, color = colors[cnt], linestyle='--')  # Here
        plt.xlabel(f"Normalized Standard Level (via internal standard)")
        plt.ylabel(f"{acid} (mM)")
        plt.title(f"Standard Curve for {acid}")
        plt.legend()
        plt.savefig(f"{acid}_standard_curve.png")
        plt.close()
        # ALL STUFF FOR PLOTTING
        regression_dic[acid] = model

    return raw_regression_dic, _start, _end, norm_regression_dic, regression_dic


def match_sample_to_standard(gcClassObject):
    '''
    Match sample peaks to an acid based on the standard
    '''
    obj = gcClassObject
    peaks = obj.Peaks
    std_starts = obj.standard_data[1]

    matched_peaks = {}
    # Go through each peak and get distance to closest in standard
    for peak in peaks.keys():
        # Now check this peak for distance against all std peaks
        prev_diff = 100
        acid_match = None
        for std_peak in std_starts.keys():
            current_diff = abs(peaks[peak][3] - std_starts[std_peak])
            if (current_diff < prev_diff and current_diff < 0.25):  # ADD THRESHOLD
                prev_diff = current_diff
                acid_match = std_peak
        # Compile a new dictionary of values matching to the standard
        if acid_match:
            matched_peaks[acid_match] = peaks[peak]

    return matched_peaks


def normalize_aucs(gcClassObject):
    '''
    Normalize each AUC by dividing each acid by the internal standard
    '''
    obj = gcClassObject
    peaks = obj.peak_matches

    norm_peaks = peaks
    # Loop and normalize each peak
    for acid in peaks.keys():
        norm_auc = peaks[acid][0] / peaks['Internal'][0]
        norm_peaks[acid][0] = norm_auc
    return norm_peaks


def calculate_measurement(gcClassObject):
    '''
    Given a standard curve and normalized AUC value, calculate the
    concentration of a SCFA
    '''
    obj = gcClassObject
    normalized_peaks = obj.normalized_peak_matches
    regression_dic = obj.standard_data[4]
    # print(f"Normalized Peaks:\n{normalized_peaks}")
    # print(regression_dic)

    # def objective(x, a, b, c):
    #     return [a * x + b * x**2 + c]
    def objective(x, a, b):
        return [a * x + b]

    normalized_concentrations = {}
    # Go through and put each value into a dictionary
    # The error is I'm saying given a , what's the likely AUC
    # Instead, I need to get AUC
    for npeak in normalized_peaks.keys():
        a, b = regression_dic[npeak]
        # value = (normalized_peaks[npeak][0] *
        #          regression_dic[npeak][0]) + regression_dic[npeak][1]
        value = objective(normalized_peaks[npeak][0], a, b)
        # print('Values')
        # print(f"{normalized_peaks[npeak][0]}: {npeak}\t{value}\n")
        normalized_concentrations[npeak] = value
    return normalized_concentrations


def main(filepath, L, m, n, verbose=False):
    '''
    Go through a directory and make GC objects for each Sample and
    add attributes by comparisong to Standards
    '''
    sampleList = []
    count = 0
    # Get standard information
    standard_data = calc_standard_curve(filepath)

    for file in os.listdir(filepath):
        if file.endswith('.txt'):
            full_name = os.path.join(filepath, file)
            gc = GC(full_name, L, m, n)
            if gc.condition == 'Sample':
                gc.standard_data = standard_data
                if (count == 0 and verbose):  # Only print this once!
                    print(f"Standard data for this batch:\nFormat:\n\
Acid: [rawAUC_Std1, rawAUC_Std2, ..., rawAUC_StdN]\n\
Acid1: [SlopeStart], Acid2: [SlopeStart], ...\n\
Acid1: [SlopeEnd], Acid2: [SlopeEnd], ...\n\
Acid: [normAUC_Std1, normAUC_Std2, ..., normAUC_StdN]\n\
Acid1: [RegressionEquation], Acid2: RegressionEquation, ...\n")
                    print(f"{gc.standard_data}\n")
                    print(f"|-----Starting Sample Analysis-----|\n")
                    count += 1
                gc.peak_matches = match_sample_to_standard(gc)
                gc.normalized_peak_matches = normalize_aucs(gc)
                gc.normalized_measurements = calculate_measurement(gc)
                sampleList.append(gc)
                if verbose:
                    print(f"Analyzing sample: --{gc.name}--")
                    print(f"Condition of the sample: --{gc.condition}--\n")
                    print("Sample peak data: [[Timepoint],[Index]]")
                    print(f"Forward: {gc.forward_slopes}")
                    print(f"Reverse: {gc.reverse_slopes}")
                    # Moving on
                    print('\nPeaks: [raw AUC, IndexStart, IndexEnd, TimeStart, TimeEnd\n')
                    print(gc.Peaks)
                    print('Peak matches:')
                    print(gc.normalized_peak_matches)
                    print('\nNormalized peaks:')
                    print(gc.normalized_peak_matches)
                    print('\nNormalized Concentrations:')
                    print(gc.normalized_measurements)
                    print(f"\n|-----Done with sample analysis-----|\n\n\n")

    return 0


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("-d", "--Directory",
                        help="Location of all raw GC files - (Tab-delim)",
                        required=True)
    parser.add_argument("-w", "--WindowSize",
                        help="Size of the sliding window for peak calling",
                        required=False, default=30)
    parser.add_argument("-m", "--MinHeight",
                        help="Minimum height (relative to baseline) or a peak",
                        required=False, default=3000)
    parser.add_argument("-n", "--NumWindows",
                        help="Number of increasing windows to call a peak",
                        required=False, default=2)
    parser.add_argument("-v", "--Verbose",
                        help="Provide verbose results to the stdout",
                        required=False, default=False, action='store_true')
    argument = parser.parse_args()
    main(argument.Directory, argument.WindowSize,
         argument.MinHeight, argument.NumWindows,
         argument.Verbose)
