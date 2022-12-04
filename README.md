# AntyAgenci Szczelnie Decyzyjni

Diagrams: https://demo.bpmn.io/

## Review B

https://forms.office.com/r/mXeXGpzSfz > maxlength="4000"

## Starting XMPP server

* Run `docker-compose up --build -d`
* If you start this first time, run `docker-compose exec xmpp /config/initdb.sh` to register some users

## Running example

### Install __SPADE__
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
```

### Run `main.py`
```sh
python main.py
```

You should see something like this:
```
  ~/dev/python/AASD_AntyAgenciSzczelnieDecyzyjni   main !1 ?7 ❯ python main.py                                                                                                                               3m 8s 🐍 AASDpy39  20:55:34
Agent starting . . .
Starting behaviour . . .
Counter: 0
Wait until user interrupts with ctrl+C
Counter: 1
Counter: 2
Counter: 3
^CStopping...
```

__WARNING__: If you have python **>= 3.10** you need to downgrade to **<= 3.9** as SPADE has some problems with itself.


