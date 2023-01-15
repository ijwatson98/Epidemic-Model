# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 14:30:30 2022

@author: Surface
"""

#imports 
import sys
import numpy as np 
import math
import random 
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def pbc(pos, l):
    # Use mod function to find position of particle within pbc
    return np.mod(pos, l)

def init_lattice(N):
    #create empty lattice 
    lattice = np.zeros((N,N), dtype=int)
    for i in range(N):
        for j in range(N):
            #generate a random number between 0 and 1
            lattice[i,j] = random.randint(-1,1) #0-suscept, 1-recovered, -1-infected
    return lattice

def immune_lattice(N, If):
    #create empty lattice 
    lattice = np.zeros((N,N), dtype=int)
    for i in range(N):
        for j in range(N):
            #generate a random number between 0 and 2
            if random.random() <= If:
                lattice[i,j] = 2 #2-immune
            else:
               lattice[i,j] = random.randint(-1,1) #0-suscept, 1-recovered, -1-infected 

    return lattice

def rand_coord(lattice):
    i = random.randint(0,N-1)
    j = random.randint(0,N-1)
    return i, j

def infect_nn(lattice, i, j, p1):
    if random.random() <= p1: 
        if lattice[i,pbc(j+1,N)]==-1:
            return True
        if lattice[i,pbc(j-1,N)]==-1:
            return True
        if lattice[pbc(i+1,N),j]==-1:
            return True
        if lattice[pbc(i-1,N),j]==-1:
            return True  
    else:
        return False

def recov(p2):
    if random.random() <= p2:
        return True
    else:
        return False
    
def suscept(p3):
    if random.random() <= p3:
        return True
    else:
        return False
        
def infect_count(lattice):
    count = 0
    for i in range(N):
        for j in range(N):
            if lattice[i,j] == -1:
                count+=1
    return count 

def rules(lattice, p1, p2, p3):
    x, y = rand_coord(lattice)
    if lattice[x,y]==0:
        if infect_nn(lattice,x,y,p1)==True:
            lattice[x,y]=-1
    elif lattice[x,y]==-1:
        if recov(p2)==True:
            lattice[x,y]=1 
    elif lattice[x,y]==1:
        if suscept(p3)==True:
            lattice[x,y]=0
    return lattice
    

vis = str(input(">>>visual (observe/immunity/p1p3/variance) = "))

if vis == "observe": 

    p1 = float(input(">>>p1 = "))
    p2 = float(input(">>>p2 = "))    
    p3 = float(input(">>>p3 = "))            
    steps = int(input(">>>number of steps = ")) 
    N = int(input(">>>lattice dimensions = "))    
    animate = input(">>>animate (Y/N) = ")
    
    lattice = init_lattice(N)
    
    for t in range(steps):
        count = infect_count(lattice)
        for a in range(N*N):
            lattice = rules(lattice, p1, p2, p3)
    
        if animate == 'Y':        
            if(t % 1 == 0):  
                #show animation
                plt.cla()
                im=plt.imshow(lattice, animated=True, vmin=-1, vmax=1)
                plt.draw()
                plt.pause(0.0001)
                
if vis == "immunity": 
    
    p1 = float(input(">>>p1 = "))
    p2 = float(input(">>>p2 = "))    
    p3 = float(input(">>>p3 = "))            
    steps = int(input(">>>number of steps = ")) 
    N = int(input(">>>lattice dimensions = ")) 
    animate = input(">>>animate (Y/N) = ")
    
    frac_avg_all = []
    If_list = np.linspace(0,1,20)
    
    std = []
    
    for If in If_list:
        print(If)
        frac_5avg = []
        for r in range(5):
            lattice = immune_lattice(N, If)
            frac_list = []
            for t in range(steps):
                count = infect_count(lattice)
                frac = count/(N*N)
                frac_list.append(frac)       
                for a in range(N*N):
                    lattice = rules(lattice, p1, p2, p3)
            
            frac_5avg.append(np.mean(frac_list))
     
        frac_avg_all.append(np.mean(frac_5avg))
        std.append(np.std(frac_5avg)/np.sqrt(len(frac_5avg)))
   
    # for If in If_list:
    #     lattice = immune_lattice(N, If)
    #     frac_list = []
    #     for t in range(steps):
    #         count = infect_count(lattice)
    #         frac = count/(N*N)
    #         frac_list.append(frac)       
    #         for a in range(N*N):
    #             lattice = rules(lattice, p1, p2, p3)
                
    #     frac_avg_all.append(np.mean(frac_list))    
        
        if animate == 'Y':        
            if(t % 1 == 0):                  
                plt.cla()
                im=plt.imshow(lattice, animated=True, vmin=-1, vmax=2)
                plt.draw()
                plt.pause(0.0001)
    
    plt.title("")
    plt.xlabel("Immunity Fraction")
    plt.ylabel("Infected Fraction")
    plt.plot(If_list, frac_avg_all)
    plt.errorbar(If_list, frac_avg_all, yerr=std)
    plt.show()
               

if vis == "p1p3":
    
    steps = int(input(">>>number of steps = "))  
    N = int(input(">>>lattice dimensions = "))    
    
    p2 = 0.5    
    p1_list = np.linspace(0,1,20)
    p3_list = np.linspace(0,1,20)
    M = len(p1_list)
    
    count_arr = np.zeros([M,M], dtype=float)
    var = np.zeros([M,M], dtype=float)
    
    for i in range(M):
        print(p1_list[i])  
        for j in range(M):
            lattice = init_lattice(N)
            count_list = []
            count_sq_list = []
            for t in range(steps):
                if t>100:
                    count_list.append(infect_count(lattice))
                    count_sq_list.append(infect_count(lattice)**2)
                for a in range(N*N):
                    lattice = rules(lattice, p1_list[i], p2, p3_list[j]) 
                               
            var[i,j] = ((np.mean(count_sq_list)-np.mean(count_list)**2)/N)
            count_arr[i,j] = np.mean(count_list)/(N*N)    

    X, Y = np.meshgrid(p1_list, p3_list)
    
    contour = plt.contour(X, Y, count_arr)
    contour_fill = plt.contourf(X, Y, count_arr)
    plt.colorbar()
    plt.title('p1-p3 Plane Count')
    plt.xlabel("p1")
    plt.ylabel("p3")
    plt.get_cmap("viridis")
    plt.show()
    
    contour2 = plt.contour(X, Y, var) 
    contour2_fill = plt.contourf(X, Y, var)
    plt.colorbar()
    plt.title('p1-p3 Plane Variance')
    plt.xlabel("p1")
    plt.ylabel("p3")
    plt.get_cmap("plasma")
    plt.show()
         
if vis == "variance":
    
    steps = int(input(">>>number of steps = "))  
    N = int(input(">>>lattice dimensions = "))    
    
    p2 = 0.5
    p3 = 0.5    
    p1_list = np.linspace(0.2,0.5,7)
    M = len(p1_list)

    var = []
    errors = []
    
    for i in range(M):
        print(p1_list[i]) 
        lattice = init_lattice(N)
        count_list = []
        count_sq_list = []
        for t in range(steps):
            if t>100:
                count_list.append(infect_count(lattice))
                count_sq_list.append(infect_count(lattice)**2)
            for a in range(N*N):
                lattice = rules(lattice, p1_list[i], p2, p3) 
                               
        var.append((np.mean(count_sq_list)-np.mean(count_list)**2)/N)
        
        #bootstrap error
        m = 0
        var_s_list = []
        while m <= 1000:
            #get sample (with replacment)
            s = np.random.choice(count_list, len(count_list))
            avg_s = np.mean(s)
            avg_s_sq = np.array(s)**2
            #calculate variance
            var_s = (np.mean(avg_s_sq)-(avg_s**2))/N
            #append variance of sample to a list of all smaple variances
            var_s_list.append(var_s)
            m += 1
            #calculate variance and standard deviation of sample data  
        variance = (np.mean(np.array(var_s_list)**2)-np.mean(var_s_list)**2)
        std = variance**(1/2) 
        errors.append(std)
        
    plt.title("Fixed p2 and p3")
    plt.xlabel("p1")
    plt.ylabel("Variance")
    plt.errorbar(p1_list, var, yerr=errors)
    plt.show()
   

     
        
