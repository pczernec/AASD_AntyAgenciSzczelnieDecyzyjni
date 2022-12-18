# AntyAgenci Szczelnie Decyzyjni

Diagrams: https://demo.bpmn.io/

## Review B

https://forms.office.com/r/mXeXGpzSfz > maxlength="4000"

## Starting XMPP server and agents

Run `docker-compose up --force-recreate --build --remove-orphans`

## Running example

__WARNING__: If you have python **>= 3.10** you need to downgrade to **<= 3.9**, because `TypeError: As of 3.10, the *loop* parameter was removed from Lock() since it is no longer necessary`.

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

