
class _DTC_OUT:
    ATT_LF = 0
    ATT_RF = 1
    ATT_LR = 2
    ATT_RR = 3

class _DTC_SURROUND:
    SIMULATED = 0
    MUSIC = 1
    OFF = 2
    FLAT = 3
    MOVIE = 4
    PSEUDO = 5

class _DTC_SWITCH:
    DISABLE = 0
    ENABLE = 1

class DigitalToneControl:
    _addr = 0
    _max_input = 0
    _max_data = 0
    _data = []
    _Write = None

    DTC_OUT = _DTC_OUT()
    DTC_SURROUND = _DTC_SURROUND()
    DTC_SWITCH = _DTC_SWITCH()

    def __init__(self) -> None:
        for a in range(self._max_data):
            self._data.append(0)

    def Write(self, data):
        self._Write = data

    def constrain(self, a, b, c):
        if a < b: return b
        elif a > c: return c
        return a

    def _SendWrite(self, data):
        a = [self._addr]
        if type(data) == list:
            for b in data:
                a.append(b)
        else: a.append(data)
        self._Write(a)

class PT2313(DigitalToneControl):
    _addr = 136
    _max_input = 3
    _max_data = 8

    def __init__(self) -> None:
        super().__init__()

    def volume(self, data):
        data = self.constrain(data, 0, 63)

        if self._data[0] == data: return
        self._data[0] = data
        self._SendWrite(self._data[0])

    def bass(self, data):
        data = self.constrain(data, -7, 7)
        if data <= 0: data += 7
        else: data = 14 - data

        if (self._data[6] & 15) == data: return
        self._data[6] = data | (6<<4)
        self._SendWrite(self._data[6])

    def treble(self, data):
        data = self.constrain(data, -7, 7)
        if data <= 0: data += 7
        else: data = 14 - data

        if (self._data[7] & 15) == data: return
        self._data[7] = data | (7<<4)
        self._SendWrite(self._data[7])

    def balance_all(self, data):
        self.balance(self.DTC_OUT.ATT_LF, data)
        self.balance(self.DTC_OUT.ATT_RF, data)
        self.balance(self.DTC_OUT.ATT_LR, data)
        self.balance(self.DTC_OUT.ATT_RR, data)

    def balance(self, mode, data):
        mode = self.constrain(mode, 0, 3)
        data = self.constrain(data, 0, 30)
        a = 0; b = 0
        
        if mode == self.DTC_OUT.ATT_LF: 
            a = 1
            b = 5
        elif mode == self.DTC_OUT.ATT_LR:
            a = 2
            b = 6
        elif mode == self.DTC_OUT.ATT_LR:
            a = 3
            b = 7
        elif mode == self.DTC_OUT.ATT_LR:
            a = 4
            b = 8
        else: return
        
        if (self._data[a] & 31) == data: return 
        self._data[a] = data | (b<<5)
        self._SendWrite(self._data[a])

    def input(self, data):
        data = self.constrain(data, 1, self._max_input) - 1

        if (self._data[5] & 3) == data: return
        self._data[5] &= ~(3)
        self._data[5] |= data | (1<<6)
        self._SendWrite(self._data[5])

    def loudness(self, data):
        data = 3 - self.constrain(data, 0, 3)

        if ((self._data[5]>>3) & 3) == data: return
        self._data[5] &= ~(3<<3)
        self._data[5] |= (data<<3) | (1<<6)
        self._SendWrite(self._data[5])

    def modeLoudness(self, data):
        data = self.constrain(data, 0, 1)

        if ((self._data[5]>>2) & 1) == data: return
        self._data[5] &= ~(1<<2)
        self._data[5] |= (data<<2)
        self._SendWrite(self._data[5])

    def mute_all(self, data):
        self.mute(self.DTC_OUT.ATT_LF, data)
        self.mute(self.DTC_OUT.ATT_RF, data)
        self.mute(self.DTC_OUT.ATT_LR, data)
        self.mute(self.DTC_OUT.ATT_RR, data)

    def mute(self, mode, data):
        mode = self.constrain(mode, 0, 3)
        data = self.constrain(data, 0, 1)
        a = 0; b = 0
        
        if mode == self.DTC_OUT.ATT_LF: 
            a = 1
            b = 5
        elif mode == self.DTC_OUT.ATT_LR:
            a = 2
            b = 6
        elif mode == self.DTC_OUT.ATT_LR:
            a = 3
            b = 7
        elif mode == self.DTC_OUT.ATT_LR:
            a = 4
            b = 8
        else: return

        if data == self.DTC_SWITCH.ENABLE: self._SendWrite(31 | (b<<5))
        else: self._SendWrite(self._data[a])

