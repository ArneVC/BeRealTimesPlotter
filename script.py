import json
import os
from collections import Counter
import matplotlib.pyplot as plt
import requests

# inputs of program
from_file = False  # True  => get data from input data file (needs to be updated) False => get data live from API
input_file = "data.json"  # only if data inputted from file
value_to_filter = "europe-west"
output_file_filtered_data = value_to_filter + ".json"

API_KEY = ""

# getting api  key from .env file and set API_KEY variable
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
        + "&limit=NONE&format=JSON",
        headers=headers,
    )
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
ax.set_xlabel("Uren van de dag")
ax.set_ylabel("Aantal keer in dataset")
ax.set_title("BeReal momenten (UTC)")
ax.tick_params(axis="x", labelsize=8)
ax.tick_params(axis="y", labelsize=8)
ax.title.set_fontsize(12)
ax.set_xticks(left_coordinates)
ax.set_xticklabels(labels, rotation=45, ha="right")
plt.tight_layout()
plt.savefig("plot.png")
