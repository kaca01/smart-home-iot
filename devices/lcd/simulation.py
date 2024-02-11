from time import sleep

def display(inp):
    print(inp)


def run_simulation(event):
    # TODO: here should be while loop that will get data from the dht
    try:
        while True:
            if event.is_set():
                return
            display("SIM\nTEMP:22.2\nHUM:33%")
            sleep(2)
    except KeyboardInterrupt:
        print("LCD simulation stopped by user.")
