# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 11:03:48 2022

@author: asus
"""
import matplotlib.pyplot as plt
import math
import numpy as np
import random
import imageio
import os

def generate_wall(num, h, w):
    walls = []
    while(len(walls) < num):
        px = random.uniform(0, w)
        py = random.uniform(0, h)
        # ori = random.uniform(0, math.pi)
        ori = 0
        if([px, py, ori] not in walls):
            walls.append([px, py, ori])
    return [h, w, walls]

def draw_environment(ax, env, wall_len):
    h, w, walls = env
    ax.set_ylim([0, h])
    ax.set_xlim([0, w])
    point_x = []
    point_y = []
    for i in range(len(walls)):
        px = walls[i][0]
        py = walls[i][1]
        ori = walls[i][2]
        
        # draw line
        ax.plot([px- math.cos(ori)* wall_len/2, px+ math.cos(ori)* wall_len/2], 
                [py- math.sin(ori)* wall_len/2, py+ math.sin(ori)* wall_len/2], 'b-', lw=5)
        
        # center point of wall
        point_x.append(px)
        point_y.append(py)
    
    ax.scatter(point_x, point_y, color='red', linewidths=4)

def draw_walls(env, wall_len):
    h, w, walls = env
    plt.ylim([0, h])
    plt.xlim([0, w])
    point_x = []
    point_y = []
    for i in range(len(walls)):
        px = walls[i][0]
        py = walls[i][1]
        ori = walls[i][2]
        
        # draw line
        plt.plot([px- math.cos(ori)* wall_len/2, px+ math.cos(ori)* wall_len/2], 
                [py- math.sin(ori)* wall_len/2, py+ math.sin(ori)* wall_len/2], 'b-', lw=5)
        
        # center point of wall
        point_x.append(px)
        point_y.append(py)
    
    plt.scatter(point_x, point_y, color='red', linewidths=4)

def radian_check(r):
    while(r>2* math.pi):
        r = r - 2* math.pi
    while(r<0):
        r = r + 2* math.pi
    else:
        pass
    return r

def Move(robot, particles):
    rx = robot[0]
    ry = robot[1]
    r_ori = robot[2]
    stddev_m = 0.1
    stddev_a = 0.01
    
    # motion command
    command_m = 0
    angle = 0
    distance = 0
    
    # Move: robot
    count = 0
    while(True):
        # command_m = random.uniform(0, np.sqrt(9**2 + 3**2)) # maximum distance is the diagonal of the boundary
        command_m = random.uniform(0, 1)
        # turn
        angle = math.radians(random.normalvariate(mu=0, sigma=command_m* stddev_a))
        
        # move forward
        distance = random.normalvariate(mu=command_m, sigma=stddev_m* command_m)
        
        # check boundary condition
        new_rx = rx + distance* math.cos(r_ori + angle)
        new_ry = ry + distance* math.sin(r_ori + angle)
        
        if(new_rx<=9 and new_rx>=0 and new_ry<=3 and new_ry>=0):
            robot[0] = new_rx
            robot[1] = new_ry
            robot[2] = radian_check(r_ori + angle)
            # print('robot move: distance={}, angle={}'.format(distance, angle))
            break
        else:
            if(count < 5):
                count = count + 1
            else:
                command_m = 0
                angle = 0
                distance = 0
                # print('robot move: distance={}, angle={}'.format(distance, angle))
                break
    
    # Move: particles
    for i in range(len(particles)):
        px = particles[i][0]
        py = particles[i][1]
        p_ori = particles[i][2]
        
        # check boundary condition
        new_px = px + distance* math.cos(p_ori + angle)
        new_py = py + distance* math.sin(p_ori + angle)
        
        if(new_px <= 9 and new_px >= 0 and new_py <= 3 and new_py >= 0):
            particles[i][0] = new_px
            particles[i][1] = new_py
            particles[i][2] = radian_check(p_ori + angle)
            # print('particle move: distance={}, angle={}'.format(distance, angle))
        else:
            # print('particle move: distance={}, angle={}'.format(distance, angle))
            pass
        
    
                
        
def Turn(robot, particles):
    r_ori = robot[2]
    stddev_a = 0.01
    
    # Turn: robot
    command_t = random.uniform(0, 360)
    angle = math.radians(random.normalvariate(mu=command_t, sigma=command_t* stddev_a))
    # update orientation
    robot[2] = radian_check(r_ori + angle)
    # print("Turn: dr={}".format(angle))
    
    # Turn: particles
    for i in range(len(particles)):
        particles[i][2] = radian_check(particles[i][2]+ angle)

def Motion_model(robot, particles):
    command = random.randint(0, 3)
    
    if(command==0):
        # print('Command0:')
        Move(robot, particles)
    elif(command==1):
        # print('Command1:')
        Turn(robot, particles)
    elif(command==2):
        # print('Command2:')
        Move(robot, particles)
        Turn(robot, particles)
    else:
        # print('Command3:')
        Turn(robot, particles)
        Move(robot, particles)

def cal_distance(a, b):
    return np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def help_sensor(particle, wall, d, sigma_d, sigma_angle, sigma_orientation):
    dist = random.normalvariate(mu=d, sigma=d* sigma_d)
    angle = radian_check(random.normalvariate(mu=np.arctan(wall[1]/wall[0]+0.001)-np.arctan(particle[1]/particle[0]+0.001)
                                              , sigma=d* sigma_angle))
    orientation = radian_check(random.normalvariate(mu=particle[2]-wall[2], sigma=d* sigma_orientation))
    return dist, angle, orientation

def Sensor_model(particle, walls):
    # check whether in the visual domain
    walls_in_domain = []
    for i in range(len(walls)):
        # relative cooridinate to particle
        w_x = walls[i][0] - particle[0]
        w_y = walls[i][1] - particle[1]
        w_ori = np.arctan(w_y/w_x)
        if(w_x>0 and w_y>0): # 第一象限
            pass
        elif(w_x<0 and w_y>0): # 第二象限
            w_ori = w_ori + math.radians(180)
        elif(w_x<0 and w_y<0): #第三象限
            w_ori = w_ori + math.radians(180)
        elif(w_x>0 and w_y<0): # 第四象限
            pass
        else:
            pass
        
        # determine
        if(abs(w_ori-particle[2])<math.radians(40)):
            walls_in_domain.append(walls[i])
        
    # detect or not detect
    walls_detect = []
    for i in range(len(walls_in_domain)):
        d = cal_distance([particle[0], particle[1]], [walls_in_domain[i][0], walls_in_domain[i][1]])
        
        # case1: d>=1
        if(d >= 1):
            if(random.random() <= 0.1):
                dist, angle, orientation = help_sensor(particle, walls_in_domain[i], d, 0.1, 0.05, 0.3)
                walls_detect.append([dist, angle, orientation])
            else:
                if(random.random() < 0.05): #0.95
                    dist = random.uniform(1, 3)
                    angle = random.uniform(-math.radians(40), math.radians(40)) + particle[2]
                    orientation = random.uniform(0, 2* math.pi)
                    walls_detect.append([dist, angle, orientation])
        # case2: 0.5<=d<1
        elif(d >= 0.5):
            if(random.random() <= 0.8):
                dist, angle, orientation = help_sensor(particle, walls_in_domain[i], d, 0.01, 0.01, 0.1)
                walls_detect.append([dist, angle, orientation])
            else:
                if(random.random() < 0.1): #0.9
                    dist = random.uniform(0.5, 1)
                    angle = random.uniform(-math.radians(40), math.radians(40)) + particle[2]
                    orientation = random.uniform(0, 2* math.pi)
                    walls_detect.append([dist, angle, orientation])
        
        # case3: 0<=d<0.5
        else:
            if(random.random() <= 0.6):
                dist, angle, orientation = help_sensor(particle, walls_in_domain[i], d, 0.05, 0.1, 10)
                walls_detect.append([dist, angle, orientation])
            else:
                if(random.random() < 0.01): #0.99
                    dist = random.uniform(0,0.5)
                    angle = random.uniform(-math.radians(40), math.radians(40)) + particle[2]
                    orientation = random.uniform(0, 2* math.pi)
                    walls_detect.append([dist, angle, orientation])
                    
    return walls_detect

            
def cal_weight(p_detect, r_detect): # dist, angle, orientation
    # particle
    if(len(p_detect)==0): return 0
    
    p_dis = 0
    p_angle = 0
    p_ori = 0
    for p in p_detect:
        p_dis = p_dis + p[0]
        p_angle = p_angle + p[1]
        p_ori = p_ori + p[2]
    
    r_dis = 0
    r_angle = 0
    r_ori = 0
    for r in r_detect:
        r_dis = r_dis + r[0]
        r_angle = r_angle + r[1]
        r_ori = r_ori + r[2]
    
    # distance weight
    dis_weight = 100 / abs(p_dis-r_dis+0.01)
    
    # angle weight
    angle_weight = 1 / abs(p_angle-r_angle+0.01)
    
    # orientation weight
    ori_weight = 1 / abs(p_ori-r_ori+0.01)
    
    total_weight = dis_weight + angle_weight + ori_weight
    
    # panelty
    panelty = 100
    if(len(p_detect) > len(r_detect)):
        total_weight = total_weight - (len(p_detect) - len(r_detect))* panelty
    elif(len(p_detect) < len(r_detect)):
        total_weight = total_weight + (len(p_detect) - len(r_detect))* panelty
    else: pass
    
    if(total_weight < 0): total_weight = 0
    return total_weight

def resample(N, particle, weights_and_index):
    new_particle = []
    weights = []
    for i in range(len(weights_and_index)):
        weights.append(weights_and_index[i][0])
    
    if(sum(weights)==0):
        for i in range(N):
            px = random.uniform(0, 9)
            py = random.uniform(0, 3)
            ori = random.uniform(0, 2* math.pi)
            new_particle.append([px, py, ori])
    else:
        ## n effective particles
        weights = np.array(weights)
        n_effective = np.sum(weights)**2 / np.sum(weights**2)
        print("n_effective:", n_effective)
        if(n_effective >= int(0.7*N)): return particle
        
        
        ## resample
        weights = weights / np.sum(weights)
        print("resample...")
        cweights = np.cumsum( weights )
        
        # 20% will be retained
        weights_and_index = sorted(weights_and_index, reverse=True)
        for i in range(int(N*0.2)):
            new_particle.append(particle[weights_and_index[i][1]])
        
        # 80% resample
        for i in range(int(N*0.8)):
            r = random.random()
            part = 0
            for pr in range( len( cweights ) ):
                if ( r < cweights[pr]  or pr == len(cweights) - 1):
                    part = pr
                    break
            while(True):
                new_px = random.normalvariate(mu=particle[part][0], sigma=0.05)
                new_py = random.normalvariate(mu=particle[part][1], sigma=0.05)
                new_ori = random.normalvariate(mu=particle[part][2], sigma=np.pi/20)
                if(new_px <= 9 and new_px >=0 and new_py <= 3 and new_py >= 0):
                    # new_particle.append(particle[part])
                    new_particle.append([new_px, new_py, new_ori])
                    break
        # 10% will generated randomly
        # for i in range(int(N*0.1)):
        #     r = random.random()
        #     part = 0
        #     for pr in range( len( cweights ) ):
        #         if ( r < cweights[pr]  or pr == len(cweights) - 1):
        #             part = pr
        #             break
        #     while(True):
        #         new_px = random.normalvariate(mu=particle[part][0], sigma=0.1)
        #         new_py = random.normalvariate(mu=particle[part][1], sigma=0.1)
        #         new_ori = random.normalvariate(mu=particle[part][2], sigma=np.pi/10)
        #         if(new_px <= 9 and new_px >=0 and new_py <= 3 and new_py >= 0):
        #             # new_particle.append(particle[part])
        #             new_particle.append([new_px, new_py, new_ori])
        #             break

    return new_particle

def particle_filter(N_obstacle, N_particle, iteration):
    ''' generate environment '''
    # initialize
    h = 3
    w = 9
    wall_len = 0.5
    
    # generate environment
    env = generate_wall(N_obstacle, h, w)
    
    
    ''' particle filter '''
    # Initialize
    walls = env[2]
    
    # robot position
    robot = [9/2, 3/2, 0]
    p_x = []
    p_y = []
    p_ori = []
    
    # particle position
    particle = []
    for i in range(N_particle):
        px = random.uniform(0, w)
        py = random.uniform(0, h)
        ori = random.uniform(0, 2* math.pi)
        # ori = 0
        particle.append([px, py, ori])
        p_x.append(px)
        p_y.append(py)
        p_ori.append(ori)
    
    # start iterations
    filenames = []
    for i in range(iteration):
        print("iteration: {}......".format(i+1))
        
        # robot move and particle gets the same command and movements
        while(True):
            Motion_model(robot, particle)
            r_detect = Sensor_model(robot, walls)
            if(len(r_detect)>0):
                break
            else:
                pass
    
        # calculate particle weight by robot's sensing
        weights = []
        for j in range(len(particle)):
            p_detect = Sensor_model(particle[j], walls)
            weight = cal_weight(p_detect, r_detect)
            print("weight:", weight)
            weights.append([weight, j])
            
        # resample
        particle = resample(N_particle, particle, weights)
        
        # update particle position
        for j in range(len(particle)):
            p_x[j] = particle[j][0]
            p_y[j] = particle[j][1]
            p_ori[j] = particle[j][2]
        
        # save picture for animation
        draw_walls(env, wall_len)
        plt.title('iteration: {}'.format(i))
        plt.xlabel('x')
        plt.ylabel('y')
        plt.scatter(robot[0], robot[1], color='green', linewidths=15)  
        plt.scatter(p_x[0 : int(-N_particle*0.1)], p_y[0 : int(-N_particle*0.1)], color='yellow', linewidths=3)
        plt.scatter(robot[0]+0.1*np.cos(robot[2]), robot[1]+0.1*np.sin(robot[2]), color='black', linewidths=1)
        plt.savefig('particle_filter{}.png'.format(i))
        filenames.append('particle_filter{}.png'.format(i))
        plt.close()
    
    ''' visialization '''
    # animation
    with imageio.get_writer('animation/particle_filter_with {} obstacle and {} particles.gif'.format(N_obstacle, N_particle), mode='I', duration=0.5) as writer:
        for i in range(1, len(filenames)):
            image = imageio.imread(filenames[i])
            writer.append_data(image)
    # 刪除40張折線圖
    for filename in set(filenames):
        os.remove(filename)
        
    
    # # final iteration
    # fig = plt.figure( dpi = 200 )
    # ax = fig.add_subplot(1, 1, 1)
    # draw_environment(ax, env, wall_len)
    
    # p_x_head = []
    # p_y_head = []
    # for i in range(len(p_x)):
    #     p_x_head.append(p_x[i]+0.05*np.cos(p_ori[i]))
    #     p_y_head.append(p_y[i]+0.05*np.sin(p_ori[i]))
    
    # # draw particles
    # ax.scatter(p_x_head[0 : int(-N_particle*0.1)], p_y_head[0 : int(-N_particle*0.1)], color='black', linewidths=0.1)
    
    # # draw robot
    # ax.scatter(robot[0], robot[1], color='green', linewidths=10)  
    # ax.scatter(p_x[0 : int(-N_particle*0.1)], p_y[0 : int(-N_particle*0.1)], color='yellow', linewidths=5)
    # ax.scatter(robot[0]+0.05*np.cos(robot[2]), robot[1]+0.05*np.sin(robot[2]), color='black', linewidths=0.1)
    
    


        