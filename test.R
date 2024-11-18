library(airGR)
library(readr)

file_name = "BasinObs.csv"
period_run_ini = "1990-01-01"
period_run_end = "1999-12-31"
x1 = 257.24
x2 = 1.01
x3 = 88.23
x4 = 2.21

BasinObs <- read_csv(file_name, show_col_types=FALSE)
BasinObs$DatesR <- as.POSIXlt(BasinObs$DatesR, format = "%Y-%m-%d")

InputsModel <- CreateInputsModel(FUN_MOD = RunModel_GR4J,
  DatesR = BasinObs$DatesR,
  Precip = BasinObs$P,
  PotEvap = BasinObs$E
  )

Ind_Run <- seq(which(format(BasinObs$DatesR, format = "%Y-%m-%d") == period_run_ini),
               which(format(BasinObs$DatesR, format = "%Y-%m-%d") == period_run_end)
               )

RunOptions <- CreateRunOptions(FUN_MOD = RunModel_GR4J,
                               InputsModel = InputsModel,
                               IndPeriod_Run = Ind_Run,
                               IniStates = NULL,
                               IniResLevels = NULL, IndPeriod_WarmUp = NULL
                               )

Param <- c(x1, x2, x3, x4)

OutputsModel <- RunModel_GR4J(InputsModel = InputsModel, RunOptions = RunOptions, Param = Param)
plot(OutputsModel, Qobs = BasinObs$Qmm[Ind_Run])