class PT2314(PT2313):
    def __init__(self):
        super().__init__()

    def balance(self, mode, data):
        mode = self.constrain(mode, 0, 3)
        data = self.constrain(data, 0, 30)
        a = 0; b = 0
        
        if mode == self.DTC_OUT.ATT_LF: 
            a = 1
            b = 5
        elif mode == self.DTC_OUT.ATT_LR:
            a = 2
            b = 6
        else: return
        
        if (self._data[a] & 31) == data: return 
        self._data[a] = data | (b<<5)
        self._SendWrite(self._data[a])

    def mute(self, mode, data):
        mode = self.constrain(mode, 0, 3)
        data = self.constrain(data, 0, 1)
        a = 0; b = 0
        
        if mode == self.DTC_OUT.ATT_LF: 
            a = 1
            b = 5
        elif mode == self.DTC_OUT.ATT_LR:
            a = 2
            b = 6
        else: return

        if data == self.DTC_SWITCH.ENABLE: self._SendWrite(31 | (b<<5))
        else: self._SendWrite(self._data[a])

class TDA7303(PT2313):
    def __init__(self):
        super().__init__()

class TDA7309(DigitalToneControl):
    _addr = 24
    _max_input = 4
    _max_data = 4

    def __init__(self):
        super().__init__()

    def volume(self, data):
        data = self.constrain(data, 0, 95)
        
        if self._data[0] == data: return
        self._data[0] = data
        self._SendWrite(self._data[0])

    def input(self, data):
        data = self.constrain(data, 1, self._max_input) - 1

        if (self._data[2] & 3) == data: return
        self._data[2] = data | (5<<5)
        self.Write(self._data[2])

    def channel(self, data):
        data = self.constrain(data, 0, 2)
        
        if (self._data[3] & 3) == data: return
        self._data[3] &= ~(3)
        self._data[3] |= data | (6<<5)
        self._SendWrite(self._data[3])

    def loudness(self, data):
        data = self.constrain(data, 0, 1)

        if ((self._data[1]>>3) & 1) == data: return
        self._data[1] &= ~(1<<3)
        self._data[1] |= (data<<3) | (4<<5)
        self._SendWrite(self._data[1])

    def modeLoudness(self, data):
        data = self.constrain(data, 0, 1)
        
        if ((self._data[1]>>2) & 1) == data: return
        self._data[1] &= ~(1<<2)
        self._data[1] |= (data<<2) | (4<<5)
        self._SendWrite(self._data[1])

    def mute(self, data):
        data = self.constrain(data, 0, 2)
        
        if (self._data[1] & 3) == data: return
        self._data[1] &= ~(3)
        self._data[1] |= data | (4<<5)
        self._SendWrite(self._data[1])

class TDA7318(PT2313):
    _max_input = 4

    def __init__(self):
        super().__init__()

    def modeLoudness(self, data):
        return

# class TDA7340(DigitalToneControl):
#     def __init__(self):
#         super().__init__()

# class TDA7429(DigitalToneControl):
#     def __init__(self):
#         super().__init__()

