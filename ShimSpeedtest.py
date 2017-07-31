import datetime
import time
import speedtest
import re
import csv
from subprocess import Popen, PIPE

INTERVAL = 120 #Seconds

class SpeedTestOutputParser():

    def __init__(self, output):
        self.output = output

    def get_ping(self):
        match = re.search("Ping: (.*) ms", self.output, re.MULTILINE)
        if match:
            return float(match.group(1))
        raise Exception("Search failed:\r\n {}".format(self.output))

    def get_download(self):
        match = re.search("Download: (.*) Mbit/s", self.output, re.MULTILINE)
        if match:
            return float(match.group(1))
        raise Exception("Search failed:\r\n {}".format(self.output))

    def get_upload(self):
        match = re.search("Upload: (.*) Mbit/s", self.output, re.MULTILINE)
        if match:
            return float(match.group(1))
        raise Exception("Search failed:\r\n {}".format(self.output))


test_string = """
Ping: 40.292 ms
Download: 81.56 Mbit/s
Upload: 4.56 Mbit/s
"""

def test_parser():
    output = SpeedTestOutputParser(test_string)
    assert output.get_ping() == 40.292
    assert output.get_download() == 81.56
    assert output.get_upload() == 4.56


if __name__ == "__main__":

    st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')

    with open(st + ".csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(['date', "Ping (ms)", "Download Mb/sec", "Upload Mb/sec"])
        while True:
            current_time = time.time()
            date = datetime.datetime.fromtimestamp(current_time).strftime('%Y/%m/%d %H:%M:%S')
            process = Popen(["speedtest", "--secure", "--simple"], stdout=PIPE)
            (output, err) = process.communicate()
            exit_code = process.wait()
            parsed = SpeedTestOutputParser(output.decode("utf-8"))

            print("Current Result: Ping {} ms DL {} Mbits / UL {} Mbits".format(parsed.get_ping(), parsed.get_download(), parsed.get_upload()))

            writer.writerow([date, parsed.get_ping(), parsed.get_download(), parsed.get_upload()])
            f.flush()
            time.sleep(INTERVAL)


