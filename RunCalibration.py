import HW7P4 as Cls
import CalibrationSettings as CalibSets
import scr.FigureSupport as Fig

# create a calibration object
calibration = Cls.Calibration()

# sample the posterior of the mortality probability
calibration.sample_posterior()


# Estimate of mortality probability and the posterior interval
print('Estimate of mortality probability ({:.{prec}%} credible interval):'.format(1-CalibSets.ALPHA, prec=0),
      calibration.get_mortality_estimate_credible_interval(CalibSets.ALPHA, 4))

# '('Estimate of mortality probability (95% credible interval):', '0.0696 (0.0580, 0.0815)'))'
