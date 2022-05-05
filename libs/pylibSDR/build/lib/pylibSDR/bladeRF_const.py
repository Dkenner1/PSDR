TxMode_CONTINUOUS="continuous"
TxMode_PULSE="pulse"

CMode_SINGLE="single"
CMode_MIMO="mimo"

GMode_DECOUPLED="decoupled"
GMode_COUPLED="coupled"

HELP_TXT = {"freq": "Frequency: Range (47MHz, 6GHz)",
"bw": "Bandwidth: Range (200KHz, 56MHz)",
	    
"num_samples": """Number of samples to be transmit.
Determines transmission length

Transmit time = num_samples/Sample Rate
For 500K at 1Msps the transmission will last .5 seconds

Maximum # is the same as the sample rate to prevent
memory overflow issues.
""",
            
"pwr": """Determines the amplitude and gain of the signal.

Device power range is -83 - 8 dbm

Device output power is determined in dbm as
Pwr_total = DAC + Amplifiers

Dbm is the unit for decibel milliwatts which is an
exponential unit with 0dbm being 1mW

Output power is calculated internally with scaling value.
The formula is mostly logic related but can generally be
expressed as
For dbm in range -60 > x > -83
Pwr = 0 amp + x*DAC
For dbm  in range: x > -60
PWR = amp[x] + DAC*1

The DAC power calculation is determined as it outputs the
signal as a function of quadrature sampling. In which 
signal amplitude is the sum of its I and Q components this
is represented with a digital value that can vary from 
-2048 to 2047. This set of values will be decoded and 
sampled by the onboard DAC. It is important to remember
that these digital values are just steps breaking down the
actual voltage range. This range varies programmatically
and therefore is difficult to determine without calibration.
Generally speaking the voltage range is 2.7-3.3V

DAC signal amplitude is sqrt(I^2 + Q^2)
Power in watts is expressed as I^2 + Q^2.

Amplifiers are directly controlled as a measure of gain
in db.
""",
            
"tx_mode": """Sets the output waveform mode
Continuous: device will transmit the set number of samples
before reloading config file and restarting the transmit
            
Pulse: Device will transmit the a percentage
of the number of samples before disabling and
waiting for a period determined by duty cycle.

For example, with 500K samples, 1MSPS
(set in the config header file) and a 70% duty cycle
the program will transmit for
(duty_cycle/100)*#Samples/Sample Rate=0.7*0.5=.35 seconds

Then disable the transmitter and hold for
(1-duty_cycle/100) * # Samples/Sample Rate = 0.15 seconds

These numbers however, are only close estimates because the
GUI has only indirect control of the bladeRF.

Delays can occur in the USB connection
in the range of microseconds.""",
            
"channel_mode": """Sets the output waveform channel mode
Single: Will output only through whatever channel
has been selected

MIMO: Multiple input, multiple output. Will output through
both channels.

Normally MIMO is used for beamforming, but because the
transmitted signal is just an amplitude
it is instead used for additional power.""",
	    
"channel": """Sets the output channel, only relevant in single channel mode
""",
            
"duty_cycle": """Sets the duty cycle for a pulsed signal

Value can range from 0 to 100 and determines
what percentage of # Samples / Sample Rate will transmit

Only used when in pulse tx_mode

Exact calculation of time is:
Time_on = Duty Cycle * Samples / Sample Rate 
Time_off = (1-Duty_cycle) * Samples / Sample Rate
Entire transmit period is:
Transmit_total = Transmit_on + Transmit_off
""",

"gain" : """ Gain controls two settings, gain mode and gain level

Gain mode has two settings; Coupled and Decoupled.

In coupled mode the power scale will affect both signal
amplitude and gain.

In this mode Gain will be scaled from: 0 - 66

In decoupled mode gain will be set by the gain slider.

This is useful if you need negative gain or want power
to only vary the amplitude of the signal.
""",
"sample_rate" : """Sets the sample rate of the system.
Range [521000, 61440000]
Sample rate should ideally be
1.2*2BW
to satisfy the nyquist rate and prevent aliasing

""",
            
"help" : """

"""
}
