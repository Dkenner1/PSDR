import re
import math
SI_PREFIX = {
    "u": 1/1000000,
    "": 1,
    "d": 1,
    "k": 1000,
    "K": 1000,
    "m": 1000000,
    "M": 1000000,
    "g": 1000000000,
    "G": 1000000000
}


class UnitParser:
    def __init__(self, r=None, *_unit, ):
        if r is None:
            r = []
        self.restrictions = r
        self.unit = _unit
        # TODO add restrictions + parse for list of allowed units
        self.expr = re.compile(r"^\d+[mg]h*z*$", re.IGNORECASE)

    def toInt(self, _str):
        if (_str.isnumeric()):
            return int(_str)
        if not self.expr.match(_str):
            raise ValueError("Input expression does not conform to allowed values")
        print("This shouldn't be reachable, error with value: " + str(SI2int(_str)))

    def int2SI(self, num, _unit=""):
        if num >= SI_PREFIX['g']:
            return str(num / SI_PREFIX['g']) + "G" + _unit
        elif num >= SI_PREFIX['m']:
            return str(num / SI_PREFIX['m']) + "M" + _unit
        elif num >= SI_PREFIX['k']:
            return str(num / SI_PREFIX['k']) + "K" + _unit
        return str(num) + _unit


def get_prefix(_str):
    for ch in _str:
        if ch in SI_PREFIX:
            print("Prefix is: " + ch)
            return ch.lower()
    return ""


def get_first_num(_str):
    x = re.findall(r"-?\d+\.?\d*", _str)
    return float(x[0]) if x else None


def SI2int(_str):
    #Todo Handle when unit needs to be converted back to understandable unit (dbm)
    if re.findall(r".W", _str, re.IGNORECASE):
        print(" Watts")
        return
    return int(get_first_num(_str)*SI_PREFIX[get_prefix(_str)])

def dbm2mWatt(num):
    out = 10**(num/10)/1000
    print(out)
    if out >= SI_forWatts["m"]:
        return str(round(out/SI_forWatts["m"], 3)) + "mW"
    elif out >= SI_forWatts["u"]:
        return str(round(out/SI_forWatts["u"], 3)) + "uW"
    elif out >= SI_forWatts["n"]:
        return str(round(out/SI_forWatts["n"], 3)) + "nW"
    elif out >= SI_forWatts["p"]:
        return str(round(out/SI_forWatts["p"], 3)) + "pW"
    return "0mW"


SI_forWatts = {
    "": 1,
    "m": 10**(-3),
    "u": 10**(-6),
    "n": 10**(-9),
    "p": 10**(-12)
}

def watt2dbm(watt_str):
    pre = get_prefix(watt_str)
    num = get_first_num(watt_str)
    out = None
    if pre == "m":
        out = 10*math.log(num*SI_forWatts['m'], 10)+30
    elif pre == "u":
        out = 10*math.log(num*SI_forWatts['u'], 10)+30
    elif pre == "n":
        out = 10*math.log(num*SI_forWatts['n'], 10)+30
    elif pre == "p":
        out = 10*math.log(num*SI_forWatts['p'], 10)+30
    elif pre == "":
        out = 10 * math.log(num, 10) + 30
    return round(out, 2)
