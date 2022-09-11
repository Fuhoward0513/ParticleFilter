# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 15:17:54 2022

@author: asus
"""

from src.particle_filter import particle_filter

''' Compare performance according to the number of particles '''

''' 20 obstacle and 100 particles '''
print('particle filter with 20 obstacle and 10 particles: ')
particle_filter(N_obstacle=20, N_particle=100, iteration=50)
print('finished')

''' 20 obstacle and 500 particles '''
print('particle filter with 20 obstacle and 100 particles: ')
particle_filter(N_obstacle=20, N_particle=500, iteration=50)
print('finished')

# ''' 20 obstacle and 1000 particles '''
print('particle filter with 20 obstacle and 1000 particles: ')
particle_filter(N_obstacle=20, N_particle=1000, iteration=50)
print('finished')


# ''' Compare performance according to the number of obstacles '''

''' 10 obstacle and 100 particles '''
print('particle filter with 10 obstacle and 500 particles: ')
particle_filter(N_obstacle=10, N_particle=500, iteration=50)
print('finished')

''' 20 obstacle and 100 particles '''
print('particle filter with 20 obstacle and 500 particles: ')
particle_filter(N_obstacle=20, N_particle=500, iteration=50)
print('finished')

''' 40 obstacle and 100 particles '''
print('particle filter with 40 obstacle and 500 particles: ')
particle_filter(N_obstacle=40, N_particle=500, iteration=50)
print('finished')



