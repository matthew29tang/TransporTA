import output_validator as ov
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
import pickle
import input_validator

def validate_all_outputs(input_directory, output_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, '.in')
    output_files = utils.get_files_with_extension(output_directory, '.out')

    all_results = []
    all_baseline = pickle.load(open("baselineCosts.p", "rb"))
    i = 0
    for input_file in input_files:
        output_file = utils.input_to_output(input_file, output_directory).replace("\\", "/")
        if output_file not in output_files:
            print(f'No corresponding .out file for {input_file}')
            results = (None, None, f'No corresponding .out file for {input_file}')
        else:
            cost = ov.validate_output(input_file, output_file, params=args.params)[1]
            # baselineCost = ov.validate_output(input_file, "./baseline_outputs/" + output_file.split("/")[-1], params=args.params)[1]
            baselineCost = all_baseline[i]
            all_baseline.append(baselineCost)
            results = cost / baselineCost
            print("Input: ", input_file, "\t Results: ", results)
        all_results.append(results)
        i += 1
    # pickle.dump(all_baseline, open( "baselineCosts.p", "wb" )) Cache results
    print("Total results: ", str(100 / 949 * sum(all_results)))
    return all_results

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

