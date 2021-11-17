from RunningGram import RunningGram
from RunningGram import RunningGramWait
import time 
import matplotlib.pyplot as plt
import numpy as np

#tests waiting .5 seconds for startup (and some amount of time for closing too) or watching for gram to finish in task manager based on memory

#Arrays for storing time values over the 100 trials
start_time = np.array([],dtype = float)
start_time_wait = np.array([],dtype = float)

i = 1
x = np.linspace(1, 100, num = 100)
while i <= 100:

    #Running RunningGram and recording the time it takes to full end
    timeCMD = time.time()
    RunningGram()
    start_time = np.append(start_time, [time.time() - timeCMD])

    #Running RunningGramWait and recording the time it takes to full end
    time_wait = time.time()
    RunningGramWait()
    start_time_wait = np.append(start_time_wait, [time.time() - time_wait])

    i = i + 1


#Graphing the results
plt.plot(x, start_time, label = 'Task Manager')
plt.title('Testing Runtime of Monitering Memory vs Waiting')
plt.plot(x, start_time_wait, label = 'Literally Just Waiting')
plt.ylabel('Runtime (s)')
plt.xlabel('Trial (#)')
plt.ylim([0, 1.2])
plt.legend()
plt.show()
