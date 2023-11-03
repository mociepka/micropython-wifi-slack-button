import machine
import utime as time
import network
import usocket as socket
import ussl as ssl
import ntptime

from helpers import unquote, get_http_response

OPEN_PIN =  machine.Pin(16, machine.Pin.OUT, value=0)

def connect_to_wifi(ssid, password, reconnects=20):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    retry_count = 0
    print(ssid, password, "Credentials")
    print("Awaitable networks", [n[0] for n in wlan.scan()])
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print("Connecting")
        if retry_count > reconnects:
            wlan.active(False)
            return None
        retry_count += 1
        time.sleep(1)
    print("Connected")
    return wlan


def get_settings():
    try:
        with open("settings.txt", "r") as conn:
            settings = {
                "ssid": conn.readline().replace("\n", ""),
                "password": conn.readline().replace("\n", ""),
                "token": conn.readline().replace("\n", ""),
            }
    except OSError:
        settings = {"ssid": "", "password": ""}
    return settings

def read_full_http_body(sock):
    cl_file = sock.makefile("rb", 0)
    content_length = 0
    body = b""
    while True:
        # read headers
        line = cl_file.readline()
        # search for content length
        if b"Content-Length: " in line:
            content_length = line.split(b"Content-Length: ")[1].strip()
            if content_length.isdigit():
                content_length = int(content_length)
            else:
                break
        if line == b"\r\n" and content_length:
            body = sock.read(content_length)
            break
        elif line == b"\r\n":
            break
    return body


def run_server(settings):
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]

    s = socket.socket()
    # s.settimeout(10)
    s.bind(addr)
    s.listen(1)

    print("listening on", addr)

    # waiting for connections
    while True:
        rws, addr = s.accept()
        print("client connected from", addr)
        content_length = 0
        first_line = None
        post_data = None

        body = read_full_http_body(rws)

        if body:
            post_data = [s2 for s1 in body.split(b"&") for s2 in s1.split(b";")]
            post_data = {
                query.split(b"=")[0]
                .decode(): unquote(query.split(b"=")[1])
                .decode("utf-8")
                for query in post_data
            }
        else:
            post_data = {}
        print(post_data)
        # print button
        if "token" in post_data and post_data["token"] == settings["token"]:
            rws.sendall(get_http_response("Release The Kraken!"))
            print("Button down")
            OPEN_PIN.value(1)
            time.sleep_ms(500)
            rws.close()
            time.sleep_ms(500)
            OPEN_PIN.value(0)
            print("Button up")
        else:
            rws.sendall(get_http_response("Wrong token", 403))
            rws.close()
            time.sleep_ms(500)


def main():
    settings = get_settings()
    print(settings, "Settings")
    if settings["ssid"]:
        wlan = connect_to_wifi(settings["ssid"].rstrip(), settings["password"].rstrip())
    else:
        wlan = None
    if wlan:
        print("network config:", wlan.ifconfig())
        # set device time
        ntptime.settime()
        # run command server
        run_server(settings)
    print("No network")


try:
    main()
except Exception as e:
    print(e)
