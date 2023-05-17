# Exporting Apple Health data using Python

This repository provides some useful information for extracting specific data from the Apple health app given in the form of an XML file. Luckily the process of extracting data from a very large file is made simple through python (read below). 

First export the data file:

        1. Open the Health app on your iPhone
        2. Click on the Account icon and scroll down to "Export All Health Data"
        3. Send the "export.zip" file you just downloaded to your computer and extract

![Alt text](export.jpeg)

This export file will contain the following : 

        export.xml
        export_cda.xml
        workout-routes

***export.xml*** is the one we need. This file will contain lots of data and may take time to load.


# XML 

Extensible Markup Language (XML) is a markup language and file format used for storing and transmitting structured data. If you are unfamiliar with XML, i highly recommend taking a look mozilla's [XML introduction](https://developer.mozilla.org/en-US/docs/Web/XML/XML_introduction).

Opening the file can be alarming as there are thousands of lines of data, but we can browse through it very briefly to get a better understanding of how the elements are stored. This will help us with knowing how to refer to the elements when we want to extract them later. Here our element of interest is the "Workout" element and its contents

![Alt text](workout.png)


# HealthKit :

If you are curious or uncertain about a particular element or attribute, you can browse through Apple's [HealthKit documentation](https://developer.apple.com/documentation/healthkit) for more details :

![Alt text](workoutactivitytype.png)


https://developer.apple.com/documentation/healthkit/hkworkouttype



# Python :

To extract specific elements of interest from this large XML file, we can use Python to write our own parsing logic and leverage its rich collection of frameworks for data handling and analysis. In this case we are using *Pandas* to put the collected pieces of information into a much more succint dataframe.
```python
import datetime
import pandas as pd
import xml.etree.ElementTree as ET
```

We parse the XML file using the ElementTree module. Make sure to specify the correct path/location of to your export.xml file 
```python
tree = ET.parse('data/export.xml')
root = tree.getroot()
```

Next we iterate throught the target elements. You can add/remove fields according to your usecase. Here we are iterating through the 'Workout' elements and storing 'type', 'startDate', 'Duration'
```python
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
    
        # append data to list        
        data.append(workout_data)
```


If you are interested in one or two specific fields from your data frame, you might find it easier to print the target data out to the console and copy/paste directly : For example here we extract the distance element and print it along with the startDate

```python
...
        workout_data['duration'] = float(workout.attrib['duration'])

        # Extract the DistanceWalkingRunning sum element
        for stat in workout.iter('WorkoutStatistics'):
            if stat.attrib['type'] == 'HKQuantityTypeIdentifierDistanceWalkingRunning':
                workout_data['distance'] = stat.attrib['sum']
                print(workout_data['startdate'] + ": " + workout_data['distance'] + "mi")

        # append data to list        
        data.append(workout_data)
```
Output to the console: <br>

        Feb 03 2023: 5.00482mi
        Feb 06 2023: 5.18372mi
        Feb 08 2023: 6.63026mi
        ...
        May 10 2023: 6.67133mi
        Process finished with exit code 0


Finally, you can decide how to export the data you collected : 
```python
# Create a pandas DataFrame from the extracted data
df = pd.DataFrame(data)

# Save DataFrame to CSV
df.to_csv('workout_data.csv', index=False)

# Save DataFrame to html
html = df.to_html('workout_data.html')
```
