# Fork of nchah/github-traffic-stats

Get statistics on web traffic to your GitHub repositories.

## Python CLI

Python CLI tool to get web traffic stats on the command line using the GitHub API.

A few use cases to show why this may be useful.

- Checking the volume of traffic to all of your repos. Monitor sudden spikes in interest or any general patterns.
- Storing the traffic stats for future reference.

### Dependencies

- Requests ([kennethreitz/requests](https://github.com/kennethreitz/requests))

There are a number of GitHub [libraries](https://developer.github.com/libraries/) for Python and other languages, although they may not support the Repository Traffic API (announced on August 15, 2016).

### Run

Run on the command line with either `python` or `python3`.

### Get Stats for Clones

```
$ python github-traffic-stats.py 'hocinebendou' 'baobab.lims' 'clones' 'save_csv'
Password:* (passwords are hidden)
github-traffic-stats
Date        Clones   Unique visitors
Totals      18       15
2017-07-11  2        2
2017-07-14  1        1
2017-07-15  2        1
2017-07-16  1        1
2017-07-17  1        1
2017-07-18  4        3
2017-07-19  2        2
2017-07-21  4        4
2017-07-24  1        1
...

```

Traffic data stored in CSV files with columns:
```
repository_name, date, clones, unique_visitors
```

```
$ python github-traffic-stats.py 'hocinebendou' 'baobab.lims' 'views' 'save_csv'
Password:* (passwords are hidden)
github-traffic-stats
Date        Views   Unique visitors
Totals      452      21
2017-07-11  26       2
2017-07-12  27       2
2017-07-13  8        1
2017-07-14  22       2
2017-07-15  28       2
2017-07-16  6        2
2017-07-17  8        1
2017-07-18  20       2
2017-07-19  63       9
2017-07-20  8        1
2017-07-21  30       5
2017-07-22  13       1
2017-07-23  3        1
2017-07-24  73       5
2017-07-25  117      5
...

```

Traffic data stored in CSV files with columns:
```
repository_name, date, views, unique_visitors
```

Separate CSVs are created for each run of the script.
To merge and only preserve the unique data points, run:

```
$ bash bash/merge-csv.sh [folder_with_CSVs]
```


## Documentation

A list of the references used for this project.

- [Preview the Original Repository](https://github.com/nchah/github-traffic-stats.git)

