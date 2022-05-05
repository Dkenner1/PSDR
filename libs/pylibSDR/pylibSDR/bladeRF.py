from ..constants import bladeRF_const
import os


exc_loc = os.path.abspath("bin/foo_out")
file_loc = os.path.abspath("etc/bladeRF_TxConfig.ini")


class SDR:
    def __init__(self, _exe=exc_loc, _config_loc=file_loc):
        self.exe = _exe
        self.config_loc = _config_loc
        # Dictionary for convenient calling relevant function
        self.update_list = {
            "freq": self.set_freq,
            "bandwidth": self.set_bandwidth,
            "num_samples": self.set_num_samples,
            "pwr": self.set_pwr,
            "tx_mode": self.set_tx_mode,
            "channel_mode": self.set_channel_mode,
            "channel": self.set_channel,
            "duty_cycle": self.set_duty_cycle,
            "sample_rate": self.set_sample_rate,
            "gain": self.set_gain,
            "gain_mode": self.set_gain_mode,

            "rx_freq": self.set_rx_freq,
            "rx_bandwidth": self.set_rx_bandwidth,
            "rx_num_samples": self.set_rx_num_samples,
            "auto": self.set_rx_sample_rate_auto,
            "rx_sample_rate": self.set_rx_sample_rate,
            "rx_gain": self.set_rx_gain,
            "rx_channel": self.set_rx_channel
        }


    def enable(self):
        update_config("tx", 1, self.config_loc)
        #Popen([self.exe])

    def disable(self):
        update_config("tx", 0, self.config_loc)

    def set_freq(self, _freq):
        freq = int(_freq)
        if 47000000 <= freq <= 6000000000:
            update_config("freq", freq, self.config_loc)
        else:
            raise ValueError("Supplied value not in valid range: 47MHz - 6GHz")

    def set_bandwidth(self, bw):
        bw = int(bw)
        if 200000 <= bw <= 56000000:
            update_config("bandwidth", bw, self.config_loc)
        else:
            raise ValueError("Supplied value not in valid range: 200KHz - 56MHz")

    def set_num_samples(self, _num_samp):
        num_samp = int(_num_samp)
        if 1 <= num_samp <= 61440000:
            update_config("num_samples", num_samp, self.config_loc)
        else:
            raise ValueError("Supplied value not in valid range: 1 - 61.44Ms")

    def set_sample_rate(self, samp_rate):
        samp_rate = int(samp_rate)
        if 521000 <= samp_rate <= 61440000:
            update_config("sample_rate", samp_rate, self.config_loc)
        else:
            raise ValueError("Supplied value not in valid range: 521Ksps - 61.44Msps")

    def set_pwr(self, _pwr):
        pwr = float(_pwr)
        if -83 <= pwr <= 8:
            update_config("pwr", pwr, self.config_loc)
        else:
            raise ValueError("Supplied value not in valid range: -83 - 8")

    def set_gain_mode(self, mode):
        if mode == bladeRF_const.GMode_DECOUPLED or mode == bladeRF_const.GMode_COUPLED:
            update_config("gain_mode", mode, self.config_loc)
        else:
            raise ValueError("Invalid gain mode, use either (decoupled, coupled)")

    def set_gain(self, gain):
        gain = int(gain)
        if gain >= -23 or gain <= 66:
            update_config("gain", gain, self.config_loc)
        else:
            raise ValueError("Invalid power mode, use either (decoupled, coupled)")

    def set_tx_mode(self, tmode):
        if tmode.lower() == bladeRF_const.TxMode_CONTINUOUS or tmode.lower() == bladeRF_const.TxMode_PULSE:
            update_config("tx_mode", tmode, self.config_loc)
        else:
            raise ValueError("Setting not valid, use value from constants.py \n" +
                             "or one of the two strings: 'continuous', 'pulse'")

    def set_channel_mode(self, cmode):
        if cmode.lower() == bladeRF_const.CMode_SINGLE or cmode.lower() == bladeRF_const.CMode_MIMO:
            update_config("channel_mode", cmode, self.config_loc)
        else:
            raise ValueError("""Setting not valid, use value from constants.py
                             or one of the two strings: 'single', 'mimo'""")

    def set_channel(self, ch):
        ch = int(ch)
        if ch == 1 or ch == 2:
            update_config("channel", ch, self.config_loc)
        else:
            raise ValueError("Undefined Channel: Acceptable values: 1, 2")

    def set_duty_cycle(self, duty_cycle):
        duty_cycle = float(duty_cycle)
        if 0 <= duty_cycle <= 100:
            update_config("duty_cycle", duty_cycle, self.config_loc)
        else:
            raise ValueError("Supplied value not in valid range: 0 - 100")

    def rx_enable(self):
        update_config("rx", 1, self.config_loc)
        #Popen([self.exe])

    def rx_disable(self):
        update_config("rx", 0, self.config_loc)

    #Rx funcs
    def set_rx_freq(self, _freq):
        freq = int(_freq)
        if 70000000 <= freq <= 6000000000:
            update_config("rx_freq", freq, self.config_loc)
        else:
            raise ValueError("Supplied value not in valid range: 70MHz - 6GHz")

    def set_rx_bandwidth(self, bw):
        bw = int(bw)
        if 200000 <= bw <= 56000000:
            update_config("rx_bandwidth", bw, self.config_loc)
        else:
            raise ValueError("Supplied value not in valid range: 200KHz - 56MHz")

    def set_rx_num_samples(self, _num_samp):
        num_samp = int(_num_samp)
        if 1 <= num_samp <= 61440000:
            update_config("rx_num_samples", num_samp, self.config_loc)
        else:
            raise ValueError("Supplied value not in valid range: 1 - 61.44Ms")

    def set_rx_sample_rate(self, samp_rate):
        samp_rate = int(samp_rate)
        if 521000 <= samp_rate <= 61440000:
            update_config("rx_sample_rate", samp_rate, self.config_loc)
        else:
            raise ValueError("Supplied value not in valid range: 521Ksps - 61.44Msps")

    def set_rx_sample_rate_auto(self, mode):
        if mode == 1 or mode == 0:
            update_config("auto", mode, self.config_loc)
        else:
            raise ValueError("Supplied value can only be 1 or 0")

    def set_rx_gain(self, gain):
        gain = int(gain)
        if gain >= -15 or gain <= 60:
            update_config("rx_gain", gain, self.config_loc)
        else:
            raise ValueError("Invalid gain value. Range is [-15, 60]")

    def set_rx_channel(self, ch):
        ch = int(ch)
        if ch == 1 or ch == 2:
            update_config("rx_channel", ch, self.config_loc)
        else:
            raise ValueError("Undefined Channel: Acceptable values: 1, 2")

    def get_config(self):
        import re
        f = open(self.config_loc, "r")
        config = {}
        for x in f:
            if x[0] == '#' or x[0] == '\n':
                continue
            x = re.sub(r"[\t\n\s]*", "", x)
            x.replace(" ", "")
            x.replace("\n", "")
            key_value = x.split('=')
            config[key_value[0]] = key_value[1]
        f.close()
        return config


def get_config_value(key, config_loc=file_loc):
    f = open(config_loc, "r")
    for x in f:
        if x[0] == '#' or x[0] == '\n':
            continue
        x.replace(" ", "")
        x.replace("\n", "")
        key_value = x.split('=')
        if key == key_value[0]:
            return key_value[1]
    f.close()


def update_config(key, new_value, config_loc):
    f = open(config_loc, "r")
    flines = f.readlines()
    for i, line in enumerate(flines, start=0):
        line.replace(" ", "")
        line.replace("\n", "")
        key_value = line.split('=')
        if key_value[0] != key:
            continue
        key_value[1] = str(new_value) + "\n"
        flines[i] = key_value[0] + "=" + key_value[1]
    f = open(config_loc, "w")
    f.writelines(flines)
    f.close()
