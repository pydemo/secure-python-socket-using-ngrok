# secure-python-socket-using-ngrok
SSL secure Python socket using ngrok

## Generate certs

```
python3 mk_certs.py
```
## Server
```
python3 ssl_server.py  6063
ngrok tunnel 'tcp://6.tcp.ngrok.io:14507' -> 'tcp://127.0.0.1:6063'
```
## Client
```
python3 ssl_client.py 0.tcp.ngrok.io 15957
```


## Test

![test](https://github.com/pydemo/secure-python-socket-using-ngrok/blob/main/images/test.JPG?raw=true)
