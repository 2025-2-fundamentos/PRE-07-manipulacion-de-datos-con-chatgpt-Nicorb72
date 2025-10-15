import os
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

drivers = pd.read_csv("files/input/drivers.csv", sep=",", thousands=None, decimal=".")
timesheet = pd.read_csv("files/input/timesheet.csv", sep=",", thousands=None, decimal=".")

mean_timesheet = timesheet.groupby("driverId").mean()
mean_timesheet.pop("week")

mean_hours_logged_by_driver = timesheet.groupby("driverId")["hours-logged"].transform("mean")
timesheet_with_means = timesheet.copy()
timesheet_with_means["mean_hours-logged"] = mean_hours_logged_by_driver

timesheet_below = timesheet_with_means[
    timesheet_with_means["hours-logged"] < timesheet_with_means["mean_hours-logged"]
]

sum_timesheet = timesheet.groupby("driverId").sum()
sum_timesheet.pop("week")

summary = pd.merge(sum_timesheet, drivers[["driverId", "name"]], on="driverId")

if not os.path.exists("files/output"):
    os.makedirs("files/output")

summary.to_csv("files/output/summary.csv", sep=",", header=True, index=False)

top10 = summary.sort_values(by="miles-logged", ascending=False).head(10)
top10 = top10.set_index("name")

top10["miles-logged"].plot.barh(color="tab:orange", alpha=0.6)
plt.gca().invert_yaxis()
plt.gca().get_xaxis().set_major_formatter(
    matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
)
plt.xticks(rotation=90)
plt.gca().spines["left"].set_color("lightgray")
plt.gca().spines["bottom"].set_color("gray")
plt.gca().spines["top"].set_visible(False)
plt.gca().spines["right"].set_visible(False)

if not os.path.exists("files/plots"):
    os.makedirs("files/plots")

plt.savefig("files/plots/top10_drivers.png", bbox_inches="tight")