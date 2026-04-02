import time

def PlayTimer():
    minutos = 0
    while True:
        for i in range(60):
            print(f"\rProgreso: {minutos}:{i:02d}", end="")
            time.sleep(1)
        minutos += 1