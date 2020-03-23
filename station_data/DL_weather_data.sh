# The station changed ID in 2013 so we have to make these two separate calls
for year in `seq 2003 2013`;
do 
  for month in `seq 1 12`; 
  do wget --content-disposition "https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=202&Year=${year}&Month=${month}&Day=14&timeframe=2&submit=Download+Data" 
  done;
done;
for year in `seq 2013 2019`;
do 
  for month in `seq 1 12`; 
  do wget --content-disposition "https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=51319&Year=${year}&Month=${month}&Day=14&timeframe=2&submit=Download+Data" 
  done;
done
