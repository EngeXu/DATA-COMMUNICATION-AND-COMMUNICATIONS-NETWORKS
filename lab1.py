# -*- coding: utf-8 -*-
"""
# @file     mm1_lab1.py
# @author   Enge.Xu
# @date     2018-11-29
#
# @brief    Simulate M/M/1 queueing system
#
"""

import argparse
import numpy as np
import random
import simpy
import sys
import matplotlib.pyplot as plt



def source(env, mean_ia_time, mean_srv_time, server, wait_times, number, trace):
    """Generates packets with exponential interarrival time."""
    for i in range(number):
        ia_time = random.expovariate(1.0 / mean_ia_time)
        srv_time = random.expovariate(1.0 / mean_srv_time)
        pkt = packet(env, 'Packet-%d' % i, server, srv_time, wait_times, trace)
        env.process(pkt)
        yield env.timeout(ia_time)


def packet(env, name, server, service_time, wait_times, trace):
    """Requests a server, is served for a given service_time, and leaves the server."""
    global summ,queue_length,status_change_time
    
    # record arrival time
    arrv_time = env.now
    if trace:

        change_time= env.now - status_change_time
        
        # update at each packet arrival
        if queue_length > 0:
            # only waiting people will be calculate 
            summ=summ+(queue_length-1)*(change_time)
            
        queue_length = queue_length + 1
        
        status_change_time=env.now
        
    with server.request() as request:
        yield request
        # save wait time in a matrix
        wait_time = env.now - arrv_time
        wait_times.append(wait_time)
        
        yield env.timeout(service_time)
        # update at the end of each packet’s waiting in the queue  
        if trace:
           
            change_time = env.now - status_change_time
            
            if queue_length > 1:
                # only waiting people will be calculate
                summ = summ+(queue_length - 1)*(change_time)
            
            queue_length = queue_length - 1
            service_times.append(service_time)
            status_change_time = env.now


def run_simulation(mean_ia_time, mean_srv_time, num_packets=1000, random_seed=1234, trace=True):
    """Runs a simulation and returns statistics."""
    random.seed(random_seed)
    env = simpy.Environment()
    # start processes and run
    server = simpy.Resource(env, capacity=1)
    wait_times = []
    env.process(source(env, mean_ia_time,
                       mean_srv_time, server, wait_times, number=num_packets, trace=trace))
    env.run()

    # return mean waiting time
    return np.mean(wait_times)

# Initialize all variables
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-A",
        "--mean_ia_time",
        help="mean packet interarrival time [s]; default is 1",
        default=1,
        type=float)
    parser.add_argument(
        "-S",
        "--mean_srv_time",
        help="mean packet service time [s]; default is 1",
        default=1,
        type=float)
    parser.add_argument(
        "-N",
        "--num_packets",
        help="number of packets to generate; default is 1000",
        default=1000,
        type=int)
    parser.add_argument(
        "-R",
        "--random_seed",
        help="seed for random number generation; default is 1234",
        default=1234,
        type=int)
    parser.add_argument(
        "-SUMM",
        "--summ",
        help="the sum of the rectangles' area; default is 0",
        default=0,
        type=float)
    parser.add_argument(
        "-QL",
        "--queue_length",
        help="the number of packets in the queue; default is 0",
        default=0,
        type=float)
    parser.add_argument(
        "-SCT",
        "--status_change_time",
        help="the time interval between changes in this number; default is 0",
        default=0,
        type=float) 
    
    parser.add_argument('--trace', dest='trace', action='store_true')
    parser.add_argument('--no-trace', dest='trace', action='store_false')
    parser.set_defaults(trace=True)
    
    args = parser.parse_args()
    # set variables using command-line arguments
    mean_ia_time = args.mean_ia_time
    mean_srv_time = args.mean_srv_time
    num_packets = args.num_packets
    random_seed = args.random_seed
    trace = args.trace
    summ=args.summ
    queue_length=args.queue_length
    status_change_time=args.status_change_time
    
    mean_waiting_times=[] 
    al_waiting_times=[]
    service_times=[]
    servtime=[]
    servtimes=[]
      
    arrival_rate = 0.05
    # The while loop can calculate the average waiting time and service time for different arrival rates
    while arrival_rate < 1 :
        mean_ia_time = 1 / arrival_rate
        # the first way 
        mean_waiting_time = run_simulation(mean_ia_time, mean_srv_time, num_packets, random_seed, trace)
        mean_waiting_times.append(mean_waiting_time)
        # the second way
        average_length = summ / status_change_time
        al_waiting_time = average_length / arrival_rate
        al_waiting_times.append(al_waiting_time)
        servtime = np.mean(service_times)
        servtimes.append(servtime)
        
    #start the next loop
        arrival_rate = arrival_rate + 0.05
        summ=0
        status_change_time=0
        queue_length=0

    # plot the task1 figure
    plt.figure(1)
    y1=[]
    y1=np.squeeze(mean_waiting_times)
    x = np.linspace(0,1,19)
    plt.plot(x,y1, "x-", label="the first method")
    plt.ylabel('mean waiting times')
    plt.xlabel('arrival rate')
    y2=[]
    y2=np.squeeze(al_waiting_times)
    plt.plot(x,y2, "+-", label="the second method")
    plt.grid(True)

    plt.legend(loc = 0)
   
    plt.show()

    # plot the task2 figure
    plt.figure(2)
    y2=[]
    y2=np.squeeze(servtimes)
    x = np.linspace(0,1,19)
    plt.plot(x,y2)
    plt.ylabel('mean service times')
    plt.xlabel('arrival rate')
    plt.title("the second method")
    plt.show()
    

print("Average waiting time = %.4Es\n" % mean_waiting_time)

        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
