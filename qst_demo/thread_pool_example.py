from concurrent.futures import ThreadPoolExecutor
import time


def test(pause=1):
    for i in range(3):
        print("-> Hello from 'test' - {}".format(i))
        time.sleep(pause)


executor = ThreadPoolExecutor(max_workers=2)
pause = 2

# Now we are waiting `test` to end printing.
executor.submit(test, pause)

print("End of script")
