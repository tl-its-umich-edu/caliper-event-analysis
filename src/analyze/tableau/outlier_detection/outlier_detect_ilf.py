import sys
import argparse
import json
import pandas as pd
from math import log
from sklearn.ensemble import IsolationForest


def read_file(f_name):
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

def cal_log(x):
    if x == 0:
        return 0
    else:
        return log(x)

def use_log_value(data):
    data['AttemptDuration'] = list(map(cal_log, data['AttemptDuration']))

def ilf_predict(data, contamination, use_log):
    if use_log:
        use_log_value(data)
    ilf = IsolationForest(contamination=contamination) # Consider 5% of the data as "outliers" if not specified
    use_df = data[data.columns[1:]]
    ilf.fit(use_df) # Fit the model
    data['IsInlier'] = ilf.predict(use_df) # Unsupervised learning and predicting outliers


def main():

    if sys.version_info < (3, 6):
        print('Sorry, need Python version 3.6+')
        sys.exit(1)

    argParser = argparse.ArgumentParser(
        description="Decide which problem-dealing events are considered outliers."
    )
    argParser.add_argument(
        'file',
        type=str,
        metavar='FILE',
        default='',
        nargs='?',
        help='JSON file for processing'
    )
    argParser.add_argument(
        '--perc',
        type=float,
        dest='contamination',
        default=0.05,
        help='''Percentage of outliers in data.
                Default: %(default)s'''
    )
    argParser.add_argument(
        '--uselog',
        type=bool,
        dest='use_log',
        default=True,
        help='''Whether or not use log value of Attempt Duration.
                Default: %(default)s'''
    )
    args = argParser.parse_args()

    if args.file == '':
        print("No file name provided.")
        sys.exit(1)

    try:
        data = read_file(args.file)
        ilf_predict(data, args.contamination, args.use_log)
        data.to_csv('outlier_detect.csv', columns=['OpenlrsSourceId', 'IsInlier'], index=False)
    except:
        print("Sorry, cannot read this file.")
        sys.exit(1)

    print("Please check your working directory for output file 'outlier_detect.csv'.")


if __name__ == "__main__":
    main()