class TDA7430(DigitalToneControl):
    _addr = 128
    _max_data = 10
    _max_input = 4

    def __init__(self):
        super().__init__()

    def volume(self, data):
        data = self.constrain(data, 0, 63)
        
        if (self._data[0] & 63) == data: return
        self._data[0] &= ~(63)
        self._data[0] |= data
        self._SendWrite([0, self._data[0]])

    def bass(self, data): 
        data = self.constrain(data, -7, 7)

        if data <= 0: data += 7
        else: data = 14 - data

        if (self._data[3] & 15) == data: return
        self._data[3] &= ~(15)
        self._data[3] |= data
        self._SendWrite([5, self._SendWrite[3]])

    def middle(self, data):
        data = self.constrain(data, -7, 7)

        if data <= 0: data += 7
        else: data = 14 - data

        if (self._data[4] & 15) == data: return
        self._data[4] &= ~(15)
        self._data[4] |= data
        self._SendWrite([4, self._data[4]])

    def treble(self, data):
        data = self.constrain(data, -7, 7)

        if data <= 0: data += 7
        else: data = 14 - data

        if ((self._data[4]>>4) & 15) == data: return
        self._data[4] &= ~(15<<4)
        self._data[4] |= (data<<4)
        self._SendWrite([4, self._data[4]])

    def balance_all(self, data):
        self.balance(self.DTC_OUT.ATT_LF, data)
        self.balance(self.DTC_OUT.ATT_RF, data)
        self.balance(self.DTC_OUT.ATT_LR, data)
        self.balance(self.DTC_OUT.ATT_RR, data)

    def balance(self, mode, data): 
        mode = self.constrain(mode, 0, 5)
        data = self.constrain(mode, 0, 79)
        a = 0

        if data == self.DTC_OUT.ATT_LF: a = 5
        elif data == self.DTC_OUT.ATT_LR: a = 6
        elif data == self.DTC_OUT.ATT_RF: a = 7
        elif data == self.DTC_OUT.ATT_RR: a = 8
        else: return

        if self._data[a] == data: return
        self._data[a] = data
        self._SendWrite([a, self._data[a]])

    def input(self, data): 
        data = self.constrain(data, 1, self._max_input) - 1

        if ((self._data[9]>>1) & 3) == data: return
        self._data[9] &= ~(3<<1)
        self._data[9] |= (data<<1)
        self._SendWrite([9, self._data[9]])

    def naturalBase(self, data): 
        data = self.constrain(data, 0, 1)

        if data == self.DTC_SWITCH.ENABLE: data = 0
        elif data == self.DTC_SWITCH.DISABLE: data = 1
        else: return

        if ((self._data[4]>>4) & 1) == data: return
        self._data[4] &= ~(1<<4)
        self._data[4] |= (data<<4)
        self._SendWrite([4, self._data[4]])

    def rearSwitch(self, data):
        data = self.constrain(data, 0, 1)

        if data == self.DTC_SWITCH.ENABLE: data = 0
        elif data == self.DTC_SWITCH.DISABLE: data = 1
        else: return

        if ((self._data[0]>>6) & 1) == data: return
        self._data[0] &= ~(1<<6)
        self._data[0] |= (data<<6)
        self._SendWrite([0, self._data[0]])

    def modeSurround(self, data): 
        data = self.constrain(data, 0, 4)
        b = 0

        if data == self.DTC_SURROUND.SIMULATED: b = 0
        elif data == self.DTC_SURROUND.MUSIC: b = 1
        elif data == self.DTC_SURROUND.OFF: b = 2
        elif data == self.DTC_SURROUND.MOVIE: b = 3
        elif data == self.DTC_SURROUND.FLAT: b = 4
        else: return

        if (self._data[1] & 7) == b: return
        self._data[1] &= ~(7)
        self._data[1] |= b
        self._SendWrite([1, self._data[1]])

    def voiceCanceller(self, data): 
        data = self.constrain(data, 0, 15)

        if ((self._data[1]>>3) & 15) == data: return
        self._data[1] &= ~(15<<3)
        self._data[1] |= (data<<3)
        self._SendWrite([1, self._data[1]])

    def effectControl(self, data): 
        data = self.constrain(data, 0, 15)

        if ((self._data[9] >> 3) & 15) == data: return
        self._data[9] &= ~(15<<3)
        self._data[9] |= (data<<3)
        self._SendWrite([9, self._data[9]])

    def phaseResistor_all(self, data):
        self.phaseResistor(0, data)
        self.phaseResistor(1, data)
        self.phaseResistor(2, data)
        self.phaseResistor(3, data)

    def phaseResistor(self, mode, data): 
        mode = self.constrain(mode, 0, 3)
        data = self.constrain(data, 1, 4) - 1

        if ((self._data[2] >> (mode * 2)) & 3) == data: return
        self._data[2] &= ~(3 << (mode * 2))
        self._data[2] |= (data << (mode * 2))
        self._SendWrite([2, self._data[2]])
    
    def phaseResistor_set(self, data, data1, data2, data3):
        self.phaseResistor(0, data)
        self.phaseResistor(1, data1)
        self.phaseResistor(2, data2)
        self.phaseResistor(3, data3)

    def selectorRecOut_all(self, data): 
        self.selectorRecOut(self.DTC_OUT.ATT_LF, data)
        self.selectorRecOut(self.DTC_OUT.ATT_RF, data)

    def selectorRecOut(self, mode, data): 
        mode = self.constrain(mode, 0, 3)
        data = self.constrain(data, 0, 1)
        b = 0

        if mode == self.DTC_OUT.ATT_LF: b = 0
        elif mode == self.DTC_OUT.ATT_LR: b = 2
        else: return

        if ((self._data[9] >> (3+b)) & 3) == data: return
        self._data[9] &= ~(3 << (3+b))
        self._data[9] |= (data << (3+b))
        self._SendWrite([9, self._data[9]])

    def mute_all(self, data): 
        self.mute(self.DTC_OUT.ATT_LF, data)
        self.mute(self.DTC_OUT.ATT_RF, data)
        self.mute(self.DTC_OUT.ATT_LR, data)
        self.mute(self.DTC_OUT.ATT_RR, data)

    def mute(self, mode, data): 
        mode = self.constrain(mode, 0, 5)
        data = self.constrain(mode, 0, 1)
        a = 0

        if data == self.DTC_OUT.ATT_LF: a = 5
        elif data == self.DTC_OUT.ATT_LR: a = 6
        elif data == self.DTC_OUT.ATT_RF: a = 7
        elif data == self.DTC_OUT.ATT_RR: a = 8
        else: return

        if data == self.DTC_SWITCH.ENABLE: self._SendWrite([a, 80])
        else: self._SendWrite([a, self._data[a]])

