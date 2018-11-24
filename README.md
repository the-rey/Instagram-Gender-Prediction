# Thanos

Know your Instagram followers gender!

## Getting Started

```
export IG_USERNAME=
export IG_PASSWORD=
```

Assuming you have `virtualenv` installed:

- `virtualenv venv && source venv/bin/activate`
- `pip install -r requirements.txt`
- `cd thanos && python thanos.py`

```
$ ./thanos.py -h
usage: thanos.py [-h] [-p PORT] [-o HOST] [-d] [-e ENV] [-s SECRET]

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Specifies the port to listen on
  -o HOST, --host HOST  Specifies the interface address to listen on
  -d, --debug           Specifies the debug mode
  -e ENV, --env ENV     Specifies the env for flask to run
  -s SECRET, --secret SECRET
                        Specifies the session secret key
```

## Under construction!