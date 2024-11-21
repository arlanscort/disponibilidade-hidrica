library(airGR)
library(readr)

FileName <- "BasinObs.csv"
Period_WarmUp_Ini <- "1989-01-01"
Period_WarmUp_End <- "1989-12-31"
Period_Run_Ini <- "1990-01-01"
Period_Run_End <- "1999-12-31"
Param = c(257.24, 1.01, 88.23, 2.21)

BasinObs <- read_csv(FileName)
BasinObs$DatesR <- as.POSIXlt(BasinObs$DatesR, format = "%Y-%m-%d")

InputsModel <- CreateInputsModel(
  FUN_MOD = RunModel_GR4J,
  DatesR = BasinObs$DatesR,
  Precip = BasinObs$P,
  PotEvap = BasinObs$E
  )

IndPeriod_WarmUp <- seq(
  which(format(BasinObs$DatesR, format = "%Y-%m-%d") == Period_WarmUp_Ini),
  which(format(BasinObs$DatesR, format = "%Y-%m-%d") == Period_WarmUp_End)
  )

Ind_Run <- seq(
  which(format(BasinObs$DatesR, format = "%Y-%m-%d") == Period_Run_Ini),
  which(format(BasinObs$DatesR, format = "%Y-%m-%d") == Period_Run_End)
  )

RunOptions <- CreateRunOptions(
  FUN_MOD = RunModel_GR4J,
  InputsModel = InputsModel,
  IndPeriod_WarmUp = IndPeriod_WarmUp,
  IndPeriod_Run = Ind_Run,
  IniStates = NULL,
  IniResLevels = NULL,
  )

OutputsModel <- RunModel_GR4J(
  InputsModel = InputsModel,
  RunOptions = RunOptions,
  Param = Param)

write.csv(OutputsModel[1:19], "OutputsModel.csv", row.names=FALSE, quote=FALSE)