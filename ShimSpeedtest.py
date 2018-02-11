import time
from speed_test_daemon import SpeedTestDaemon
import threading
import click


@click.group()
def greet():
    pass


@greet.command()
@click.option("--frequency", required=True, help="The frequency in seconds to grab metrics.", type=int)
def daemon(**kwargs):
    stop_signal = threading.Event()
    daemon = SpeedTestDaemon(kwargs["frequency"], stop_signal)
    daemon.start()
    time.sleep(60)
    stop_signal.set()
    daemon.join()


@greet.command()
@click.argument("filename")
def visualizer(**kwargs):
    pass


if __name__ == "__main__":
    greet()



