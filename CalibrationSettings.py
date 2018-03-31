import scipy.stats as stat


SIM_POP_SIZE = 1000       # population size of simulated cohorts
TIME_STEPS = 5        # length of simulation
ALPHA = 0.05             # significance level for calculating confidence intervals
NUM_SIM_COHORTS = 500   # number of simulated cohorts used to calculate prediction intervals

# details of a clinical study estimating the mean survival time
OBS_N = 573        # number of patients involved in the study
OBS_Live = 400   # number of survived patients

# how to sample the posterior distribution of mortality probability
# minimum, maximum and the number of samples for the mortality probablity
POST_L, POST_U, POST_N = 0, 1, 1000

