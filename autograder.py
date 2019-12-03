import output_validator as ov
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
import pickle
import input_validator
from datetime import datetime

# Set true for multi-core enhancement.
import multiprocessing
from multiprocessing import Pool
from multiprocessing import Array
from multiprocessing import Manager
MULTICORE = True
num_thread = multiprocessing.cpu_count()
VERBOSE = False

def validate_all_outputs(input_directory, output_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, '.in')
    output_files = utils.get_files_with_extension(output_directory, '.out')

    i = 0
    all_results = []
    all_baseline = []
    all_baseline = pickle.load(open("baselineCosts.p", "rb"))
    if not MULTICORE:
        inputs = Manager().list()
        for input_file in input_files:
            _outputCost(input_file, output_files, output_directory, all_baseline, i, all_results, inputs)
            i += 1
        final_score = "Graded " + str(len(all_results)) +  " results with a score of: " + str(100 / len(all_results) * sum(all_results))
        print(final_score)
        a = open(str(datetime.now()).split(".")[0].replace(":","-")+".log", "w")
        for r in all_results:
            a.write(str(r) + "\n")
        a.write("\n")
        for inp in inputs:
            a.write(str(inp) + "\n")
        a.write(final_score)
        a.close()
        return all_results
    else:
        print("MULTICORE IN PROCESS. DO NOT CONTROL-C.")
        all_results = Manager().list()
        inputs = Manager().list()
        tasks = []
        i = 0
        for input_file in input_files:
            tasks.append((input_file, output_files, output_directory, all_baseline, i, all_results, inputs))
            i += 1
        pool = Pool(num_thread - 1)
        results = [pool.apply_async(_outputCost, t) for t in tasks]
        pool.close()
        pool.join()
        final_score = "Graded " + str(len(all_results)) +  " results with a score of: " + str(100 / len(all_results) * sum(all_results))
        print(final_score)
        a = open(str(datetime.now()).split(".")[0].replace(":","-")+".log", "w")
        for r in all_results:
            a.write(str(r) + "\n")
        a.write("\n")
        for inp in inputs:
            a.write(str(inp) + "\n")
        a.write(final_score)
        a.close()
        return all_results
    #pickle.dump(all_baseline, open( "baselineCosts.p", "wb" )) #Cache results

def _outputCost(input_file, output_files, output_directory, all_baseline, i, all_results, inputs=[]):
    output_file = utils.input_to_output(input_file, output_directory).replace("\\", "/")
    if output_file not in output_files:
        print(f'No corresponding .out file for {input_file}')
        results = (None, None, f'No corresponding .out file for {input_file}')
    else:
        cost = ov.validate_output(input_file, output_file, verbose=VERBOSE)[1]
        #baselineCost = ov.validate_output(input_file, "./baseline_outputs/" + output_file.split("/")[-1])[1]
        baselineCost = all_baseline[i]
        #all_baseline.append(baselineCost)
        if type(cost) is str:
            raise Exception("<-- CUSTOM ERROR --> Solver output is string: " + cost)
        results = cost / baselineCost
        print("Input: ", input_file, "\t Results: ", results)
        all_results.append(min(results, 1))
        inputs.append(input_file)
        return min(results, 1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the output validator is run on all files in the output directory. Else, it is run on just the given output file')
    parser.add_argument('--disableMulticore', action='store_true', help='Disable autograder multicore')
    parser.add_argument('-v', action='store_true', help='Verbose output')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('output', type=str, help='The path to the output file or directory')
    #parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    if args.disableMulticore:
        MULTICORE = False
    if args.v:
        VERBOSE = True
    if args.all:
        input_directory, output_directory = args.input, args.output
        validate_all_outputs(input_directory, output_directory)
    else:
        input_file, output_file = args.input, args.output
        cost = ov.validate_output(input_file, output_file, verbose=VERBOSE)[1]
        baselineCost = ov.validate_output(input_file, "./baseline_outputs/" + output_file.split("/")[-1], verbose=VERBOSE)[1]
        if type(cost) is str:
            raise Exception("<-- CUSTOM ERROR --> Solver output is string: " + cost)
        print(cost / baselineCost)
