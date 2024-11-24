import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

def hyeto_hydrograph(Dates, Precip, PotEvap, Qobs, Qsim):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [1, 2]})


    # Gráfico de Precipitação e PotEvap
    ax1.bar(Dates, Precip, color="blue", label="Precip")
    ax1.invert_yaxis()
    ax1.plot(Dates, PotEvap, color="red", label="PotEvap")
    ax1.set_ylabel("Inputs (mm)")
    ax1.set_xticklabels([])
    ax1.legend(loc="lower right")

    ax2.plot(Dates, Qobs, label="Qobs", color="black", linewidth=1)
    ax2.plot(Dates, Qsim, label="Qsim", color="red", linewidth=1)
    ax2.set_ylabel("Outputs (mm)")
    ax2.set_xlabel("Date")
    ax2.legend()

    plt.tight_layout()
    
    with PdfPages("OutputsModel.pdf") as pdf:
        pdf.savefig(fig)

    return fig
