library(airGR)
library(readr)

args <- commandArgs(trailingOnly = TRUE)
FileName <- args[1]
Period_WarmUp_Ini <- args[2]
Period_WarmUp_End <- args[3]
Period_Run_Ini <- args[4]
Period_Run_End <- args[5]
x1 <- as.numeric(args[6])
x2 <- as.numeric(args[7])
x3 <- as.numeric(args[8])
x4 <- as.numeric(args[9])
Param <- c(x1, x2, x3, x4)

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
  Param = Param
  )

write.csv(OutputsModel[1:19], "OutputsModel.csv", row.names=FALSE, quote=FALSE)