class TDA7431(TDA7430):
    _max_input = 1

    def __init__(self):
        super().__init__()

class TDA7433(DigitalToneControl):
    _addr = 138
    _max_data = 7
    _max_input = 3

    def __init__(self):
        super().__init__()

    def volume(self, data):
        data = self. constrain(data, 0, 111)

        if self._data[1] == data: return
        self._data[1] = data
        self._SendWrite([1, self._data[1]])

    def bass(self, data): 
        data = self.constrain(data, -9, 9)
        a = 2; b = 0; c = 0;

        if data < -7:
            data = 1 - (9 + data)
            b  = 0
        elif data <= 0: 
            data += 7
            b = 1
        elif data > 7: 
            data = 1 - (9 - data)
            b = 0
        elif data > 0:
            data = 14 - data
            b = 1
        else: return

        if ((self._data[c]>>4) & 1) == b: return
        elif ((self._data[a]>>4) & 15) == data: return

        self._data[c] &= ~(1<<4)
        self._data[c] |= (b<<4)
        self._SendWrite([c, self._data[c]])

        self._data[a] &= ~(15<<4)
        self._data[a] |= (b<<4)
        self._SendWrite([a, self._data[a]])

    def treble(self, data): 
        data = self.constrain(data, -7, 7)

        if data <= 0: data += 7
        else: data = 14 - data

        if (self._data[2] & 15) == data: return
        self._data[2] &= ~(15)
        self._data[2] |= data
        self._SendWrite([2, self._data[2]])

    def balance_all(self, data):
        self.balance(self.DTC_OUT.ATT_LF, data)
        self.balance(self.DTC_OUT.ATT_RF, data)
        self.balance(self.DTC_OUT.ATT_LR, data)
        self.balance(self.DTC_OUT.ATT_RR, data)

    def balance(self, mode, data):
        mode = self.constrain(mode, 0, 4)
        data = self.constrain(data, 0, 31)
        a = 0

        if data == self.DTC_OUT.ATT_LF: a = 3
        elif data == self.DTC_OUT.ATT_LR: a = 4
        elif data == self.DTC_OUT.ATT_RF: a = 5
        elif data == self.DTC_OUT.ATT_RR: a = 6
        else: return

        if self._data[a] == data: return
        self._data[a] = data
        self._SendWrite([a, self._data[a]])

    def input(self, data): 
        data = 3 - self.constrain(data, 1, self._max_input)

        if (self._data[0] & 3) == data: return
        self._data[0] &= ~(3)
        self._data[0] |= data
        self._SendWrite([0, self._data[0]])

    def symmetrical(self, data):
        data = self.constrain(data, 0, 1)

        if ((self._data[0]>>3) & 1) == data: return
        self._data[0] &= ~(1<<3)
        self._data[0] |= (data<<3)
        self._SendWrite([0, self._data[0]])

    def mute_all(self, data):
        self.mute(self.DTC_OUT.ATT_LF, data)
        self.mute(self.DTC_OUT.ATT_RF, data)
        self.mute(self.DTC_OUT.ATT_LR, data)
        self.mute(self.DTC_OUT.ATT_RR, data)

    def mute(self, mode, data):
        mode = self.constrain(mode, 0, 4)
        data = self.constrain(data, 0, 1)
        a = 0

        if data == self.DTC_OUT.ATT_LF: a = 3
        elif data == self.DTC_OUT.ATT_LR: a = 4
        elif data == self.DTC_OUT.ATT_RF: a = 5
        elif data == self.DTC_OUT.ATT_RR: a = 6
        else: return

        if data == self.DTC_SWITCH.ENABLE: self._SendWrite([a, 32])
        else: self._SendWrite([a, self._data[a]])

