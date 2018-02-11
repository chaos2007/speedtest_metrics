from speed_test_daemon import SpeedTestDaemon
from speed_test_visualizer import SpeedTestVisualizer
import threading
import click


@click.group()
def greet():
    pass


@greet.command()
@click.option("--frequency", required=True, help="The frequency in seconds to grab metrics.", type=int)
@click.option("--filename", required=True, help="The name of the file to store data, existing file will be appended to.")
def daemon(**kwargs):
    stop_signal = threading.Event()
    dae = SpeedTestDaemon(frequency=kwargs["frequency"],
                          filename=kwargs["filename"],
                          stop_signal=stop_signal)
    dae.start()
    while not click.confirm("Shutdown daemon?"):
        pass
    print("Shutting down daemon, please hold.")
    stop_signal.set()
    dae.join()


@greet.command()
@click.option("--filename", required=True, help="Filename of logfile to visualize.")
def visualizer(**kwargs):
    viz = SpeedTestVisualizer(kwargs["filename"])
    viz.graph()


if __name__ == "__main__":
    greet()



