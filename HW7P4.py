from enum import Enum
import scipy.stats as stat
import numpy as np
import scr.InOutFunctions as InOutSupport
import scr.StatisticalClasses as StatSupport
import scr.FormatFunctions as FormatSupport
import SurvivalModelClasses as SurvivalCls
import CalibrationSettings as CalibSets
import HW7P1 as HW
from scipy.stats import binom


class CalibrationColIndex(Enum):
    """ indices of columns in the calibration results cvs file  """
    ID = 0          # cohort ID
    W = 1  # likelihood weight
    MORT_PROB = 2   # mortality probability


class Calibration:
    def __init__(self):
        """ initializes the calibration object"""
        np.random.seed(1)   # specifying the seed of the numpy random number generator
        self._cohortIDs = range(CalibSets.POST_N)   # IDs of cohorts to simulate
        self._mortalitySamples = []      # values of mortality probability at which the posterior should be sampled
        self._mortalityResamples = []    # resampled values for constructing posterior estimate and interval
        self._weights = []               # likelihood weights of sampled mortality probabilities
        self._normalizedWeights = []     # normalized likelihood weights (sums to 1)
        self._csvRows = \
            [['Cohort ID', 'Likelihood Weights' ,'Mortality Prob']]  # list containing the calibration results

    def sample_posterior(self):
        """ sample the posterior distribution of the mortality probability """

        # find values of mortality probability at which the posterior should be evaluated
        self._mortalitySamples = np.random.uniform(
            low=CalibSets.POST_L,
            high=CalibSets.POST_U,
            size=CalibSets.POST_N)

        # create a multi cohort
        multiCohort = HW.MultiCohort(
            ids=self._cohortIDs,
            mortality_probs=self._mortalitySamples,
            pop_sizes=[CalibSets.SIM_POP_SIZE]*CalibSets.POST_N
        )

        # simulate the multi cohort
        multiCohort.simulate(CalibSets.TIME_STEPS)

        # calculate the likelihood of each simulated cohort
        for cohort_id in self._cohortIDs:

            rate = multiCohort.get_cohort_survival_rate(cohort_id)

            weight = binom.pmf(CalibSets.OBS_Live, CalibSets.OBS_N, rate)
            # store the weight
            self._weights.append(weight)

        # normalize the likelihood weights
        sum_weights = np.sum(self._weights)
        self._normalizedWeights = np.divide(self._weights, sum_weights)

        # re-sample mortality probability (with replacement) according to likelihood weights
        self._mortalityResamples = np.random.choice(
            a=self._mortalitySamples,
            size=CalibSets.NUM_SIM_COHORTS,
            replace=True,
            p=self._normalizedWeights)

        # produce the list to report the results
        for i in range(0, len(self._mortalitySamples)):
            self._csvRows.append(
                [self._cohortIDs[i], self._normalizedWeights[i], self._mortalitySamples[i]])

        InOutSupport.write_csv('CalibrationResultsHW7.csv', self._csvRows)

    def get_mortality_resamples(self):
        """
        :return: mortality resamples
        """
        return self._mortalityResamples

    def get_mortality_estimate_credible_interval(self, alpha, deci):
        """
        :param alpha: the significance level
        :param deci: decimal places
        :returns text in the form of 'mean (lower, upper)' of the posterior distribution"""

        # calculate the credible interval
        sum_stat = StatSupport.SummaryStat('Posterior samples', self._mortalityResamples)

        estimate = sum_stat.get_mean()  # estimated mortality probability
        credible_interval = sum_stat.get_PI(alpha)  # credible interval

        return FormatSupport.format_estimate_interval(estimate, credible_interval, deci)
