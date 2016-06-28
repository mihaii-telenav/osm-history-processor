## Openstreetmap History Processor
Python port of [processing-osm-history](https://github.com/Rub21/processing-osm-history/)

### Installation

```
git clone https://github.com/baditaflorin/osm-history-processor.git
cd osm-history-processor
pip install -r requirements.txt
```

### Usage

The script it`s hardcoded to work with only 5 days. It will give an error if you try to download for 6 days or just 4 days.

`python peer_review.py date days`, for example - to find changes starting June 24, 2015 and 4 days back in time run `python peer_review.py 2016-06-24 4` 
In total will download everything from 20 June until 24 of June (5 days)
