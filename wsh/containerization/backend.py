import docker
import os
from time import sleep
CWD = os.getcwd()

class worker_node():
    name = ''
    cpus = ''
    mem_limit = ''
    
    # time_before_exec = 0
    def __init__(self, name, cpus, mem_limit, net):
        self.name = name
        self.cpus = cpus
        self.mem_limit = mem_limit
        self.net = net
        self.container = None

    # I don't know why it does not contain ip, so I use hostname in network instead.
    def ip(self):
        network_setting, = self.container.attrs['NetworkSettings']['Networks'].values()
        print(self.container.attrs)
        return network_setting['IPAddress']

    # Run script in the container. If the container is not yet created, then run is used, otherwise
    # exec_run(docker exec) is used.
    def run_script(self, script, host, port, memory, sleep_time):
        if not self.container:
            self.container = client.containers.run(IMAGES,
            'python3 /root/runtime/{0} {1} {2} {3} {4}'.format(script, host, port, memory, sleep_time),
            detach=True, name=self.name,hostname=self.name, cpuset_cpus=self.cpus, network=self.net,
            mem_limit=self.mem_limit, volumes={CWD:{"bind":"/root/runtime", "mode":"rw"}})
        else:
            self.container.exec_run(detach=True,
                cmd='python3 /root/runtime/{0} {1} {2} {3} {4}'.format(script, host, port, memory, sleep_time))

    def __del__(self):
        if self.container:
            try:
                self.container.remove()
            except:
                sleep(2.5)
                self.container.remove()

    # class task():
    #     def __init__(self, mem, input, output):



if __name__ == '__main__':
    # specify image
    IMAGES = "test/alpine:latest"

    # initialize the client
    client = docker.from_env()
    cli = docker.APIClient(base_url='unix://var/run/docker.sock')
    # create network so that workers can resolve hostname
    networks = [net.name for net in client.networks.list()]
    if 'workers' not in networks:
        client.networks.create("workers", driver="bridge")
    # create workers here
    NUM_WORKERS = 4
    workers = [0]*NUM_WORKERS
    workers[0] = worker_node('worker-1', '0,1', '128m', "workers")
    workers[1] = worker_node('worker-2', '2,3', '128m', "workers")
    workers[2] = worker_node('worker-3', '4,5', '128m', "workers")
    workers[3] = worker_node('worker-4', '6,7', '128m', "workers")

    workers[0].run_script('t1.py', 'worker-2', '8080', 128, 0)
    workers[1].run_script('t2.py', 'localhost', '8080', 128, 3)
    workers[1].run_script('t3.py', 'worker-1', '8080', 128, 3)
    workers[1].run_script('t4.py', 'worker-1', '8080', 128, 3)
    workers[0].run_script('t7.py', 'localhost', '8080', 128, 3)
    workers[2].run_script('t8.py', 'localhost', '8080', 128, 3)
    workers[0].run_script('t5.py', 'worker-4', '8080', 128, 3)
    workers[2].run_script('t10.py', 'worker-4', '8080', 128, 3)
    workers[2].run_script('t11.py', 'worker-4', '8080', 128, 3)
    workers[3].run_script('t6.py', 'worker-4', '8080', 128, 3)
    workers[3].run_script('t9.py', 'localhost', '8080', 128, 3)
    workers[3].run_script('t12.py', 'localhost', '8080', 128, 3)
    # first run servers
    # workers[2].run_script('l2_1.py', 'worker-3', '8080', 128, 3)
    # # sleep(1)
    # #Then run containers does not need input
    # # host = workers[2].ip()
    # host = 'worker-3'
    # # print("worker-3 IP: ", host)
    # workers[0].run_script('l1_1.py', host, '8080', 128, 0)
    # workers[1].run_script('l1_2.py', host, '8080', 128, 0)
    # # print(cli.inspect_container(workers[2].name))
    # # sleep(10)
    exited = 0
    while exited < NUM_WORKERS:
        for i in range(NUM_WORKERS):
            try:
                # t = workers[i].container.top()
                code, out = workers[i].container.exec_run('top -n1')
                print(out[2:].decode('ascii'))
            except docker.errors.APIError as e:
                print(workers[i].name, e)
                exited = exited + 1
        sleep(0.5)
