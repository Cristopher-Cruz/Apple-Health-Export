import datetime
import pandas as pd
import xml.etree.ElementTree as ET
# Parse the XML file
tree = ET.parse('data/export.xml')
root = tree.getroot()

data = []
# Iterate over the 'Workout' elements
for workout in root.iter('Workout'):
    creation_date = pd.to_datetime(workout.attrib['creationDate']).tz_convert(None)

    # Getting data for the year 2023 exclusively
    if creation_date.year == 2023:
        workout_data = {}

        # Store data + proper type conversion for dates and numeric values
        workout_data['type'] = workout.attrib['workoutActivityType']
        start_date = pd.to_datetime(workout.attrib['startDate']).strftime('%b %d %Y')
        workout_data['startdate'] = start_date
        workout_data['duration'] = float(workout.attrib['duration'])

        # Extract the DistanceWalkingRunning sum element
        for stat in workout.iter('WorkoutStatistics'):
            if stat.attrib['type'] == 'HKQuantityTypeIdentifierDistanceWalkingRunning':
                workout_data['distance'] = stat.attrib['sum']
                print(workout_data['startdate'] + ": " + workout_data['distance'] + "mi")

        # append data to list
        data.append(workout_data)


# Create a pandas DataFrame from the extracted data
df = pd.DataFrame(data)

# Save DataFrame to CSV
df.to_csv('workout_data.csv', index=False)

# Save DataFrame to html
html = df.to_html('workout_data.html')import datetime
import pandas as pd
import xml.etree.ElementTree as ET
# Parse the XML file
tree = ET.parse('data/export.xml')
root = tree.getroot()

data = []
# Iterate over the 'Workout' elements
for workout in root.iter('Workout'):
    creation_date = pd.to_datetime(workout.attrib['creationDate']).tz_convert(None)

    # Getting data for the year 2023 exclusively
    if creation_date.year == 2023:
        workout_data = {}

        # Store data + proper type conversion for dates and numeric values
        workout_data['type'] = workout.attrib['workoutActivityType']
        start_date = pd.to_datetime(workout.attrib['startDate']).strftime('%b %d %Y')
        workout_data['startdate'] = start_date
        workout_data['duration'] = float(workout.attrib['duration'])

        # Extract the DistanceWalkingRunning sum element
        for stat in workout.iter('WorkoutStatistics'):
            if stat.attrib['type'] == 'HKQuantityTypeIdentifierDistanceWalkingRunning':
                workout_data['distance'] = stat.attrib['sum']
                print(workout_data['startdate'] + ": " + workout_data['distance'] + "mi")

        # append data to list
        data.append(workout_data)


# Create a pandas DataFrame from the extracted data
df = pd.DataFrame(data)

# Save DataFrame to CSV
df.to_csv('workout_data.csv', index=False)

# Save DataFrame to html
html = df.to_html('workout_data.html')