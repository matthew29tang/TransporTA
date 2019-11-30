import output_validator as ov
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
import pickle
import input_validator

# Set true for multi-core enhancement.
import multiprocessing
from multiprocessing import Pool
from multiprocessing import Array
from multiprocessing import Manager
MULTICORE = True
num_thread = multiprocessing.cpu_count()

def validate_all_outputs(input_directory, output_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, '.in')
    output_files = utils.get_files_with_extension(output_directory, '.out')

    i = 0
    all_results = []
    all_baseline = pickle.load(open("baselineCosts.p", "rb"))
    if not MULTICORE:
        for input_file in input_files:
            _outputCost(input_file, output_files, output_directory, all_baseline, i, all_results)
            i += 1
        print("Total results: ", str(100 / 949 * sum(all_results)))
        return all_results
    else:
        print("MULTICORE IN PROCESS. DO NOT CONTROL-C.")
        all_results = Manager().list() #Array('d', [])
        tasks = []
        i = 0
        for input_file in input_files:
            tasks.append((input_file, output_files, output_directory, all_baseline, i, all_results))
            i += 1
        pool = Pool(num_thread - 1)
        results = [pool.apply_async(_outputCost, t) for t in tasks]
        pool.close()
        pool.join()
        print("Total results: ", str(100 / 949 * sum(all_results)))
        return all_results
    # pickle.dump(all_baseline, open( "baselineCosts.p", "wb" )) Cache results    

def _outputCost(input_file, output_files, output_directory, all_baseline, i, all_results):
    output_file = utils.input_to_output(input_file, output_directory).replace("\\", "/")
    if output_file not in output_files:
        print(f'No corresponding .out file for {input_file}')
        results = (None, None, f'No corresponding .out file for {input_file}')
    else:
        cost = ov.validate_output(input_file, output_file)[1]
        # baselineCost = ov.validate_output(input_file, "./baseline_outputs/" + output_file.split("/")[-1], params=args.params)[1]
        baselineCost = all_baseline[i]
        # all_baseline.append(baselineCost)
        results = cost / baselineCost
        print("Input: ", input_file, "\t Results: ", results)
        all_results.append(min(results, 1))
        return min(results, 1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the output validator is run on all files in the output directory. Else, it is run on just the given output file')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('output', type=str, help='The path to the output file or directory')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    if args.all:
        input_directory, output_directory = args.input, args.output
        validate_all_outputs(input_directory, output_directory, params=args.params)
    else:
        input_file, output_file = args.input, args.output
        cost = ov.validate_output(input_file, output_file, params=args.params)[1]
        baselineCost = ov.validate_output(input_file, "./baseline_outputs/" + output_file.split("/")[-1], params=args.params)[1]
        print(cost / baselineCost)

