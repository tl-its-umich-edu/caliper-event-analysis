For running outlier_detection_ilf.py:

Needed packages: pandas, math, sklearn.

Data Preparation: store data in a csv file, including the dimensions (must be numeric values) 
that are going to be used for identifing outliers. The first line of csv stores dimension names.

Data Output: a csv file with a single column showing the result of IsolationForest prediction.

	value 1: Inlier
	value -1: Outlier
