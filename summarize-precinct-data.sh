#!/bin/bash -ex
ST='AZ'
st='az'

ogr2ogr -f CSV \
    -sql 'SELECT FID,CDE_COUNTY,PCTNUM,PRECINCTNA,G20PREDBID,G20PRERTRU from '$st'_2020' \
    "/tmp/${ST}-precincts.csv" "/vsizip/VEST/${st}_2020.zip"

ogr2ogr -f CSV \
    -sql 'SELECT precinct,GEOID20,"Population 2020","Citizen Voting-Age Population 2019","Black Citizen Voting-Age Population 2019","Asian Citizen Voting-Age Population 2019","Hispanic Citizen Voting-Age Population 2019","US President 2020 - DEM","US President 2020 - REP" from "assembled-state-'$ST'"' \
    "/tmp/${ST}-block.csv" "assembled-state-${ST}.geojson"

csvsql -I \
    --query 'select precinct, SUM("Population 2020") as "Population 2020", SUM("Citizen Voting-Age Population 2019") as "Citizen Voting-Age Population 2019", SUM("Black Citizen Voting-Age Population 2019") as "Black Citizen Voting-Age Population 2019", SUM("Asian Citizen Voting-Age Population 2019") as "Asian Citizen Voting-Age Population 2019", SUM("Hispanic Citizen Voting-Age Population 2019") as "Hispanic Citizen Voting-Age Population 2019", SUM("US President 2020 - DEM") as "US President 2020 - DEM", SUM("US President 2020 - REP") as "US President 2020 - REP" FROM "'$st'-block" GROUP BY precinct' \
    "/tmp/${ST}-block.csv" \
    > "/tmp/${ST}-block-grouped.csv"

csvstat --sum -c 'G20PREDBID,G20PRERTRU' "/tmp/${ST}-precincts.csv"
csvstat --sum -c 'Population 2020' "/tmp/${ST}-block.csv"
csvstat --sum -c 'Population 2020,US President 2020 - DEM,US President 2020 - REP' "/tmp/${ST}-block-grouped.csv"

csvjoin -I -c FID,precinct --left "/tmp/${ST}-precincts.csv" "/tmp/${ST}-block-grouped.csv" \
    > "/tmp/${ST}-precinct-populations.csv"
