 # -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 14:24:06 2022

@author: Surface
"""

#imports 
import sys
import numpy as np 
import math
import random 
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# =============================================================================
# =============================================================================
# # FUNCTIONS
# =============================================================================
# =============================================================================

#periodic boundary conditions function
def pbc(pos, l):
    # Use mod function to find position of particle within pbc
    return np.mod(pos, l)


# =============================================================================
# Game of Life Functions
# =============================================================================

def update_lattice(new_lattice, N):
    updated_lattice = np.zeros((N,N), dtype=int)    
    for i in range(N):
        for j in range(N):
                updated_lattice[i,j] = new_lattice[i,j]
    return updated_lattice

def rules_gol(lattice, new_lattice, N):                
    total = int(lattice[pbc(i+1,N),j]+lattice[pbc(i-1,N),j]+lattice[i,pbc(j+1,N)]
            +lattice[i,pbc(j-1,N)]+lattice[pbc(i+1,N),pbc(j+1,N)]+lattice[pbc(i+1,N),pbc(j-1,N)]
            +lattice[pbc(i-1,N),pbc(j+1,N)]+lattice[pbc(i-1,N),pbc(j-1,N)])
    if lattice[i,j] == 1:
        if total == 2 or total == 3:
            new_lattice[i,j] = 1
        else:
            new_lattice[i,j] = 0       
    else:
        if total == 3:
            new_lattice[i,j] = 1
        else:
            new_lattice[i,j] = 0
    return new_lattice

def rand(new_lattice, lattice, N):
    for i in range(N):
        for j in range(N):
            #generate a random number between 0 and 1
            new_lattice[i,j] = lattice[i,j] = np.random.choice([0,1])
    return lattice, new_lattice
        
def glide(new_lattice, lattice, N):
    i = random.randint(0,N-1)
    j = random.randint(0,N-1)
    new_lattice[i,j] = lattice[i,j] = 1
    new_lattice[pbc(i+1,N),j] = lattice[pbc(i+1,N),j] = 1
    new_lattice[pbc(i-1,N),j] = lattice[pbc(i-1,N),j] = 1
    new_lattice[pbc(i+1,N),pbc(j+1,N)] = lattice[pbc(i+1,N),pbc(j+1,N)] = 1
    new_lattice[i,pbc(j+2,N)] = lattice[i,pbc(j+2,N)] = 1
    return lattice, new_lattice

def blink(new_lattice, lattice, N):
    i = random.randint(0,N-1)
    j = random.randint(0,N-1)
    new_lattice[i,j] = lattice[i,j] = 1
    new_lattice[pbc(i+1,N),j] = lattice[pbc(i+1,N),j] = 1
    new_lattice[pbc(i-1,N),j] = lattice[pbc(i-1,N),j] = 1
    return lattice, new_lattice
    
def equilibration(count):
    for i in range(9, len(count)):
        if len(count)>9:
            if count[i]==count[i-1]==count[i-2]==count[i-3]==count[i-4]==count[i-5]==count[i-6]==count[i-7]==count[i-8]==count[i-9]:
                return True
                break
        else:
            return False

def com(lattice, N):
    rx = []
    ry = []
    for i in range(N):
        for j in range(N): 
            if lattice[i, j] == 1:
                r_i = i
                r_j = j
                rx.append(r_i)
                ry.append(r_j)
    comx = np.sum(rx)/len(rx)
    comy = np.sum(ry)/len(ry)
    return comx, comy

def com_bounds(com_list):        
    for i in range(len(com_list)-1):
        if abs(com_list[i]-com_list[i+1]) > 4:
            com_list[i]=np.nan
        else:
            com_list[i]=com_list[i]
    return com_list

# =============================================================================
# SIRS Functions
# =============================================================================

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

def rules_sirs(lattice, p1, p2, p3):
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

# =============================================================================
# =============================================================================
# # SIMULATIONS
# =============================================================================
# =============================================================================

sim = str(input(">>>simulation (GoL/SIRS) = "))

# =============================================================================
# Game of Life Simulation
# =============================================================================

if sim == "GoL":
  
    ic = str(input(">>>initial conditions = "))            
    steps = int(input(">>>number of steps = ")) 
    N = int(input(">>>lattice dimensions = "))     
    animate = input(">>>animate (Y/N) = ") 
    
    #create empty lattices 
    new_lattice0 = np.zeros((N,N), dtype=int) 
    lattice0 = np.zeros((N,N), dtype=int)
    
    #iterate through points of the lattice 
    if ic == "random":
        
        simulations = int(input(">>>number of simulations = ")) 
        
        t_list = []
        e_time_list = []    
     
        for n in range(1, simulations+1):
            count_list = []
            print(n)
            lattice, new_lattice = rand(new_lattice0, lattice0, N)
            for t in range(steps):
                if t%100==0:
                    print(t)
                count = 0
                t_list.append(t)
                
                for i in range(N):
                    for j in range(N):
                        if lattice[i,j] == 1:
                            count+=1
                        new_lattice = rules_gol(lattice, new_lattice, N)
            
                count_list.append(count)
                lattice = update_lattice(new_lattice, N)    
                
                if animate == 'Y':        
                    if(t % 10 == 0):  
                        #show animation
                        plt.cla()
                        im=plt.imshow(lattice, animated=True, vmin=-1, vmax=1)
                        plt.gca().invert_yaxis()
                        plt.draw()
                        plt.pause(0.0001)
                        
                if equilibration(count_list) == True:
                    e_time_list.append(int(t-9))
                    print(t-9)
                    break
                else:
                    continue
                
        if simulations==1:
            #produce plots
            plt.title("Evolution of living cells")
            plt.xlabel("Time Step")
            plt.ylabel("Number of living cells")
            plt.plot(t_list, count_list)
            plt.show()
            
            #write data to files
            # f = open('evolution.dat','w')
            # for v in range(len(t_list)):
            #     f.write(str(t_list[v]) + ": " + str(count_list[v]) + "\n")
            # f.close()
        
        else:
            e_time_list.sort()
            std_e = np.std(e_time_list)
            num = len(e_time_list)
            bins = int(1+np.log2(len(e_time_list))) #sturges rule for bin size
            print(bins) 
            max = np.max(e_time_list)
            min = np.min(e_time_list)
            entries, binedges = np.histogram(e_time_list, bins, range=(0,max))
    
            # Define the x data as bin centres
            xdata = (binedges[:-1]+binedges[1:])/2
            #print(xdata)
            # Define the y data as bin entries
            ydata = entries
            #print(ydata)
            # Calculate binwdiths 
            binwidth = binedges[1]-binedges[0]
            
            #write data to files
            # f = open('equilibration.dat','w')
            # for v in range(len(xdata)):
            #     f.write(str(xdata[v]) + ": " + str(ydata[v]) + "\n")
            # f.close()
                    
            #produce plots
            plt.title("Equilibration Histogram")
            plt.xlabel("Time Step")
            plt.ylabel("Number of Simulations")
            plt.bar(xdata, ydata, width=binwidth)
            plt.show()
            
                
    if ic == "glider":
    
        t_list = []
        comx_list = []
        comy_list = []
        
        lattice, new_lattice = glide(new_lattice0, lattice0, N)  
    
        for t in range(steps):
            if t%10==0:
                t_list.append(t)
                print(t)
                CoMx, CoMy = com(lattice, N) 
                comx_list.append(CoMx)
                comy_list.append(CoMy)
            for i in range(N):
                for j in range(N):
                    new_lattice = rules_gol(lattice, new_lattice, N)
    
            lattice = update_lattice(new_lattice, N)
            
            if animate == 'Y':        
                if(t % 10 == 0):  
                    #show animation
                    plt.cla()
                    im=plt.imshow(lattice, animated=True, vmin=-1, vmax=1)
                    plt.gca().invert_yaxis()
                    plt.draw()
                    plt.pause(0.0001)
                    
        print(comx_list)
        print(comy_list)

        comx_list = com_bounds(comx_list)  
        comy_list = com_bounds(comy_list)
        
        # #write data to files
        # f = open('comx.dat','w')
        # for v in range(len(t_list)):
        #     f.write(str(t_list[v]) + ": " + str(comx_list[v]) + "\n")
        # f.close()
        
        # #write data to files
        # f = open('comy.dat','w')
        # for v in range(len(t_list)):
        #     f.write(str(t_list[v]) + ": " + str(comy_list[v]) + "\n")
        # f.close()

    
        #produce plots
        plt.title("CoM of Glider")
        plt.xlabel("Time Step")
        plt.ylabel("CoM")
        plt.plot(t_list, comx_list, label="CoM X")
        plt.plot(t_list, comy_list, label="CoM Y")  
        plt.legend(loc="upper right")
        plt.show()
        
        x1 = int(int(input(">>>lower x = "))/10)
        x2 = int(int(input(">>>upper x = "))/10)
        
        m, b = np.polyfit(t_list[x1:x2], comx_list[x1:x2], 1)
        print("CoM velocity = ", m)
        
    if ic == "blinker":
        
        lattice, new_lattice = blink(new_lattice0, lattice0, N)
        
        for t in range(steps):
            if t%10==0:
                print(t)                
            for i in range(N):
                for j in range(N):
                    new_lattice = rules_gol(lattice, new_lattice, N)
                    
            lattice = update_lattice(new_lattice, N)
            
            if animate == 'Y':        
                if(t % 1 == 0):  
                    #show animation
                    plt.cla()
                    im=plt.imshow(lattice, animated=True, vmin=-1, vmax=1)
                    plt.gca().invert_yaxis()
                    plt.draw()
                    plt.pause(0.0001)
                    
# =============================================================================
#  SIRS Simulation                  
# =============================================================================
                    
if sim == "SIRS":
    
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
            if t%100==0:
                print(t)
            count = infect_count(lattice)
            for a in range(N*N):
                lattice = rules_sirs(lattice, p1, p2, p3)
        
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
                    if t%100==0:
                        print(t)    
                    count = infect_count(lattice)
                    frac = count/(N*N)
                    frac_list.append(frac)       
                    for a in range(N*N):
                        lattice = rules_sirs(lattice, p1, p2, p3)
                
                    if animate == 'Y':        
                        if(t % 1 == 0):                  
                            plt.cla()
                            im=plt.imshow(lattice, animated=True, vmin=-1, vmax=2)
                            plt.draw()
                            plt.pause(0.0001)
                
                frac_5avg.append(np.mean(frac_list))
                
            frac_avg_all.append(np.mean(frac_5avg))
            std.append(np.std(frac_5avg)/np.sqrt(len(frac_5avg)))
            
        # #write data to files
        # f = open('infected_frac.dat','w')
        # for v in range(len(If_list)):
        #     f.write(str(If_list[v]) + ": " + str(frac_avg_all[v]) + "\n")
        # f.close()        
        
        plt.title("Infected Fraction vs Fraction of Imunity")
        plt.xlabel("Immunity Fraction")
        plt.ylabel("Infected Fraction")
        plt.errorbar(If_list, frac_avg_all, yerr=std)
        plt.show()
                   
    if vis == "p1p3":
        
        steps = int(input(">>>number of steps (>100) = "))  
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
                        lattice = rules_sirs(lattice, p1_list[i], p2, p3_list[j]) 
                                   
                var[i,j] = ((np.mean(count_sq_list)-np.mean(count_list)**2)/N**2)
                count_arr[i,j] = np.mean(count_list)/(N*N) 
                
        # #write data to files
        # f = open('contour.dat','w')
        # for v in range(len(count_arr)):
        #     for w in range(len(count_arr[0])):
        #         f.write(str(v) + ", " + str(w) + ": " + str(count_arr[v,w]) + "\n")
        # f.close()
        
        # f = open('contour_var.dat','w')
        # for v in range(len(var)):
        #     for w in range(len(var[0])):
        #         f.write(str(v) + ", " + str(w) + ": " + str(var[v,w]) + "\n")
        # f.close()        
    
        X, Y = np.meshgrid(p1_list, p3_list)
        
        contour = plt.contour(X, Y, count_arr)
        contour_fill = plt.contourf(X, Y, count_arr)
        plt.colorbar()
        plt.title("p1-p3 Plane Count")
        plt.xlabel("p1")
        plt.ylabel("p3")
        plt.get_cmap("viridis")
        plt.show()
        plt.savefig('contour.png')
        
        contour2 = plt.contour(X, Y, var) 
        contour2_fill = plt.contourf(X, Y, var)
        plt.colorbar()
        plt.title("p1-p3 Plane Variance")
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
                if t%100==0:
                    print(t)
                if t>100:
                    count_list.append(infect_count(lattice))
                    count_sq_list.append(infect_count(lattice)**2)
                for a in range(N*N):
                    lattice = rules_sirs(lattice, p1_list[i], p2, p3) 
                                   
            var.append((np.mean(count_sq_list)-np.mean(count_list)**2)/N**2)
            
            #bootstrap error
            m = 0
            var_s_list = []
            while m <= 1000:
                #get sample (with replacment)
                s = np.random.choice(count_list, len(count_list))
                avg_s = np.mean(s)
                avg_s_sq = np.array(s)**2
                #calculate variance
                var_s = (np.mean(avg_s_sq)-(avg_s**2))/N**2
                #append variance of sample to a list of all smaple variances
                var_s_list.append(var_s)
                m += 1
                #calculate variance and standard deviation of sample data  
            variance = (np.mean(np.array(var_s_list)**2)-np.mean(var_s_list)**2)/N**2
            std = variance**(1/2) 
            errors.append(std)
            
        # #write data to files
        # f = open('variance.dat','w')
        # for v in range(len(p1_list)):
        #     f.write(str(p1_list[v]) + ": " + str(var[v]) + "\n")
        # f.close()
            
        plt.title("Fixed p2 and p3")
        plt.xlabel("p1")
        plt.ylabel("Variance")
        plt.errorbar(p1_list, var, yerr=errors)
        plt.show()
                
        