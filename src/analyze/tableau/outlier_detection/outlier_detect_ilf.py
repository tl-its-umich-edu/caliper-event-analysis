import sys
import argparse
import json
import pandas as pd
from math import log
from sklearn.ensemble import IsolationForest


def parse_file_to_dataframe(f_name):
    # read from json file and get pandas data frame
    events = []
    f = open(f_name, 'r')
    for line in f:
        rec = json.loads(line)
        id = rec['openlrsSourceId']
        if 'Completed' in rec['action']:
            is_complete = 1
            if rec['generated']['extensions']['isStudentAnswerCorrect']:
                is_correct = 1
            else:
                is_correct = 0
        elif 'Skipped' in rec['action']:
            is_complete = 0
            is_correct = -1
        else:
            continue
        attempt_count = int(rec['generated']['attempt']['count'])
        attempt_duration = int(''.join([i for i in rec['generated']['attempt']['duration'] if i.isdigit()]))
        events.append([id, is_complete, is_correct, attempt_count, attempt_duration])
    return pd.DataFrame(events, columns=['OpenlrsSourceId', 'IsComplete', 'IsCorrect', 'AttemptCount', 'AttemptDuration'])

def use_log_value(data):
    data['AttemptDuration'] = map(lambda x: -1 if x == 0 else log(x), data['AttemptDuration'])

def ilf_outlier_detect(data, contamination, use_log):
    # generate column "IsInlier" as result of detection
    if use_log:
        use_log_value(data)
    ilf = IsolationForest(contamination=contamination) # Consider 5% of the data as "outliers" if not specified
    use_df = data[data.columns[1:]]
    ilf.fit(use_df) # Fit the model
    data['IsInlier'] = ilf.predict(use_df) # Unsupervised learning and predicting outliers


def main():

    if sys.version_info < (3, 6):
        print('Python version 3.6+ is required.')
        sys.exit(1)

    argParser = argparse.ArgumentParser(
        description="Decide which problem-dealing events are considered outliers."
    )
    argParser.add_argument(
        'input_file',
        type=str,
        metavar='INPUT_FILE',
        default='',
        nargs='?',
        help='''JSON file for processing.'''
    )
    argParser.add_argument(
        'output_file',
        type=str,
        metavar='OUTPUT_FILE',
        default='',
        nargs='?',
        help='''Output csv file.
                Default: %(default)s.'''
    )
    argParser.add_argument(
        '--perc',
        type=float,
        dest='contamination',
        default=0.05,
        help='''Percentage of outliers in data.
                Default: %(default)s.'''
    )
    argParser.add_argument(
        '--uselog',
        action='store_true',
        dest='use_log',
        default=False,
        help='''Use log value of AttemptDuration.'''
    )
    args = argParser.parse_args()

    if args.input_file == '':
        print("No input file provided.")
        sys.exit(1)

    # if no output file name provided, redirect the output to stdout;
    if args.output_file == '':
        path_or_buf = sys.stdout
        msg = ''
    else:
        path_or_buf = args.output_file
        msg = "Please check your working directory for output file."

    try:
        data = parse_file_to_dataframe(args.input_file)
        ilf_outlier_detect(data, args.contamination, args.use_log)
        data.to_csv(path_or_buf=path_or_buf, columns=['OpenlrsSourceId', 'IsInlier'], index=False)
    except Exception as ex:
        print("An error has occurred:")
        print(ex)
        sys.exit(1)

    if msg:
        print(msg)


if __name__ == "__main__":
    main()