class TDA7432(TDA7433):
    _max_data = 8
    _max_input = 2

    def __init__(self):
        super().__init__()

    def volume(self, data):
        data = self.constrain(data, 0, 111)

        if (self._data[1] & 127) == data: return
        self._data[1] = data | (1<<127)
        self._SendWrite([1, self._data[1]])

    def input(self, data):
        data = self.constrain(data, 1, self._max_input) - 1
        data *= 2

        if (self._data[0] & 3) == data: return
        self._data[0] &= ~(3)
        self._data[0] |= data
        self._SendWrite([0, self._data[0]])

    def loudness(self, data):
        data = self.constrain(data, 0, 15)

        if self._data[7] == data: return
        self._data[7] = data
        self._SendWrite([7, self._data[7]])
    
class TDA7434(TDA7432):
    _max_input = 3

    def __init__(self):
        super().__init__()

class TDA7438(DigitalToneControl):
    _addr = 136
    _max_data = 8
    _max_input = 3
    
    def __init__(self):
        super().__init__()

    def volume(self, data):
        data = self.constrain(data, 0, 47)

        if self._data[2] == data: return
        self._data[2] = data
        self._SendWrite([2, self._data[2]])

    def bass(self, data):
        data = self.constrain(data, -7, 7)
        if data <= 0: data += 7
        else: data = 14 - data

        if self._data[3] == data: return
        self._data[3] = data
        self._SendWrite([3, self._data[3]])

    def middle(self, data):
        data = self.constrain(data, -7, 7)
        if data <= 0: data += 7
        else: data = 14 - data

        if self._data[4] == data: return
        self._data[4] = data
        self._SendWrite([4, self._data[4]])

    def treble(self, data):
        data = self.constrain(data, -7, 7)
        if data <= 0: data += 7
        else: data = 14 - data

        if self._data[5] == data: return
        self._data[5] = data
        self._SendWrite([5, self._data[5]])

    def balance_all(self, data):
        self.balance(self.DTC_OUT.ATT_LF, data)
        self.balance(self.DTC_OUT.ATT_RF, data)

    def balance(self, mode, data):
        mode = self.constrain(mode, 0, 3)
        data = self.constrain(data, 0, 79)
        a = 0

        if data == self.DTC_OUT.ATT_LF: a = 6
        elif data == self.DTC_OUT.ATT_RF: a = 7
        else: return

        if self._data[a] == data: return
        self._data[a] = data
        self._SendWrite([a, self._data[a]])

    def input(self, data):
        data =  3 - self.constrain(data, 1, self._max_input) - 1
        if data == 2: data = 0
        else: data = 4 - data

        if self._data[0] == data: return
        self._data[0] = data
        self._SendWrite([0, self._data[0]])

    def gain(self, data):
        data = self.constrain(data, 0, 15)

        if self._data[1] == data: return
        self._data[1] = data
        self._SendWrite([1, self._data[1]])

    def mute_all(self, data): 
        self.mute(self.DTC_OUT.ATT_LF, data)
        self.mute(self.DTC_OUT.ATT_RF, data)

    def mute(self, mode, data):
        mode = self.constrain(mode, 0, 3)
        data = self.constrain(data, 0, 1)
        a = 0

        if data == self.DTC_OUT.ATT_LF: a = 6
        elif data == self.DTC_OUT.ATT_RF: a = 7
        else: return

        if data == self.DTC_SWITCH.ENABLE: self._SendWrite([a, 80])
        else: self._SendWrite([a, self._data[a]])

