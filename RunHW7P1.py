import HW7P1 as HW

Time_Steps = 5
Pop_Size = 573
Mortality_Prob=0.1
ID=1


MyCohort=HW.Cohort(ID,Pop_Size,Mortality_Prob)
MyCohort.simulate(Time_Steps)
print(sum(MyCohort.get_survival_statuses()))
print(len(MyCohort.get_survival_statuses()))
print(MyCohort.get_survival_statuses())
print("percentage of patients survived beyond 5 years is", MyCohort.get_survival_rate())


