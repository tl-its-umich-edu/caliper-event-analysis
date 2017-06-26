Program outlier_detection_ilf.py process Caliper JSON format data collected from Problem Roulette (PR). Refer to https://github.com/tl-its-umich-edu/caliper-event-analysis/tree/master/src/extract/ for scripts that extract data from Problem Roulette's database.

The program should be excecuted from command line. You will need Python version 3.6+ and packages [pandas, math, sklearn, argparse, json] to run the program.

The program use [Isolation Forest](http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html) algorithm to detect rare ones among all PR problem-dealing events and consider them "outliers". Dimensions used in the algorithm to detect outliers include:

	IsComplete: whether PR user completed or skipped a problem;
	IsCorrect: whether PR user's answer to problem was coorect;
	AttemptCount: number of times PR user tried with the same problem (including current one);
	AttemptDuration: length of time PR user spent on the problem (measured in seconds).

Command-line usage:

	outlier_detect_ilf.py \[-h\] \[--perc CONTAMINATION\] \[--uselog\] INPUT_FILE \[OUTPUT_FILE\]

Command-line arguments:

	[INPUT_FILE]: Required. Name of the JSON file to be parsed.
	[OUTPUT_FILE]: Optional. If no name provided, the output is sent to standard output. User can redirect it to a file.

Command-line options:
	
	-h, --help: Show help message.
	--perc CONTAMINATION: Determine percentage of events in data to be considered "outliers". Default value 0.05.
	--uselog: Use log value of AttemptDuration. If not specified, the program defaults to use raw value of AttemptDuration (measured in seconds).

Sample command:
	
	python3 outlier_detection_ilf.py --perc 0.1 inputf.json
	python3 outlier_detection_ilf.py --uselog inputf.json > outputf.csv
	python3 outlier_detection_ilf.py inputf.json outputf.csv

Data Output: a csv file with two columns.

	OpenlrsSourceId: can be used to map to input data.
	IsInlier: the result of IsolationForest prediction.
		value 1: Inlier
		value -1: Outlier
