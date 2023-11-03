import machine

RED = 0
GREEN = 1
BLUE = 2

# RGB = (
#     machine.Pin(15, machine.Pin.OUT),
#     machine.Pin(13, machine.Pin.OUT),
#     machine.Pin(12, machine.Pin.OUT),
# )
RGB = (
    machine.Pin(15, machine.Pin.OUT),
    machine.Pin(12, machine.Pin.OUT),
    machine.Pin(13, machine.Pin.OUT),
)
[p.off() for p in RGB]


def blink_led(color=GREEN, freq=1, duty=512):
    def decorator(function):
        def wrapper(*args, **kwargs):
            diode = RGB[color]
            pwm = machine.PWM(diode, freq, duty)
            result = function(*args, **kwargs)
            pwm.deinit()
            diode.init(diode.OUT)
            diode.off()
            return result

        return wrapper

    return decorator


def deep_sleep(minutes=10):
    # configure RTC.ALARM0 to be able to wake the device
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    # set RTC.ALARM0 to fire after Xmilliseconds, waking the device
    rtc.alarm(rtc.ALARM0, minutes * 60_000)
    # put the device to sleep
    print("Deep sleep")
    machine.deepsleep()


_hextobyte_cache = None

def get_http_response(body, status_code=200):
    headers = "HTTP/1.0 %d OK\r\nContent-type: text/html\r\n" % status_code
    headers += "Content-Length: %d\r\n\r\n" % len(body)
    return headers + body


def unquote(string):
    """unquote('abc%20def') -> b'abc def'."""
    global _hextobyte_cache

    # Note: strings are encoded as UTF-8. This is only an issue if it contains
    # unescaped non-ASCII characters, which URIs should not.
    if not string:
        return b""

    if isinstance(string, str):
        string = string.encode("utf-8")

    bits = string.split(b"%")
    if len(bits) == 1:
        return string

    res = [bits[0]]
    append = res.append

    # Build cache for hex to char mapping on-the-fly only for codes
    # that are actually used
    if _hextobyte_cache is None:
        _hextobyte_cache = {}

    for item in bits[1:]:
        try:
            code = item[:2]
            char = _hextobyte_cache.get(code)
            if char is None:
                char = _hextobyte_cache[code] = bytes([int(code, 16)])
            append(char)
            append(item[2:])
        except KeyError:
            append(b"%")
            append(item)

    return b"".join(res)
