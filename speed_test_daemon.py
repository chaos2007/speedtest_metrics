import speedtest
import threading
import pickle
import datetime
import time
import sys


class SpeedTestDaemon(threading.Thread):

    def __init__(self, frequency, stop_signal):
        super().__init__()
        self.frequency = frequency
        self.stop_signal = stop_signal

    def run(self):
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')

        with open(st + ".pickle", "wb") as f:
            while not self.stop_signal.is_set():
                try:
                    current_time = time.time()
                    date = datetime.datetime.fromtimestamp(current_time).strftime('%Y/%m/%d %H:%M:%S')

                    output = self.get_speed_stats()
                    output["download"] = output["download"] / 1000000
                    output["upload"] = output["upload"] / 1000000
                    output["current_time"] = current_time
                    output["date"] = date
                    pickle.dump(output, f)

                    print("Current Result: Ping {} ms DL {} Mbits / UL {} Mbits".format(output["ping"],
                                                                                        output["download"],
                                                                                        output["upload"]))

                    f.flush()
                    time.sleep(self.frequency)
                except:
                    e = sys.exc_info()[0]
                    print("Exception occurred. Keep trying.\r\n{}".format(e))

    @staticmethod
    def get_speed_stats():
        st = speedtest.Speedtest()
        st.get_best_server()
        st.download()
        st.upload()
        return st.results.dict()

