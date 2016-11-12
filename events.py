import numpy as np
import json
import gzip
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

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
agg = {}
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

    if course not in agg:
        agg[course] = []
    agg[course].append(list(etime.timetuple()))


pdf = PdfPages("events.pdf")

xlabels = {6: "Day of week", 7: "Date", 3: "Hour"}

for course in agg.keys():

    mat = np.asarray(agg[course])

    # Three types of plots: by day, by weekday, and by hour
    for col in 6, 7, 3:

        u, c = np.unique(mat[:, col], return_counts=True)

        if col == 7:
            d = [datetime.fromordinal(x) for x in u]
        else:
            d = u

        plt.clf()
        ax = plt.axes()

        if col == 6:
            ax.xaxis.set_ticks([0, 1, 2, 3, 4, 5, 6])
            ax.xaxis.set_ticklabels(["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"])
            ax.set_xlim(-0.2, 6.2)
        elif col == 7:
            months = mdates.MonthLocator()
            days = mdates.DayLocator(bymonthday=[1, 7, 14, 21, 28])
            months_fmt = mdates.DateFormatter('%b')
            ax.xaxis.set_major_locator(months)
            ax.xaxis.set_minor_locator(days)
            ax.xaxis.set_major_formatter(months_fmt)
        elif col == 3:
            ax.xaxis.set_ticks(range(0, 24, 3))

        ax.set_title(course)
        ax.grid(True)
        ax.set_xlabel(xlabels[col])

        ax.plot(d, c, '-', color='grey')
        ax.plot(d, c, 'o', color='orange', alpha=0.8)

        ax.set_ylabel("Records", size=15)
        pdf.savefig()

pdf.close()
