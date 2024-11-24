import subprocess
import pandas as pd
import io
import hydrovis
import hydrocrit

def run_gr4j(
    file_name, 
    period_warmup_ini,
    period_warmup_end,
    period_run_ini,
    period_run_end,params
    ):
    command = [
        'Rscript', 'run_gr4j_from_py.R',
        file_name,
        period_warmup_ini,
        period_warmup_end,
        period_run_ini,
        period_run_end,
        *map(str, params)
    ]

    ## AQUIII
    result = subprocess.run(command, capture_output=True, text=True)
    df = pd.read_csv(io.StringIO(result.stdout))
    return df
    # df = pd.read_csv('OutputsModel.csv')
    

if __name__ == "__main__":
    file_name = "BasinObs.csv"
    period_warmup_ini = "1999-01-01"
    period_warmup_end = "2001-12-31"
    period_run_ini = "2002-01-01"
    period_run_end = "2012-12-31"
    params = [257.24, 1.01, 88.23, 2.21]
    
    df_sim = run_gr4j(
        file_name,
        period_warmup_ini,
        period_warmup_end,
        period_run_ini,
        period_run_end,
        params
    )    
    df_sim["DatesR"] = pd.to_datetime(df_sim["DatesR"])
    df_sim.set_index("DatesR", inplace=True, drop=True)

    df_obs = pd.read_csv("BasinObs.csv", parse_dates=True, index_col="DatesR")
    df_obs = df_obs.loc[period_run_ini : period_run_end]

    nse_value = hydrocrit.nse(df_obs["Qmm"], df_sim["Qsim"])
    kge_value = hydrocrit.kge(df_obs["Qmm"], df_sim["Qsim"])
    # # print("Plotando...")
    # fig = hydrovis(df_sim.index, df_sim["Precip"], df_sim["PotEvap"], df_obs["Qmm"], df_sim["Qsim"])
