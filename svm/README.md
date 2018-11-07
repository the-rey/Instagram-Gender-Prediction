# svm

## Setup

- `virtualenv venv && source venv/bin/activate`
- `pip install -r requirements.txt`
- `python3 svm.py --help`
```
usage: svm.py [-h] [-l LIMIT] [-g GAMMA] [-k KERNEL]

optional arguments:
  -h, --help            show this help message and exit
  -l LIMIT, --limit LIMIT
                        Limit processed data
  -g GAMMA, --gamma GAMMA
                        Gamma value
  -k KERNEL, --kernel KERNEL
                        Kernel to use
```
- `deactivate`

## Example

```
$ python3 svm.py --limit 100 --gamma 1 --kernel linear
Running SVM Classifier
Reading data: [########################################]
Test-1
> Training model...
> Predicting test data...
> Accuracy: 58.33%
Test-2
> Training model...
> Predicting test data...
> Accuracy: 76.92%
Test-3
> Training model...
> Predicting test data...
> Accuracy: 53.85%
Test-4
> Training model...
> Predicting test data...
> Accuracy: 58.33%
Test-5
> Training model...
> Predicting test data...
> Accuracy: 75.00%
Test-6
> Training model...
> Predicting test data...
> Accuracy: 69.23%
Test-7
> Training model...
> Predicting test data...
> Accuracy: 69.23%
Test-8
> Training model...
> Predicting test data...
> Accuracy: 91.67%
=====================================
Avg. Accuracy: 69.07%
Elapsed time: 19.24s
```