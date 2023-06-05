#
#  Copyright 2023 Direkt Embedded Pty Ltd
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""
Robot Framework (RF) wrapper library for LabJack U3 device https://robotframework.org/
Refer
https://robotframework.org/
https://github.com/labjack/LabJackPython/blob/master/src/u3.py
"""

import u3

__version__ = "0.0.0"


class LabJackU3:
    """
    RF Library Class which directly wraps the LabJack python U3() class, by providing equivalent keyword functions.
    e.g. toggle_led maps directly to U3().toggleLED() and
         set_do() wraps directly to setDOState()

    This wrapper shows how to wrap RF library to LabJack python library.
    You can then create RF keywords to setup your jig and say verify VDD as follows
    *** Keywords ***
    Setup DET003 Test Jig
        Open Device    local_id=1
        Config IO      FIOAnalog=0  EIOAnalog=0
        Config Analog  0

    Verify Vdd
        ${vdd}=        Verify Analog Input  0  minimum=3.2  maximum 3.4
        [return]       ${vdd}

    Alternatively you may wish to use this as an example  and create your solution specific wrapper, by inheriting
    this class and and having keyword methods like
    read_vdd() e.g. if you connect and configure AIN0/FIO0 to your device's Vdd, you could have a vdd threshold
    check keyword as follows. This would increase the readability of the suites. As each setup may have different
    LabJack IO configuration you would do this at design time.

    def expect_vdd(self, minimum_voltage, maximum_voltage, msg):
        vdd = self.lab_jack.getAIN(FIO0)
        if not (minimum_voltage <= vdd <= maximum_voltage):
            raise AssertionError(msg)
        return vdd

    NOTEs
    - U3().configU3() is not wrapped as it writes to flash, and we never want to do that in a test suite, as there is a
    write limit on flash'. Refer LabJack-U3-Datasheet.pdf section 5.2.2
    If you decide to hard configure your LabJack device in your Jig, then perform this using the Windows tool
    or other python code once only.
    - U3-HV has first four FIO as Analog Input only. Refer LabJack-U3-Datasheet.pdf section 2.5
    - UART is not implemented as even LabJack does not recommend it for most communications, instead opt for a USB to
    serial uart: From LabJack-U3-Datasheet.pdf section 4.3.12 "Also consider that a better way to do RS-232
    (or RS-485 or RS-422) communication is with a standard USB<=>RS-232 adapter/converter/dongle, so the user should
    have a particular reason to not use that and use a U3 instead."
    - Timers/Counters
      LabJack-U3-Datasheet.pdf section 2.9 explains that timer and counter 'pins' are defined by an offset,
      and then applied in this order and sequentially
      Timer0, Timer1, Counter0, then Counter1, so if TimerCounterPinOffset=4, then FI04 is attached to Timer0 if
      enabled, then FIO5 to Timer1 if enabled, but if not it would go to Counter0.
      Timers modes include input counting timers and output timers.
      Also note from datasheet "hardware revision 1.30, timers/counters cannot appear on FIO0-3"
    """

    ROBOT_LIBRARY_SCOPE = 'SUITE'

    def __init__(self):
        self._lab_jack = u3.U3(autoOpen=False)
        self.local_id = None

    @property
    def lab_jack(self):
        if not self._lab_jack:
            raise SystemError('No LabJack connection established!')
        return self._lab_jack

    def open_device(self, local_id: int = None):
        """
        Open the first device found, or if local_id specified open it.
        To use local_id user should ensure multiple devices have had the correct id written outside of this library.
        Open Device  1
        """
        self.local_id = local_id
        self.lab_jack.open(localId=local_id)
        return True

    def config_io(self, timer_counter_pin_offset: int = None, enable_counter_1: bool = None,
                  enable_counter_0: bool = None, number_of_timers_enabled: int = None,
                  fio_analog: int = None, eio_analog: int = None,
                  enable_uart: int = None):

        TimerCounterPinOffset = timer_counter_pin_offset
        EnableCounter1 = enable_counter_1
        EnableCounter0 = enable_counter_0
        NumberOfTimersEnabled = number_of_timers_enabled
        FIOAnalog = fio_analog
        EIOAnalog = eio_analog
        EnableUART = enable_uart
        return self.lab_jack.configIO(TimerCounterPinOffset, EnableCounter1,
                                      EnableCounter0, NumberOfTimersEnabled,
                                      FIOAnalog, EIOAnalog,
                                      EnableUART)

    def config_timer_clock(self, **kwargs):
        # TODO expand or coerce arguments
        self.lab_jack.configTimerClock(**kwargs)
        return True

    def toggle_led(self):
        """
        Toggle the led state
        """
        self.lab_jack.toggleLED()
        return True

    def set_do(self, io_num: int, state: int = 1):
        """
        Sets direction to output and sets state
        """
        self.lab_jack.setDOState(ioNum=io_num, state=state)
        return True

    def get_di(self, io_num: int):
        """
        Sets direction to input and reads input state
        """
        return self.lab_jack.getDIState(ioNum=io_num)

    def get_dio(self, io_num: int):
        """
        Gets state of input, but does not change direction
        """
        return self.lab_jack.getDIOState(ioNum=io_num)

    def get_temperature(self):
        """
        Returns labjack device temperature in Kelvin
        """
        return self.lab_jack.getTemperature()

    def get_analog_input(self, pos_channel: int):
        return self.lab_jack.getAIN(pos_channel)

    def config_analog(self, *args: int):
        """
        Make given IOs analog ones rather than digital
        """
        self.lab_jack.configAnalog(*args)
        return True

    def config_digital(self, *args: int):
        """
        Make given IOs digital ones rather than analog
        """
        self.lab_jack.configDigital(*args)
        return True

    def verify_bound_analog_input(self, pos_channel: int, minimum: float = None, maximum: float = None,
                                  msg="Analog Input Verify Failed"):
        analog = self.lab_jack.getAIN(pos_channel)
        if minimum and (analog < minimum):
            raise Exception(f"{msg}: value {analog} < minimum {minimum}")
        if maximum and (analog > maximum):
            raise Exception(f"{msg}: value {analog} > maximum {maximum}")
        return analog

    def verify_digital_input(self, io_num: int, expect: int = None, msg="Digital Input Value Invalid"):
        digital_input = self.lab_jack.getDIState(io_num)
        if expect and (expect != digital_input):
            raise Exception(f"{msg}: input {digital_input} != expected {expect}")
        return digital_input

    def get_counter0(self, **kwargs):
        # TODO expand or coerce arguments
        return self.lab_jack.getFeedback(u3.Counter0(**kwargs))

    def get_counter1(self, **kwargs):
        # TODO expand or coerce arguments
        return self.lab_jack.getFeedback(u3.Counter1(**kwargs))

    def get_timer0(self, **kwargs):
        # TODO expand or coerce arguments
        return self.lab_jack.getFeedback(u3.Timer0(**kwargs))

    def get_timer1(self, **kwargs):
        # TODO expand or coerce arguments
        return self.lab_jack.getFeedback(u3.Timer1(**kwargs))

    def config_timer0(self, **kwargs):
        # TODO verify timer is enabled already and raise error if not
        self.lab_jack.getFeedback(u3.Timer0Config(**kwargs))
        return True

    def config_timer1(self, **kwargs):
        self.lab_jack.getFeedback(u3.Timer1Config(**kwargs))
        return True

    # TODO advanced timers
