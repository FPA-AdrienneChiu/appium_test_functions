from PythonCommsBusHijack.erd_lib import ERDLib
from PythonCommsBusHijack.ipb_control import IPB_Control


class HD_control(IPB_Control):
    def __init__(self, port: str, erd_lib: ERDLib) -> None:
        super().__init__(port, erd_lib)

    def cap_touch_command(self, command: str):
        erd = self.erd_lib.search_ERD("f012")
        if command not in erd["data"][0]["values"]:
            raise ValueError("Command '" + command + "' not in Cap Touch commands")
        cmd = int(command).to_bytes(1, "big")
        cnt = self.key_count.to_bytes(1, "big")
        self.key_count += 1
        outarr = bytes.fromhex(erd["id"][2:]) + b"\x02" + cmd + cnt
        self.construct_message(outarr, 0x22)

    def dryer_start_pause(self):
        self.cap_touch_command("11")

    def washer_start_pause(self):
        self.cap_touch_command("10")

    def power_key_press(self):
        self.cap_touch_command("1")

    def power_key_quickhold(self):
        self.cap_touch_command("2")

    def power_key_shorthold(self):
        self.cap_touch_command("3")

    def power_key_longhold(self):
        self.cap_touch_command("4")

    def get_machine_status(self):
        erd = 0xF301
        self.construct_message(erd.to_bytes(2, "big"), 0x27)

    def get_machine_substatus(self):
        erd = 0xF302
        self.construct_message(erd.to_bytes(2, "big"), 0x27)

    def get_selected_cycle(self):
        erd = 0xF307
        self.construct_message(erd.to_bytes(2, "big"), 0x27)

    def set_cycle(self, cycle: str):
        # Does not work
        erd = self.erd_lib.search_ERD("f403")
        if cycle not in erd["data"][0]["values"]:
            raise ValueError("Command '" + cycle + "' not in Cap Touch commands")
        cmd = int(cycle).to_bytes(1, "big")
        outarr = bytes.fromhex(erd["id"][2:]) + b"\x01" + cmd
        self.construct_message(outarr, 0x22)

    def stop_cycle(self):
        erd = self.erd_lib.search_ERD("f307")
        outarr = bytes.fromhex(erd["id"][2:])
        self.construct_message(outarr, 0x27)

    def enable_test_mode(self):
        erd = self.erd_lib.search_ERD("f42a")
        cmd = b"\x01"
        outarr = bytes.fromhex(erd["id"][2:]) + b"\x01" + cmd
        self.construct_message(outarr, 0x21)

    def set_2d_moisture(self, moisture: str):
        erd = self.erd_lib.search_ERD("f42b")
        cmd = int(moisture).to_bytes(1, "big")
        outarr = bytes.fromhex(erd["id"][2:]) + b"\x01" + cmd
        self.construct_message(outarr, 0x21)

    def tete(self):
        a = "4b 00 fe ff 00 03".replace(" ", "")
        head = bytearray.fromhex(a)
        headcrc = self.crc16(bytearray.fromhex(a))
        head += headcrc.to_bytes(2, "big")
        b = "23".replace(" ", "")
        body = bytearray.fromhex(b)
        bodycrc = self.crc16(bytearray.fromhex(b))
        body += bodycrc.to_bytes(2, "big")
        self.com.write(head + body)

    def get_erd(self, erd):
        self.construct_message(bytearray.fromhex(erd), 0x27)
