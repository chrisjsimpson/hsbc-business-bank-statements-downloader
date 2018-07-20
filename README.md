## Setup 

- you need to `pip install -U selenium`
- also, this uses geckodriver, which is Firefox. 
- You need to download the geckodriver, binary and put it in your path e. g., 
download it and place it in /usr/bin or /usr/local/bin. https://github.com/mozilla/geckodriver/releases/tag/v0.21.0

## Run it

`python main.py`

It will ask for a code, this is the code the smart card reader HSBC bank users
use to login to their online bank, with their pin number; it generates a 
time-bound login key. 

You'll note the `memorableAnswerelm` is empty, and usually the password (fetch
this from somehwere , don't hardcode it).


