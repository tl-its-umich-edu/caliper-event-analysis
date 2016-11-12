import numpy as np
import json
import gzip
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

path = "/nfs/kshedden/Lance_Sloan/pr.json.gz"

all_recs = []
with gzip.open(path, "rt") as gid:
    all_recs = json.load(gid)

agg = {}

tfmt = "%Y-%m-%dT%H:%M:%S.%fZ"

for rec in all_recs:
    js = json.loads(rec['raw'])
    if 'actor' not in js or js['actor'] is None:
        continue
    actor = js['actor']
    user_url = actor["@id"]
    user = user_url.split(":")
    if len(user) < 3:
        continue
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

    for col in 6, 7, 3:

        u, c = np.unique(mat[:, col], return_counts=True)

        if col == 7:
            d = [datetime.fromordinal(x) for x in u]
        else:
            d = u

        plt.clf()
        ax = plt.axes()

        if col == 7:
            months = mdates.MonthLocator()
            days = mdates.DayLocator(bymonthday=[1, 7, 14, 21, 28])
            months_fmt = mdates.DateFormatter('%b')
            ax.xaxis.set_major_locator(months)
            ax.xaxis.set_minor_locator(days)
            ax.xaxis.set_major_formatter(months_fmt)
        elif col == 6:
            ax.xaxis.set_ticks([0, 1, 2, 3, 4, 5, 6])
            ax.xaxis.set_ticklabels(["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"])
        elif col == 3:
            ax.xaxis.set_ticks(range(0, 24, 3))

        ax.set_title(course)
        ax.grid(True)
        ax.set_xlabel(xlabels[col])

        ax.plot(d, c, '-', color='grey')
        ax.plot(d, c, 'o', color='orange', alpha=0.8)

        if col == 6:
            ax.set_xlim(-0.2, 6.2)

        ax.set_ylabel("Records", size=15)
        pdf.savefig()

pdf.close()
