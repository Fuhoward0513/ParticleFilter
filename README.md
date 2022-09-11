# Particle Filter Algorithm
## :mag_right: Project Description
### Implement a simple robot navigation domain and to evaluate the performance of the particle filter algorithm.
#### The green dot: the real position of the robot

#### The yellow dots: the particles' position


![](https://i.imgur.com/69b1hJE.gif)


## :earth_africa: Program Flow

![](https://i.imgur.com/tSlPKUd.png)



## :orange_book: Define Weight function

### Total weight = 100*distance weight + relative angle weight + relative orientation weight

        distance weight =1/(∑abs((robot distance to wall)-(particle distance to wall)) )


        relative angle weight=  1/(∑〖abs((robot angle to wall)-(particle angle to wall))〗)

        relative orientation weight=  1/(∑〖abs((robot orientation to wall)-(particle orientation to wall))〗)


However, although the particle can converge, I think the performance was not good enough. So, I add a penalty rules to the total weight as shown below:

	If the # walls robot detected > # walls particle detected:
    Total weight after penalty = total weight – (#walls robot detected-# walls particle detected)*100
    
	If the # walls robot detected < # walls particle detected:
    Total weight after penalty = total weight + (#walls robot detected-# walls particle detected)*100

	If the # walls robot detected = # walls particle detected:
    Total weight after penalty = total weight

In my algorithm design, I consider the distance and the # walls being detected dominates the weight function, and in the end the performance improved.


## :star: Result
### Performance of the particle filter algorithm in the environment for 10, 20, and 40 obstacles:

To show the performance of the particle filter for various number of obstacles, I apply 500 particles to the environment for 10, 20, and 40 obstacles.

1. 10 obstacles:
In the iterations, particle filter can correctly locate the position of the robot. However, in the beginning of the implementation, it is particularly hard for the particles to converge to the correct position of the robot, because the number of obstacle is too small that most of the time the sensor can’t sense any obstacle in every iteration. Because of the lacking of sensing information, the particle filter can’t work well in the environment with few obstacles.

![](https://i.imgur.com/p7jLMej.gif)

2. 20 obstacles:
In the iterations, particle filter can correctly locate the position of the robot. Moreover, it is easier for the particle filter to converge in the environment of 20 obstacles than in the environment with only 10 obstacles. I think it is because with more obstacles, the probability of sensing for particles and robot is higher.

![](https://i.imgur.com/9KBK71k.gif)

3. 40 obstacles:
Before implementing, I think that the performance in the environment of 40 obstacles will be as well as the condition of 20 obstacles. However, I figure that it is actually harder for particles to converge. Although the particles eventually can converge to the position of the robot, its speed of convergence is lower. I think the reason is that the obstacles locate densely. As the result, it is more possible to sense the assignment of the obstacles which seems similar to the robot sensing.

![](https://i.imgur.com/GiFXTiV.gif)


### Performance of particle filter algorithm using 100, 500, and 1000 particles

To clearly show the performance of the particle filter based on different number of particles. I will apply the algorithm to the environment of 20 obstacle with 100, 500, and 1000 particles.

1. 100 particles:
The speed of the converge will be slow, because the range of searching for the particles is smaller. Moreover, the particles are usually close to each others because the sample of the particles are small, so when resampling, the result will be dominate by some of the particles.

![](https://i.imgur.com/Sn6Haas.gif)


2. 500 particles:
With 100 particles, the range of searching becomes bigger, so the speed of convergence gets faster.

![](https://i.imgur.com/8CCtDy8.gif)


3. 1000 particles
The speed of convergence with 1000 particles is as well as the speed with 100 particles. However, the searching range of the particles will be too large for this environment, so sometimes the precision of the localization will be reduced as well, and the memory usage is bigger.

![](https://i.imgur.com/8NZhGey.gif)
