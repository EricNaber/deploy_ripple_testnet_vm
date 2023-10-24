import os, time, threading


sem1 = threading.Semaphore(0)   # wait for t1
sem2 = threading.Semaphore(0)   # wait for t2


def execute_transaction1():
    os.system("docker exec -it validator_00 /bin/bash -c '/transaction1.sh'")


def execute_transaction_dest1():
    sem1.release()
    sem2.acquire()
    os.system("docker exec -it validator_00 /bin/bash -c '/transaction_dest1.sh'")
    print(f"\n************************ Thread 1 at {time.time()} ************************\n")


def execute_transaction_dest2():
    sem1.acquire()
    sem2.release()
    os.system("docker exec -it validator_10 /bin/bash -c '/transaction_dest2.sh'")
    print(f"\n************************ Thread 2 at {time.time()} ************************\n")


def main():
    # Execute transaction1.sh
    execute_transaction1()

    # Wait 5 seconds
    time.sleep(10)

    # Create two threads
    t1 = threading.Thread(target=execute_transaction_dest1)
    t2 = threading.Thread(target=execute_transaction_dest2)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__=="__main__":
    main()
