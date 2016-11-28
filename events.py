import numpy as np
import json
import gzip
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd

# Path to data file
path = "/nfs/kshedden/Lance_Sloan/pr.json.gz"

# Load the raw json data
all_recs = []
with gzip.open(path, "rt") as gid:
    all_recs = json.load(gid)

# strptime for posix time stamps
tfmt = "%Y-%m-%dT%H:%M:%S.%fZ"

# Extract some fields for each event; agg is a map from course names
# to event time stamps, the event times are split into columns
# according to the time.struct_time fields:
# https://docs.python.org/3/library/time.html#time.struct_time
agg = []
tfields = ['tm_hour', 'tm_mday', 'tm_min', 'tm_mon', 'tm_wday', 'tm_yday', 'tm_year']
for rec in all_recs:

    # This seems to be where the good information is
    js = json.loads(rec['raw'])

    # Extract the user id/, but not currently used here
    if 'actor' not in js or js['actor'] is None:
        continue
    actor = js['actor']
    user_url = actor["@id"]
    user = user_url.split(":")
    if len(user) < 3:
        continue

    # Extract the time
    if 'group' not in js or js['group'] is None:
        continue
    course = js['group']['name']
    etime = js['eventTime']
    etime = datetime.strptime(etime, tfmt)
    etime = etime.timetuple()
    etime = [getattr(etime, x) for x in tfields]
    etime.append(course)
    agg.append(etime)

agg = pd.DataFrame(agg)
agg.columns = tfields + ["course"]

pdf = PdfPages("events.pdf")

xlabels = {"tm_wday": "Day of week", "tm_yday": "Date", "tm_hour": "Hour"}

for course, mat in agg.groupby("course"):

    # Three types of plots: by day, by weekday, and by hour
    for col in "tm_yday", "tm_wday", "tm_hour":

        vc = mat[col].value_counts().sort_index()

        if col == "tm_yday":
            d = [datetime.fromordinal(x) for x in vc.index]
        else:
            d = vc.index.tolist()

        plt.clf()
        ax = plt.axes()

        if col == "tm_wday":
            ax.xaxis.set_ticks([0, 1, 2, 3, 4, 5, 6])
            ax.xaxis.set_ticklabels(["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"])
            ax.set_xlim(-0.2, 6.2)
        elif col == "tm_yday":
            months = mdates.MonthLocator()
            days = mdates.DayLocator(bymonthday=[1, 7, 14, 21, 28])
            months_fmt = mdates.DateFormatter('%b')
            ax.xaxis.set_major_locator(months)
            ax.xaxis.set_minor_locator(days)
            ax.xaxis.set_major_formatter(months_fmt)
        elif col == "tm_hour":
            ax.xaxis.set_ticks(range(0, 24, 3))

        ax.set_title(course)
        ax.grid(True)
        ax.set_xlabel(xlabels[col])

        ax.plot(d, vc.values, '-', color='grey')
        ax.plot(d, vc.values, 'o', color='orange', alpha=0.8)

        ax.set_ylabel("Records", size=15)
        pdf.savefig()

pdf.close()
