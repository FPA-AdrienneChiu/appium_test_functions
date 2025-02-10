import crcmod
from serial import Serial
from PythonCommsBusHijack.erd_lib import ERDLib


class IPB_Control:
    """Controls IPB messages, enables read/write ERD messages and IPB commands."""

    def __init__(self, port: str, erd_lib: ERDLib) -> None:
        """Initialise class with IPB port and ERD Library for ERD definition and lookup.

        Args:
            port (str): COM port connected to product IPB.
            erd_lib (ERDLib): ERDLib instance.
        """
        self.com = Serial(port, 115200)
        self.com.reset_input_buffer()
        self.com.read_all()
        self.crc16 = crcmod.mkCrcFun(0x11021, rev=False, initCrc=0x1021)

        self.erd_lib = erd_lib
        self.key_count = 1
        self.err_count = 0
        self.keep_alive = True
        self.message_type = {
            0x21: "Write Request",
            0x22: "Publish",
            0x23: "Start/Pause Request",
            0x24: "IPB Safety Key",
            0x25: "Line Test Request",
            0x26: "Data Transfer Request",
            0x27: "Read Request",
        }

    def construct_message(self, databytes: bytearray, message_type: int):
        """Construct the IPB message based on data length and message type.

        Args:
            databytes (bytearray): ERD data to be sent over IPB.
            message_type (int): message type int.
        """
        header_start = (0x4B).to_bytes(1, "big")
        protocol = (0x00).to_bytes(1, "big")
        source_addr = (0xFE).to_bytes(1, "big")
        broadcast_addr = (0xFF).to_bytes(1, "big")
        seq_number = (0x00).to_bytes(1, "big")
        body_len = (len(databytes) + 3).to_bytes(1, "big")
        header = header_start + protocol + source_addr + broadcast_addr + seq_number + body_len
        head_crc = self.crc16(header)
        header += head_crc.to_bytes(2, "big")

        body_id = message_type.to_bytes(1, "big")

        body = body_id + databytes
        body_crc = self.crc16(body)
        body += body_crc.to_bytes(2, "big")

        out_bytes = header + body
        self.output(out_bytes)
        # print(out_bytes.hex())

    def run(self):
        """Runner that keeps listening on IPB for incoming messages from the products"""
        while self.keep_alive:
            header = self.com.read_until(expected="  ", size=5)
            if header[0] == 0x11:
                # print(header)
                self.com.reset_input_buffer()
                continue

            header += self.com.read_until(expected="  ", size=3)
            if not self.crc16(header[:6]) == int.from_bytes(header[6:], "big"):
                print(header.hex())
                print("ERROR")
                self.err_count += 1
                self.com.reset_input_buffer()
                continue

            body = self.com.read_until(expected="  ", size=header[5])
            # print((header + body).hex())
            self.parse_message(body)

    def parse_message(self, message: bytearray):
        """Parse incoming ERDs from the incoming messages to readable texts.

        Args:
            message (bytearray): ERD and ERD data
        """
        if message[0] not in self.message_type:
            return
        out = "[" + self.message_type[message[0]] + "] "
        # print(message[1:3].hex())
        if message[0] == 0x24:
            # print(out)
            return

        erd = self.erd_lib.search_ERD(message[1:3].hex())
        out += erd["name"] + "-"
        if message[0] == 0x27:
            return
        data = message[4:]

        for i in range(0, len(erd["data"])):
            if "bits" in erd["data"][i]:
                if erd["data"][i]["bits"]["size"] > 1:
                    out += "Reserved. "
                else:
                    bitArr = []
                    for j in range(
                        erd["data"][i]["offset"],
                        erd["data"][i]["offset"] + erd["data"][i]["size"],
                    ):
                        bitArr.extend(bin(data[j])[2:].zfill(8)[::-1])
                    if bitArr[erd["data"][i]["bits"]["offset"]] == "1":
                        out += erd["data"][i]["name"] + "; "

            else:
                if erd["data"][i]["type"] == "string":
                    for j in range(
                        erd["data"][i]["offset"],
                        erd["data"][i]["offset"] + erd["data"][i]["size"],
                    ):
                        out += chr(data[j])
                    out += ". "
                elif erd["data"][i]["type"] == "bool":
                    out += erd["data"][i]["name"] + ": " + str(bool(data[erd["data"][i]["offset"]])) + ". "
                elif erd["data"][i]["type"] == "enum":
                    val = ""
                    for j in range(
                        erd["data"][i]["offset"],
                        erd["data"][i]["offset"] + erd["data"][i]["size"],
                    ):
                        val += hex(data[j])[2:]
                    val = str(int(val, 16))
                    try:
                        out += erd["data"][i]["name"] + ": " + erd["data"][i]["values"][val] + ". "
                    except KeyError:
                        out += erd["data"][i]["name"] + ": " + val + ". "
                elif erd["data"][i]["type"] == "raw":
                    val = ""
                    for j in range(
                        erd["data"][i]["offset"],
                        erd["data"][i]["offset"] + erd["data"][i]["size"],
                    ):
                        val += hex(data[j])[2:]
                    out += erd["data"][i]["name"] + ": " + val + ". "
                elif (
                    erd["data"][i]["type"] == "u32" or erd["data"][i]["type"] == "u16" or erd["data"][i]["type"] == "u8"
                ):
                    val = ""
                    for j in range(
                        erd["data"][i]["offset"],
                        erd["data"][i]["offset"] + erd["data"][i]["size"],
                    ):
                        val += hex(data[j])[2:]
                    val = str(int(val, 16))
                    out += erd["data"][i]["name"] + ": " + val + ". "

        # return out + "|"
        # print(out)

    def output(self, output_arr: bytearray):
        """Writes to IPB comm port.

        Args:
            output_arr (bytearray): output byte array.
        """
        self.com.write(output_arr)
        self.com.flush()