class TDA7439(TDA7438):
    _max_input = 4

    def __init__(self):
        super().__init__()

    def input(self, data):
        data = self.constrain(data, 1, self._max_input) - 1

        if self._data[0] == data: return
        self._data[0] = data
        self._SendWrite([0, self._data[0]])

class TDA7440(TDA7439):
    def __init__(self):
        super().__init__()

    def middle(self, data): pass

class TDA7442(DigitalToneControl):
    _addr = 128
    _max_data = 10
    _max_input = 4

    def __init__(self):
        super().__init__()

    def volume(self, data):
        data = self.constrain(data, 0, 63)
        
        if self._data[0] == data: return
        self._data[0] = data
        self._SendWrite([0, self._data[0]])

    def bass(self, data): 
        data = self.constrain(data, -7, 7)

        if data <= 0: data += 7
        else: data = 14 - data

        if (self._data[3] & 15) == data: return
        self._data[3] = data | (1<<4)
        self._SendWrite([3, self._data[3]])

    def treble(self, data): 
        data = self.constrain(data, -7, 7)

        if data <= 0: data += 7
        else: data = 14 - data

        if (self._data[4] & 15) == data: return
        self._data[4] = data | (1<<4)
        self._SendWrite([4, self._data[4]])

    def balance_all(self, data): 
        self.balance(self.DTC_OUT.ATT_LF, data)
        self.balance(self.DTC_OUT.ATT_RF, data)

    def balance(self, mode, data):
        mode = self.constrain(mode, 0, 3)
        data = self.constrain(data, 0, 79)
        a = 0

        if mode == self.DTC_OUT.ATT_LF: a = 5
        elif mode == self.DTC_OUT.ATT_RF: a = 6
        else: return

        if self._data[a] == data: return
        self._data[a] = data
        self._SendWrite([a, self._data[a]])

    def input(self, data):
        data = self.constrain(data, 1, self._max_input)
        
        if data == 1: data = (4<<1)
        else: data = ((data - 2) << 1)

        if self._data[9] == data: return
        self._data[9] = data
        self._SendWrite([9, self._data[9]])

    def phaseResistor(self, data):
        data = self.constrain(data, 1, 4) - 1
        
        if self._data[2] == data: return
        self._data[2] = data
        self._SendWrite([2, self._data[2]])

    def effectControl(self, data):
        data = self.constrain(data, 0, 15)

        if ((self._data[1] & 15) >> 3) == data: return
        self._data[1] &= ~(15 << 3)
        self._data[1] |= (data << 3)
        self._SendWrite([1, self._data[1]])

    def modeSurround(self, data):
        data = self.constrain(data, 0, 5)
        b = 0
        if data == self.DTC_SURROUND.SIMULATED: b = 0
        elif data == self.DTC_SURROUND.MUSIC: b = 1
        elif data == self.DTC_SURROUND.OFF: b = 2
        elif data == self.DTC_SURROUND.FLAT: b = 4
        else: return

        if (self._data[1] & 7) == b: return
        self._data[1] &= ~(7)
        self._data[1] |= b
        self._SendWrite([1, self._data[1]])

    def mute_all(self, data):
        self.mute(self.DTC_OUT.ATT_LF, data)
        self.mute(self.DTC_OUT.ATT_RF, data)

    def mute(self, mode, data):
        mode = self.constrain(mode, 0, 3)
        data = self.constrain(data, 0, 1)
        a = 0

        if mode == self.DTC_OUT.ATT_LF: a = 5
        elif mode == self.DTC_OUT.ATT_RF: a = 6
        else: return

        if data == self.DTC_SWITCH.ENABLE: self._SendWrite([a, ])
        else: self._SendWrite([a, self._data[a]])

