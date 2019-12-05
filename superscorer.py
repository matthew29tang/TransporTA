import output_validator as ov
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
import pickle
import input_validator
from shutil import copyfile
from datetime import datetime

# Set true for multi-core enhancement.
import multiprocessing
from multiprocessing import Pool
from multiprocessing import Array
from multiprocessing import Manager
MULTICORE = True
num_thread = multiprocessing.cpu_count()
VERBOSE = False

def validate_all_outputs(input_directory, output_directories):
    input_files = utils.get_files_with_extension(input_directory, '.in')
    output_files_list =  [utils.get_files_with_extension(output_directory, '.out') for output_directory in output_directories]

    results = []
    bestOutputs = []
    for i in range(len(input_files)):
        input_file = input_files[i]
        result, bestOutput = _outputCost(input_file, output_directories)
        results.append(result)
        bestOutputs.append(bestOutput)
        masterOutput = "master/" + input_file.split("/")[-1].split(".")[0] + ".out"
        print(output_files_list[bestOutput][i])
        copyfile(output_files_list[bestOutput][i], masterOutput)

    final_score = "Superscored " + str(len(output_directories)) +  " directories with a score of: " + str(100 / len(results) * sum(results))
    print(final_score)
    a = open(str(datetime.now()).split(".")[0].replace(":","-")+".log", "w")
    for r in results:
        a.write(str(r) + "\n")
    a.write("\n")
    for b in bestOutputs:
        a.write(str(b) + "\n")
    a.write("\n")
    for inp in inputs:
        a.write(str(inp) + "\n")
    a.write(final_score)
    a.close()

    return results

def _outputCost(input_file, output_directories):
    output_files = [utils.input_to_output(input_file, output_directory).replace("\\", "/") for output_directory in output_directories]
    costs = [ov.validate_output(input_file, output_file, verbose=VERBOSE)[1] for output_file in output_files]
    print("Input: ", input_file, "\t Results: ", min(costs) / costs[-1], "\t from: ", costs.index(min(costs)))
    return min(costs) / costs[-1], costs.index(min(costs))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('-v', action='store_true', help='Verbose output')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('outputs', nargs=argparse.REMAINDER, help='Output directories')
    args = parser.parse_args()
    if args.v:
        VERBOSE = True
    input_directory, output_directories = args.input, args.outputs
    output_directories.append("baseline_outputs")
    validate_all_outputs(input_directory, output_directories)

