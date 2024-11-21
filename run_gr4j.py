import subprocess
import pandas as pd
import time

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
    subprocess.run(command, capture_output=True, text=True)
    # df = pd.read_csv('OutputsModel.csv')
    

if __name__ == "__main__":
    file_name = "BasinObs.csv"
    period_warmup_ini = "1999-01-01"
    period_warmup_end = "2001-12-31"
    period_run_ini = "2002-01-01"
    period_run_end = "2012-12-31"
    params = [257.24, 1.01, 88.23, 2.21]

    t0 = time.time() 

    df = run_gr4j(
        file_name,
        period_warmup_ini,
        period_warmup_end,
        period_run_ini,
        period_run_end,
        params
    )

    t1 = time.time()
    dt1 = t1-t0
    print(f"{dt1:.2f}")

    df = pd.read_csv("OutputsModel.csv")

    t2 = time.time()
    dt2 = t2 - t1
    print(f"{dt2:.2f}")

