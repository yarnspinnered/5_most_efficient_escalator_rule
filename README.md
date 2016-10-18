# This script simulates people riding the escalator according to two different scenarios. In one, the left lane is reserved for walkers and the right lane is 
reserved for people who stand still. The alternative scenario is that people just stay at whatever lane they arrive at, regardless of whether they walk or
stand still, potentially blocking people behind them. We assume 80% of people walk and walkers complete their journey in half the time a "stander" takes and 
then we model the number of people who finish an escalator ride under the two rules. We find there is little difference when the escalator is relatively empty
but the free-for-all rule quickly becomes more efficient as the escalator becomes busier. Interestingly, the disparity grows as the probability of a walker
diverges from 0.5. Intuitively, it's probably because half the escalator is being reserved for less than half of the riders which is clearly inefficient.
