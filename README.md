# HSBC Business CSV Statement Downloader

Automatically download all statements in csv format.
Defaults to top level account only

Works well with: https://github.com/chrisjsimpson/hsbc-business-csv-statement-processor
to process all of the statements and glean meaningful info (total income/out per 
year/month) etc

## Setup 

- you need:
  - `pip install -r requirements.txt`
- Firefox installed
- geckodriver
- You need to download the geckodriver, binary and put it in your path e.g.:
  - download geckodriver  https://github.com/mozilla/geckodriver/releases/tag/v0.21.0
  - place geckodriver in /usr/bin or /usr/local/bin.
  - or current directory, and add it to your path: e.g: `export PATH=$PATH:./`

## Run it

`python main.py`

It will ask for a code, this is the code the smart card reader HSBC bank users
use to login to their online bank, with their pin number; it generates a 
time-bound login key. 

You'll note the `memorableAnswerelm` is empty, and usually the password (fetch
this from somehwere , don't hardcode it).


