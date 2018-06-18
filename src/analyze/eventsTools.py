import numpy as np
import gzip
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd

# Variables required
# ------------------
#
# The following variables are usually set by the user in a Jupyter Notebook cell
# before any of the functions in this module are called:
#
# Path to input data file.
# path = '../../tmp/pr.jsonl'
#
# Is the input JSONL (JSON Lines)? (If False, input will be treated as plain JSON)
# The JSONL format (AKA NDJSON, newline-delimited JSON) contains complete JSON objects
# separated only by line breaks (newline or carriage return)
# jsonlInput = True
#
# Output to PDF?  (If False, display output inline with Jupyter Notebook)
# pdfOutput = True
#
# Name of PDF output file.  (Ignored if pdfOutput == False)
# pdfFilename = 'events.pdf'

# Format of ISO 8601 timestamps (for datetime.strptime)
ISO8601_TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

FILE_MODE_READ = 'r'
FILE_MODE_READ_TEXT = 'rt'

# Some figure formats for convenience.  Instead of using a string to specify the
# output formats, use one of these symbols instead.  They will usually work with
# editor autocompletion.
FIGURE_FORMAT_PDF = 'pdf'
FIGURE_FORMAT_PNG = 'png'
FIGURE_FORMAT_SVG = 'svg'
    
def loadEventJson(path, jsonlInput):
    '''This automatically supports files that have been compressed with `gzip`.'''
    if (jsonlInput):
        import ndjson as json
    else:
        import json

    try:
        with gzip.open(path, FILE_MODE_READ_TEXT) as gid:
            all_recs = json.load(gid)
    except OSError:
        with open(path, FILE_MODE_READ) as gid:
            all_recs = json.load(gid)
    
    return all_recs

def extractEventActorUserId(js):
    if 'actor' not in js or js['actor'] is None:
        return False
    actor = js['actor']
    user_url = actor['@id']
    user = user_url.split(':')
    
    return user

def extractEventCourseName(js):
    if 'group' not in js or js['group'] is None:
        return False
    course = js['group']['name']
    
    return course
    
def extractEventTime(js, tfields):
    etime = js['eventTime']
    etime = datetime.strptime(etime, ISO8601_TIMESTAMP_FORMAT)
    etime = etime.timetuple()
    etime = [getattr(etime, x) for x in tfields]
    
    return etime

def visualizeInit():
    ax = plt.axes()
    return ax

def visualizeFinal(ax, course, vc, xlabel, d, pdfOutput):
    ax.set_title(course)
    ax.grid(True)
    ax.set_xlabel(xlabel)

    ax.plot(d, vc.values, '-', color='grey')
    ax.plot(d, vc.values, 'o', color='orange', alpha=0.8)

    ax.set_ylabel('Records', size=15)
        
    if (pdfOutput):
        pdf.savefig()
    else:
        plt.show()

    plt.clf()

def visualizeByDate(course, mat, pdfOutput):
    vc = mat['tm_yday'].value_counts().sort_index()
    d = [datetime.fromordinal(x) for x in vc.index]
    
    ax = visualizeInit()
    
    months = mdates.MonthLocator()
    days = mdates.DayLocator(bymonthday=[1, 7, 14, 21, 28])
    months_fmt = mdates.DateFormatter('%b')
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_minor_locator(days)
    ax.xaxis.set_major_formatter(months_fmt)
    
    visualizeFinal(ax, course, vc, 'Date', d, pdfOutput)
    
def visualizeByWeekday(course, mat, pdfOutput):
    vc = mat['tm_wday'].value_counts().sort_index()
    d = vc.index.tolist()
    
    ax = visualizeInit()

    ax.xaxis.set_ticks([0, 1, 2, 3, 4, 5, 6])
    ax.xaxis.set_ticklabels(['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'])
    ax.set_xlim(-0.2, 6.2)

    visualizeFinal(ax, course, vc, 'Day of Week', d, pdfOutput)

def visualizeByHour(course, mat, pdfOutput):
    vc = mat['tm_hour'].value_counts().sort_index()
    d = vc.index.tolist()

    ax = visualizeInit()

    ax.xaxis.set_ticks(range(0, 24, 3))

    visualizeFinal(ax, course, vc, 'Hour of Day', d, pdfOutput)
