from enum import Enum
import numpy as np
import scr.SamplePathClasses as PathCls
import scr.StatisticalClasses as Stat


class HealthStat(Enum):
    """ health status of patients  """
    ALIVE = 1
    DEAD = 0


class Patient:
    def __init__(self, id, mortality_prob):
        """ initiates a patient
        :param id: ID of the patient
        :param mortality_prob: probability of death during a time-step (must be in [0,1])
        """
        self._id = id
        self._rnd = np.random       # random number generator for this patient
        self._rnd.seed(self._id)    # specifying the seed of random number generator for this patient

        self._mortalityProb = mortality_prob
        self._healthState = HealthStat.ALIVE  # assuming all patients are alive at the beginning
        self._survivalTime = 0

    def simulate(self, n_time_steps):
        """ simulate the patient over the specified simulation length """

        t = 0  # simulation current time

        # while the patient is alive and simulation length is not yet reached
        while self._healthState == HealthStat.ALIVE and t < n_time_steps:
            # determine if the patient will die during this time-step
            if self._rnd.sample() < self._mortalityProb:
                self._healthState = HealthStat.DEAD
                self._survivalTime = t + 1  # assuming deaths occurs at the end of this period

            # increment time
            t += 1

    def get_survival_status(self):

        if self._healthState == HealthStat.DEAD:
            return 0
        else:
            return 1


class Cohort:
    def __init__(self, id, pop_size, mortality_prob):
        """ create a cohort of patients
        :param id: cohort ID
        :param pop_size: population size of this cohort
        :param mortality_prob: probability of death for each patient in this cohort over a time-step (must be in [0,1])
        """
        self._patients = []      # list of patients
        self._survivalstatus = []
        # populate the cohort
        for i in range(pop_size):
            # create a new patient (use id * pop_size + n as patient id)
            patient = Patient(id * pop_size + i, mortality_prob)
            # add the patient to the cohort
            self._patients.append(patient)

    def simulate(self, n_time_steps):
        """ simulate the cohort of patients over the specified number of time-steps
        :param n_time_steps: number of time steps to simulate the cohort
        :returns simulation outputs from simulating this cohort
        """

        # simulate all patients
        for patient in self._patients:
            # simulate
            patient.simulate(n_time_steps)
            value = patient.get_survival_status()
            self._survivalstatus.append(value)

    def get_survival_statuses(self):
        return self._survivalstatus

    def get_survival_number(self):
        return sum(self._survivalstatus)

    def get_survival_rate(self):
        return sum(self._survivalstatus)/float(len(self._survivalstatus))


class MultiCohort:
    """ simulates multiple cohorts with different parameters """

    def __init__(self, ids, pop_sizes, mortality_probs):
        """
        :param ids: a list of ids for cohorts to simulate
        :param pop_sizes: a list of population sizes of cohorts to simulate
        :param mortality_probs: a list of the mortality probabilities
        """
        self._ids = ids
        self._popSizes = pop_sizes
        self._mortality_Probs = mortality_probs
        self._multiple_survival_rate= []

    def simulate(self, n_time_steps):
        """ simulates all cohorts """

        for i in range(len(self._ids)):
            # create a cohort
            cohort = Cohort(self._ids[i], self._popSizes[i], self._mortality_Probs[i])
            # simulate the cohort
            cohort.simulate(n_time_steps)
            self._multiple_survival_rate.append(cohort.get_survival_rate())

    def get_cohort_survival_rate(self, cohort_index):
        return self._multiple_survival_rate[cohort_index]

    def get_all_survival_rate(self):
        return self._multiple_survival_rate
