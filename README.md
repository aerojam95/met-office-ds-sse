# **Forecaster's Reference Book Method**

## Overview

This Python script implements a forecaster's reference book method to process weather data and compute the minimum temperature at noon, `Temp. min. noon` (Celcius), based on various weather parameters, including wind speed and cloud cover. The method reads from a `.csv` data file, uses a lookup table for wind speed and cloud cover ranges, and outputs the processed data to a new `.csv` file.

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

The method then computes the minimum temperature at noon (`Temp. min. noon`) based on the formula:

```
Temp. min. noon = 0.316 * Temp. noon + 0.548 * Temp. dew point noon - 1.24 + K
```

Where `K` is the value assigned from by a lookup table.

## Data

### Configuration File (`forecasters_reference_book_config.yaml`)

The configuration file is used to define various paths and settings. The structure is as follows:

```yaml
csv_files:
- constants
- k_lookup
- data

constants:
  constants_file_path: "data/forecasters_reference_book_constants.csv"
  constants_columns:
  - Temp. noon coeff (/celcius)
  - Temp. dew point noon coeff (/celius)
  - Temp. constant (celius)

k_lookup:
  k_lookup_file_path: "data/K_lookup.csv"
  k_lookup_columns:
    - Wind speed min. (knots)
    - Wind speed max. (knots)
    - Cloud cover min. (oktas)
    - Cloud cover max. (oktas)
    - K ()

data:
  data_file_path: "data/initial_data.csv"
  data_columns:
  - Temp. noon (celcius)
  - Temp. dew point noon (celius)
  - Wind speed (knots)
  - Cloud cover (oktas)
  - Location
  - Date

outputs:
  output_file_path: "outputs/initial_outputs.csv"
  output_columns:
  - Temp. noon (celcius)
  - Temp. dew point noon (celius)
  - Wind speed (knots)
  - Cloud cover (oktas)
  - Location
  - Date
  - K ()
  - Temp. min. noon (celcius)
```

The configuration file contains the three `.csv` files containing data needed for the computation of the minimum temperature at noon (`Temp. min. noon`). It lists the three requires `.csv` files for the method's constants, the `K` lookup itself, and the data for which to calculate the the minimum temperature at noon (`Temp. min. noon`). Each of these files is then defined with a file path to the relevant `.csv` file and the columns contained within the files, respectively. The configuration also contains the intended location for output, and the expected columns for the output of the programmes computation.

### Lookup File (`K_lookup.csv`)

This CSV file contains a lookup table for wind speed, cloud cover, and the corresponding K values and is required for programme execution. It has the following columns:

- `Wind speed min. (knots)`: Minimum wind speed in knots
- `Wind speed max. (knots)`: Maximum wind speed in knots
- `Cloud cover min. (oktas)`: Minimum cloud cover in oktas
- `Cloud cover max. (oktas)`: Maximum cloud cover in oktas
- `K ()`: The K value corresponding to the wind speed and cloud cover range

The structure of the lookup table used for the lookup file (`K_lookup.csv`):

```csv
Wind speed min. (knots),Wind speed max. (knots),Cloud cover min. (oktas),Cloud cover max. (oktas),K ()
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
- `Wind speed (knots)`: Wind speed in knots
- `Cloud cover (oktas)`: Cloud cover in oktas
- `Location`: Location name
- `Date`: Date of the observation

The structure of an input `.csv` data file for the computation of the minimum temperature at noon (`Temp. min. noon`):

```csv
Temp. noon (celcius),Temp. dew point noon (celius),Wind speed (knots),Cloud cover (oktas),Location,Date
22.4,10.9,14.56,3.9,1,1
18.6,12.56,3.4,6,2,1
26,8.5,0,0.0,2,2
13.2,9.4,12.5, 4.1,3,2
```

## Code

The code to produce the results for the minimum temperature at noon (`Temp. min. noon`) can be found in [src](src/).

### Python virtual environment

Before using the code it is best to setup and start a Python virtual environment in order to avoid potential package clashes using the [requirements](requirements.txt) file:

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

To execute the script, run the following command from the root directory of the repository:

```bash
python3 main.py --config_file_path=<path-to-YAML-configuration-file>
```

### Output Generation

The processed data is saved to a `.csv` file. The output file path is specified in the configuration file. *If the file already exists, it will be overwritten.*

The output file contains the original data along with the newly computed `Temp. min. noon (celcius)` column.

Example output:

```csv
Temp. noon (celcius),Temp. dew point noon (celius),Wind speed (knots),Cloud cover (oktas),Location,Date,K (),Temp. min. noon (celcius)
22.4,10.9,15.0,4.0,1,1,0.0,11.8116
18.6,12.56,3.0,6.0,2,1,-0.6,10.920480000000001
26.0,8.5,0.0,0.0,2,2,-2.2,9.433999999999997
13.2,9.4,12.0,4.0,3,2,-1.7,6.3824
```