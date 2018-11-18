# svm

## Setup

Assuming you have `virtualenv` installed:
- `virtualenv venv && source venv/bin/activate`
- `pip install -r requirements.txt`
- `python3 naive-bayes.py --help`
```
$ ./naive_baiyes.py -h
usage: naive_baiyes.py [-h] [-l LIMIT] [-m MODEL] [-c]

optional arguments:
  -h, --help            show this help message and exit
  -l LIMIT, --limit LIMIT
                        Limit processed data
  -m MODEL, --model MODEL
                        Specify model file (pickle format)
  -c, --cache           Cache processed raw data
```
- `deactivate`

## Example

```
$ ./naive_baiyes.py
Running Naive-Bayes Classifier
Reading 1405 user(s) data: [########################################]
Finished reading data
Total number of user: 1405
Total number of comments: 74529

Running Naive-Bayes Classifier Training
Pre-processing 74529 of data: [########################################]
Finished pre-processing (74529 data)
Test-1: 77.06%
Test-2: 77.71%
Test-3: 77.31%
Test-4: 76.68%
Test-5: 77.00%
Test-6: 76.97%
Test-7: 76.77%
Test-8: 76.82%
Average accuracy: 77.04%

Classifying using trained Naive-Bayes model
===========================================

Insert phrase >>
```

## Reference

`https://scikit-learn.org/stable/modules/svm.html`