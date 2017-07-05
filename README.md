# SDRScraper
Pulls down and stores data from the DTCC SDR repository. May support ther sources in the future

# Game plan - Sourcing the data
Monitor the slice html files which list all the recent history for the last 24 hours or so
Keep track of which slice files (the zip links contained within the slice html files) have been downloaded already
Download any new zip files we haven't seen before, parse the data and store it
Store data in a time-series db (e.g. Influx)

# Game plan - Accessing the data
Create a REST API on top of it to allow for querying. 

Allow anyone interested in updates to subscribe. Requires them to provide a REST end point, their email and a password
REST end point will be called each time a new trade is found by the scraper

