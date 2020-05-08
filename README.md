# COVID-DE-19
Code to analyse time series data in COVID-19 around Delaware

.>  csv_to_time_series.py
   Generate time series plots.
   
   List of Keyword Arguments
   -------------------------
   state ['us', 'de', 'ny', 'nj', 'md']
   
   -cf, --csv_file: Optional location of csv file. If none supplied, this is taken from hard-coded presets.
   
   Sample calls: 
   csv_to_time_series.py md
   python csv_to_time_series.py md -cf us-states.csv
