# Wifi slack button pusher

Simple project for a slack command which press the button.

Wifi settings with slack auth token.

For more info about token and how too connect app:
https://api.slack.com/interactivity/slash-commands

## how to setup ESP

Micropython:
* http://micropython.org/download/esp8266/
* https://nodemcu.readthedocs.io/en/release/flash/#nodemcu-pyflasher
* https://github.com/marcelstoer/nodemcu-pyflasher/releases
* https://docs.micropython.org/en/latest/esp8266/quickref.html#quick-reference-for-the-esp8266

## how to copy python files to ESP

https://github.com/dhylands/rshell

```
rshell -p COM3
ls /pyboard
repl
cp helpers.py main.py /pyboard/
```


## Slack command example:

* https://api.slack.com/interactivity/slash-commands

```
curl -X POST http://mociepka.eu.ngrok.io/
   -H "Content-Type: application/x-www-form-urlencoded"
   -d "token=xxxxxxxxxxyRAWp6PvZt4A0g&team_id=T0001&team_domain=example&enterprise_id=E0001&enterprise_name=Globular%20Construct%20Inc&channel_id=C2147483705&channel_name=test&user_id=U2147483697&user_name=Steve&command=/weather&text=94070&response_url=https://hooks.slack.com/commands/1234/5678&trigger_id=13345224609.738474920.8088930838d88f008e0&api_app_id=A123456"
```
