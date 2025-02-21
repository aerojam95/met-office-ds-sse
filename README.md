# **Forecaster's Reference Book Method**

## Overview

This Python script implements a forecaster's reference book method to process weather data and compute the minimum temperature at noon (Temp. min. noon) based on various weather parameters, including wind speed and cloud cover. The method reads from a CSV data file, uses a lookup table for wind speed and cloud cover ranges, and outputs the processed data to a new CSV file.

## Table of Contents
- [Background](#background)
- [Data](#data)
    - [Configuration File](#configuration-file)
    - [`K_lookup.csv`](#k_lookupcsv)
    - [Input files](#input-files)
- [Code](#code)
    - [Python virtual environment](#python-venv)
    - [Script Execution](#script-execution)
    - [Output Generation](#output-generation)

## Background

The code performs the following calculations:

- It compares the wind speed and cloud cover from the data against the ranges in the K lookup table
- For each row in the input data, it finds the matching row in the lookup table where the wind speed and cloud cover fall within the defined ranges and assigns the corresponding K value

The method then computes the minimum temperature at noon (Temp. min. noon) based on the formula:

```
Temp. min. noon = 0.316 * Temp. noon + 0.548 * Temp. dew point noon - 1.24 + K
```

Where `K` is the value assigned from by a lookup table. The result is rounded to the precision defined in a configuration file.

## Data

### Configuration File (`forecasters_reference_book_config.yaml`)

The configuration file is used to define various paths and settings. The structure is as follows:

```yaml
method_data:
  k_lookup_file_path: "../data/K_lookup.csv"  # Path to the K lookup CSV file

data:
  data_file_path: "../data/initial_data.csv"  # Path to the input weather data CSV file

outputs:
  decimal_place_precision: 1  # Decimal precision for output temperature min. at 12 pm
  output_filename: "initial_outputs.csv"  # Name of the output file
  output_directory: "../outputs/"  # Directory to save the output file

```

### `K_lookup.csv`

This CSV file contains a lookup table for wind speed, cloud cover, and the corresponding K values and is required for programme execution. It has the following columns:

- `wind speed min. (knots)`: Minimum wind speed in knots
- `wind speed max. (knots)`: Maximum wind speed in knots
- `cloud cover min. (oktas)`: Minimum cloud cover in oktas
- `cloud cover max. (oktas)`: Maximum cloud cover in oktas
- `K ()`: The K value corresponding to the wind speed and cloud cover range

*Lookup file*

```csv
wind speed min. (knots),wind speed max. (knots),cloud cover min. (oktas),cloud cover max. (oktas),K ()
0,12,0,2,-2.2
0,12,2,4,-1.7
0,12,4,6,-0.6
0,12,6,8,0
13,25,0,2,-1.1
13,25,2,4,0
13,25,4,6,0.6
13,25,6,8,1.1
26,38,0,2,-0.6
26,38,2,4,0
26,38,4,6,0.6
26,38,6,8,1.1
39,51,0,2,1.1
39,51,2,4,1.7
39,51,4,6,2.8
39,51,6,8,NaN
```

### Input files

This input CSV contains weather data with columns for temperature, wind speed, and cloud cover. The columns are:

- `Temp. noon (celcius)`: Temperature at noon in Celsius
- `Temp. dew point noon` (celius): Dew point temperature at noon in Celsius
- `wind speed (knots)`: Wind speed in knots
- `cloud cover (oktas)`: Cloud cover in oktas
- `location`: Location name
- `date`: Date of the observation

*Example*

```csv
Temp. noon (celcius),Temp. dew point noon (celius),wind speed (knots),cloud cover (oktas),location,date
22.4,10.9,14.56,3.9,A,1
18.6,12.56,3.4,6,B,1
26,8.5,0,0.0,B,2
13.2,9.4,12.5, 4.1,C,2
```

## Code

The code to produce the models and results for the comparative study can be found in [src](src/).

### Python virtual environment

Before using the code it is best to setup and start a Python virtual environment in order to avoid potential package clashes using the [requirements](src/requirements.txt) file:

```
# Navigate into the data project directory

# Create a virtual environment
python3 -m venv <env-name>

# Activate virtual environment
source <env-name>/bin/activate

# Install dependencies for code
pip3 install -r requirements.txt

# When finished with virtual environment
deactivate
```

### Script Execution

To execute the script, run the following command:

```bash
python3 forecasters_reference_book.py
```

### Output Generation

The processed data is saved to a CSV file. The output filename and directory are specified in the configuration file. If the file already exists, it will be overwritten.

The output file contains the original data along with the newly computed `Temp. min. noon (celcius)` column.

Example output:

```csv
Temp. noon (celcius),Temp. dew point noon (celius),wind speed (knots),cloud cover (oktas),location,date,K (),Temp. min. noon (celcius)
22.4,10.9,14.56,3.9,A,1,0.0,11.8
18.6,12.56,3.4,6.0,B,1,-0.6,10.9
26.0,8.5,0.0,0.0,B,2,-2.2,9.4
13.2,9.4,12.5,4.1,C,2,-2.2,5.9
```