class TDA7443(DigitalToneControl):
    _addr = 136
    _max_data = 7
    _max_input = 5

    def __init__(self):
        super().__init__()

    def volume(self, data):
        data = self.constrain(data, 0, 63)

        if ((self._data[3] >> 2) & 63) == data: return
        self._data[3] &= ~(63<<2)
        self._data[3] |= (data<<2)
        self._SendWrite([3, self._data[3]])

    def bass(self, data): 
        data = self.constrain(0, -7, 7)

        if data <= 0: data += 7
        else: data = 14 - data

        if (self.data[4] & 15) == data: return
        self._data[4] &= ~(15)
        self._data[4] |= data
        self._SendWrite([4, self._data[4]])

    def treble(self, data):
        data = self.constrain(0, -7, 7)

        if data <= 0: data += 7
        else: data = 14 - data

        if ((self.data[4]>>4) & 15) == data: return
        self._data[4] &= ~(15<<4)
        self._data[4] |= (data<<4)
        self._SendWrite([4, self._data[4]])

    def balance_all(self, data):
        self.balance(self.DTC_OUT.ATT_LF, data)
        self.balance(self.DTC_OUT.ATT_RF, data)

    def balance(self, mode, data):
        mode = self.constrain(mode, 0, 5)
        data = self.constrain(data, 0, 63)
        a = 0

        if mode == self.DTC_OUT.ATT_LF: a = 5
        elif mode == self.DTC_OUT.ATT_LF: a = 6
        else: return

        if (self._data[a] >> 2) == data: return
        self._data[a] = data << 2
        self._SendWrite([a, self._data[a]])

    def input(self, data): 
        data = self.constrain(data, 1, self._max_input) - 1

        if (self._data[0] & 7) == data: return
        self._data[0] &= ~(7)
        self._data[0] |= data

    def modeSurround(self, data):
        data = self.constrain(data, 0, 5)
        a = 0

        if data == self.DTC_SURROUND.PSEUDO: a = 0
        elif data == self.DTC_SURROUND.MUSIC: a = 1
        elif data == self.DTC_SURROUND.OFF: a = 2
        else: return

        b = (a >> 1) & 1
        a &= 1
        if b == 1:
            if ((self._data[0] >> 4) & 1) != 1:
                self._data[0] |= (1<<4)
                self._SendWrite([0, self._data[0]])

            if ((self._data[3] >> 1) & 1) != 1: 
                self._data[3] |= (1<<1)
                self._SendWrite([3, self._data[3]])
        else:
            if ((self._data[0] >> 4) & 1) == 1:
                self._data[0] &= ~(1<<4)
                self._SendWrite([0, self._data[0]])
            if (self._data[2] & 1) != a:
                self._data[2] &= ~(1)
                self._data[2] |= 1
                self._SendWrite([2, self._data[2]])
            if ((self._data[3] >> 1) & 1) == 1: 
                self._data[3] &= ~(1<<1)
                self._SendWrite([3, self._data[3]])

    def gain(self, data): 
        data = self.constrain(data, 0, 7)
        
        if ((self._data[0]>>5) & 7) != data: return
        self._data[0] &= ~(7<<5)
        self._data[0] |= (data<<5)
        self._SendWrite([0, self._data[0]])

    def agc(self, data):
        data = self.constrain(data, 0, 1)

        if (self._data[1] & 1) != data: return
        self._data[1] &= ~(1)
        self._data[1] |= data
        self._SendWrite([1, self._data[1]])

    def detector(self, data):
        data = self.constrain(data, 0, 1)

        if ((self._data[1] >> 1) & 1) != data: return
        self._data[1] &= ~(1<<1)
        self._data[1] |= (data<<1)
        self._SendWrite([1, self._data[1]])

    def releaseCurrent(self, data):
        data = self.constrain(data, 0, 1)

        if ((self._data[1] >> 2) & 1) != data: return
        self._data[1] &= ~(1<<2)
        self._data[1] |= (data<<2)
        self._SendWrite([1, self._data[1]])

    def attackTime(self, data): 
        data = self.constrain(data, 1, 4) - 1

        if ((self._data[1] >> 3) & 3) != data: return
        self._data[1] &= ~(3<<3)
        self._data[1] |= (data<<3)
        self._SendWrite([1, self._data[1]])

    def targetLevel(self, data):
        data = self.constrain(data, 1, 4) - 1

        if ((self._data[1] >> 5) & 3) != data: return
        self._data[1] &= ~(3<<5)
        self._data[1] |= (data<<5)
        self._SendWrite([1, self._data[1]])

    def zeroCross(self, data):
        data = self.constrain(data, 0, 1)

        if ((self._data[1] >> 7) & 1) != data: return
        self._data[1] &= ~(1<<7)
        self._data[1] |= (data<<7)
        self._SendWrite([1, self._data[1]])

    def effectControl(self, data):
        data = self.constrain(data, 0, 15)

        if ((self._data[2] >> 2) & 15) == data: return
        self._data[2] &= ~(15<<2)
        self._data[2] |= (data<<2)
        self._SendWrite([2, self._data[2]])

    def phaseResistor(self, data):
        data = self.constrain(data, 1, 4) - 1

        if ((self._data[2] >> 6) & 3) == data: return
        self._data[2] &= ~(3<<6)
        self._data[2] |= (data<<6)
        self._SendWrite([2, self._data[2]])

    def mute_all(self, data):
        self.mute(self.DTC_OUT.ATT_LF, data)
        self.mute(self.DTC_OUT.ATT_RF, data)

    def mute(self, mode, data):
        mode = self.constrain(mode, 0, 3)
        data = self.constrain(data, 0, 1)
        b = 0

        if mode == self.DTC_OUT.ATT_LF: b = 5
        elif mode == self.DTC_OUT.ATT_RF: b = 6
        else: return

        if ((self._data[0] >> 3) & 1) != data:
            self._data[0] &= ~(1<<3)
            self._data[0] |= (data<<3)
            self._SendWrite([0, self._data[0]])
        if ((self._data[3] >> 1) & 1) != data: 
            self._data[3] &= ~(1<<1)
            self._data[3] |= (data<<1)
            self._SendWrite([3, self._data[3]])

        if data == self.DTC_SWITCH.ENABLE:
            self._SendWrite([3, 254])
            self._SendWrite([b, 252])
        else: self._SendWrite([b, self._data[b]])

# class TDA7461

# class TDA7462

# class TDA7463

# class TDA7464

# class TDA7465

# class TDA7466

# class TDA7467