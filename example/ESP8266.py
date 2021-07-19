import convert
import DigitalToneControl as dtc
from machine import I2C


i2c = I2C()

def _i2c_send(*data):
    addr, *data = data
    send = []
    for a in data:
        b = (a >> 3) & 15
        c = a & 15
        send.append(convert.DATA[b][c])
    i2c.writeto(addr, send)
    del addr, data, send, a, b, c

tone = dtc.PT2313()
# tone = dtc.PT2314()
# tone = dtc.TDA7303()
# tone = dtc.TDA7309()
# tone = dtc.TDA7318()
# tone = dtc.TDA7430()
# tone = dtc.TDA7431()
# tone = dtc.TDA7432()
# tone = dtc.TDA7433()
# tone = dtc.TDA7434()
# tone = dtc.TDA7438()
# tone = dtc.TDA7439()
# tone = dtc.TDA7440()
# tone = dtc.TDA7442()
# tone = dtc.TDA7443()

tone.Write(_i2c_send)
tone.input(1)           # 1 ~ MAX_INPUT 
tone.volume(0)          # 0 ~ 63+
tone.balance_all(0)     # 0 ~ 63+
