#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 16:10:08 2024

@author: kiraparsons
"""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

number_of_raw_visits = [503456, 550980, 846103, 1214470, 1204136,
                        1027301, 952831, 931104, 963601, 1067130,
                        975370, 1015778, 948547, 901959, 1011169,
                        1081860, 1119933, 1065462, 1058982, 1182036,
                        1343097, 996243, 842200, 912163, 1057745,
                        946244, 743785, 375479, 551058, 625949,
                        616321, 703496, 649875, 643482, 557494,
                        513149, 506427, 459809, 587513, 687901,
                        657005, 624556, 652622, 661925, 689356,
                        695491, 665796, 556465, 489877, 536098,
                        621971, 665580, 604872, 542430, 553183,
                        451296, 443988, 468300, 453920, 512400]

number_of_crimes = [3761, 3123, 3488, 3788, 4211,
                     4074, 4315, 4544, 4214, 4577,
                     4182, 4322, 3733, 3142, 3478,
                     3684, 4154, 4198, 4547, 4485,
                     4240, 3924, 3558, 3461, 3369,
                     3098, 3094, 2543, 2917, 3139,
                     3178, 3065, 3122, 3188, 2856,
                     2715, 2553, 2174, 2669, 2644,
                     3269, 3388, 3351, 3385, 3548,
                     3546, 3323, 3529, 2989, 2602,
                     3055, 3100, 3414, 3660, 3797,
                     3699, 3719, 3719, 3456, 3429]

fig, ax = plt.subplots()
ax.set_xlabel('Number of Raw Visitors')
ax.set_ylabel('Number of Crimes')

line, = ax.plot([], [], lw=2)
ax.set_xlim(0, max(number_of_raw_visits) + 100000)
ax.set_ylim(0, max(number_of_crimes) + 500)

def init():
    line.set_data([], [])
    return line,

def animate(i):
    x = number_of_raw_visits[:i]
    y = number_of_crimes[:i]
    line.set_data(x, y)
    return line,

ani = FuncAnimation(fig, animate, frames=len(number_of_raw_visits), init_func=init, blit=True)

plt.show()