import json
import os
from collections import Counter
import matplotlib.pyplot as plt
import requests
from datetime import datetime
from os.path import exists
import numpy as np

# inputs of program
from_file = False  # True  => get data from input data file (data.json) (needs to be updated) False => get data live from API
input_file = "data.json"  # only if data inputted from file
value_to_filter = "europe-west"  # us-central / europe-west / asia-west / asia-east
output_file_filtered_data = (
    value_to_filter + ".json"
)  # gets updated everytime script is excecuted

API_KEY = ""

# getting api  key from .env file and set API_KEY variable
if not exists("key.env"):
    print("key.env file containing API key to bereal.devin.fun API needs to exist")
    exit()
keyfile = open("key.env", mode="r")
key = keyfile.read()
keyfile.close()
API_KEY = key


# remove all other JSON files that are not the input file
directory = os.path.dirname(os.path.abspath(__file__))
files = os.listdir(directory)
for file in files:
    if file.endswith(".json") and file != input_file or file.endswith(".png"):
        os.remove(os.path.join(directory, file))

# filter input data from file to only selected region and output it as a JSON file
if from_file == True:
    if not exists(input_file):
        print(
            "data input file named "
            + input_file
            + " containing JSON data converted from CSV from bereal.devin.fun needs to exist"
        )
        exit()
    with open(input_file, "r") as f:
        data = json.load(f)
    filteredDataToWrite = [
        entry
        for entry in data
        if "Region" in entry and entry["Region"] == value_to_filter
    ]
    with open(output_file_filtered_data, "w") as f:
        json.dump(filteredDataToWrite, f, indent=4)
else:
    headers = {"Accept": "application/json"}
    response = requests.get(
        "https://bereal.devin.rest/v1/moments/all?api_key="
        + API_KEY
        + "&limit=NONE"
        + "&format=JSON",
        headers=headers,
    )
    if "Service Unavailable".lower() in response.text.lower():
        print("API is currently unavailable")
        print("https://status.devin.fun/?ref=offline-db-us-east1")
        exit()
    data_from_api_regions = response.json()["regions"]
    converted_data = []
    desired_region = value_to_filter
    if desired_region in data_from_api_regions:
        moments = data_from_api_regions[desired_region]
        for moment in moments:
            converted_moment = {
                "Moment ID": moment["id"],
                "Region": desired_region,
                "Timestamp (UTC)": moment["utc"],
            }
            converted_data.append(converted_moment)
    with open(output_file_filtered_data, "w") as f:
        json.dump(converted_data, f, indent=4)

# graph data on time of day (hours) (UTC)
with open(output_file_filtered_data, "r") as filtered:
    filteredData = json.load(filtered)
timestamps = [entry["Timestamp (UTC)"] for entry in filteredData]
time_parts = [timestamp.split(" ")[1] for timestamp in timestamps]
hours = [timepart.split(":")[0] for timepart in time_parts]
hourRanges = [f"{hour}:00 - {hour}:59" for hour in hours]
hourRangesCounted = Counter(hourRanges)
hourRangesCountedSorted = sorted(hourRangesCounted.items())
labels = []
counts = []
left_coordinates = []
coordCounter = 1
for key, value in hourRangesCountedSorted:
    labels.append(key)
    counts.append(value)
    left_coordinates.append(coordCounter)
    coordCounter += 1
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(
    left_coordinates, counts, tick_label=labels, width=0.6, color=["#FECC00", "black"]
)
ax.set_xlabel("Hours of day")
ax.set_ylabel("Dataset entries")
ax.set_title("BeReal moments (UTC)")
ax.tick_params(axis="x", labelsize=8)
ax.tick_params(axis="y", labelsize=8)
ax.title.set_fontsize(12)
ax.set_xticks(left_coordinates)
ax.set_xticklabels(labels, rotation=45, ha="right")
plt.tight_layout()

# save graph to image with current time in filename
current_datetime = datetime.now()
current_datetime_str = (current_datetime.strftime("%Y-%m-%d %H-%M-%S")).replace(
    " ", "_"
)
filename = current_datetime_str + "_plot.png"

# Generate trend line data
x = np.arange(len(left_coordinates))
y = np.array(counts)
z = np.polyfit(x, y, 2)  # Use a second-degree polynomial fit
p = np.poly1d(z)
trend_line = p(x)

# Plot the bar graph with trend line
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(
    np.arange(len(left_coordinates)),
    counts,
    tick_label=labels,
    width=0.6,
    color=["#FECC00", "black"],
)
ax.plot(
    x, trend_line, color="red", linestyle="--", label="Trend Line"
)  # Add trend line
ax.set_xlabel("Hours of day")
ax.set_ylabel("Dataset entries")
ax.set_title("BeReal moments (UTC)")
ax.tick_params(axis="x", labelsize=8)
ax.tick_params(axis="y", labelsize=8)
ax.title.set_fontsize(12)
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45, ha="right")
ax.legend()  # Add legend for trend line
plt.tight_layout()

plt.savefig(filename)
print("successfully created new bar graph")
