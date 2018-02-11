import plotly.graph_objs as go
import plotly.offline as py
import pickle


def pickle_loader(pkl_file):
    try:
        while True:
            yield pickle.load(pkl_file)
    except EOFError:
        pass


class SpeedTestVisualizer:

    def __init__(self, filename):
        self.filename = filename

    def graph(self):
        times=[]
        downloads=[]
        uploads=[]
        with open(self.filename, "rb") as f:
            for data in pickle_loader(f):
                downloads.append(data["download"])
                uploads.append(data["upload"])
                times.append(data["timestamp"])
        download_trace = go.Scatter(name="Download(Mb/s)", x=times, y=downloads)
        upload_trace = go.Scatter(name="Upload(Mb/s)", x=times, y=uploads)
        data = [download_trace, upload_trace]
        py.plot(data, filename="basic-line.html")
