Program outlier_detection_ilf.py process Caliper JSON format data collected from Problem Roulette (PR). Refer to https://github.com/tl-its-umich-edu/caliper-event-analysis/tree/master/src/extract/ for scripts that extract data from Problem Roulette's database.

The program should be excecuted from command line. You will need Python version 3.6+ and packages [pandas, math, sklearn, argparse, json] to run the program.

The program use Isolation Forest algorithm to detect rare ones among all PR problem-dealing events and consider them "outliers". Dimensions used in the to detect outliers include:

	IsComplete: whether PR user completed or skipped a problem;
	IsCorrect: whether PR user's answer to problem was coorect;
	AttemptCount: number of times PR user tried with the same problem (including current one);
	AttemptDuration: length of time PR user spent on the problem (measured in seconds).

Command-line options:
	
	--perc: Determine percentage of events in data to be considered "outliers". Default value 0.05.
	--uselog: Decide whether or not to use log value of AttemptDuration. Default value True.

Sample command:
	
	python3 --perc 0.1 --uselog f outlier_detection_ilf.py prdata.json

Data Output: a csv file with two columns.

	OpenlrsSourceId: can be used to map to input data.
	IsInlier: the result of IsolationForest prediction.
		value 1: Inlier
		value -1: Outlier