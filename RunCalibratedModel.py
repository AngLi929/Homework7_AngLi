import HW7P5 as Cls
import CalibrationSettings as P
import scr.FigureSupport as Fig


# initialize a calibrated model
calibrated_model = Cls.CalibratedModel('CalibrationResultsHW7.csv')
# simulate the calibrated model
calibrated_model.simulate(P.NUM_SIM_COHORTS, P.SIM_POP_SIZE, P.TIME_STEPS)

# report mean and projection interval
print('Mean survival time and {:.{prec}%} projection interval:'.format(1 - P.ALPHA, prec=0),
      calibrated_model.get_mean_survival_time_proj_interval(P.ALPHA, deci=4))

#After changing the time steps from 5 to 1000
# ('Mean survival time and 95% projection interval:', '14.2478 (12.4250, 17.8120)')




