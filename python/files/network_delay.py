import os, re

# This python-file creates a command that introduces network-delay to all docker-networks.
# The build command leverages tc and therefore might not work on all OSes. It does work on linux.

def main():
    delay = input("How much delay (ms) should be introduced to the network? ")
    assert(delay.isnumeric() and int(delay) >= 0)
    
    option = input("Add (A) or change (c) network delay? ").lower()
    if option == "" or option == "a": option = "add"
    elif option == "c": option = "change"
    assert(option == "add" or option == "change")

    net_devices = os.listdir(os.path.join("/proc", "sys", "net", "ipv6", "conf"))

    docker_net_devices = [device_name for device_name in net_devices if "veth" in device_name]

    command = f"sudo tc qdisc {option} dev {docker_net_devices[0]} root netem delay {delay}ms"
    for device in docker_net_devices[1:]:
        command += f" && \\\nsudo tc qdisc {option} dev {device} root netem delay {delay}ms"
    
    print(f"\n{command}")
    os.system(command)


if __name__=="__main__":
    try:
        main()
    except BaseException as err:
        print(f"Something went wrong: {err}")

