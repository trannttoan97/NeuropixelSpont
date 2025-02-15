import numpy as np
import matplotlib.pyplot as plt

from scipy.io import loadmat
from dependencies import data_path


def plot_config():
    """
    Set default parameters for matplotlib
    """
    plt.style.use("seaborn-paper")
    plt.rcParams.update({
        "axes.labelsize": 16,
        "axes.titlesize": 17,
        "legend.title_fontsize": 16,
        "xtick.labelsize": 14,
        "ytick.labelsize": 14,
        "lines.linewidth": 1.8,
        "lines.markersize": 6,
        "axes.linewidth": 1
    })

def generate_colors():
    """
    Generate colors for mice, behavioral states and brain regions to be used across all plots

    Returns
    -------
    micecols : list
        List of colors assigned to mice for plotting
    regcols : list
        List of colors assigned to brain regions for plotting
    behcols : list
        List of colors assigned to behavioral states for plotting
    """
    kelly_colors = dict(vivid_yellow=(255, 179, 0),
                    strong_purple=(128, 62, 117),
                    vivid_orange=(255, 104, 0),
                    very_light_blue=(166, 189, 215),
                    vivid_red=(193, 0, 32),
                    grayish_yellow=(206, 162, 98),
                    medium_gray=(129, 112, 102),

                    # these aren't good for people with defective color vision:
                    vivid_green=(0, 125, 52),
                    strong_purplish_pink=(246, 118, 142),
                    strong_blue=(0, 83, 138),
                    strong_yellowish_pink=(255, 122, 92),
                    strong_violet=(83, 55, 122),
                    vivid_orange_yellow=(255, 142, 0),
                    strong_purplish_red=(179, 40, 81),
                    vivid_greenish_yellow=(244, 200, 0),
                    strong_reddish_brown=(127, 24, 13),
                    vivid_yellowish_green=(147, 170, 0),
                    deep_yellowish_brown=(89, 51, 21),
                    vivid_reddish_orange=(241, 58, 19),
                    dark_olive_green=(35, 44, 22))
    
    tab10_colors = [plt.cm.tab10(v) for v in np.linspace(0, 1, 10)]
    tab20b_colors = [plt.cm.tab20b(v) for v in np.linspace(0, 1, 20)]
    tab20c_colors = [plt.cm.tab20c(v) for v in np.linspace(0, 1, 20)]
    
    regcols = tab10_colors
    regcols[8] = tab20b_colors[5]
    regcols.insert(1, tab20b_colors[0])
    regcols.insert(2, tab20b_colors[16])
    
    keys = ["strong_blue", "vivid_yellow", "vivid_red"]
    _normalize = lambda r, g, b: (r/255, g/255, b/255, 1)
    _mix = lambda c1, c2: ((c1[0]+c2[0])/2, (c1[1]+c2[1])/2, (c1[2]+c2[2])/2, 1)
    behcols = [_normalize(*kelly_colors[k]) for k in keys]
    behcols.append(_mix(behcols[1], behcols[2]))

    micecols = [tab20c_colors[0], tab20c_colors[4], tab20c_colors[8]]
    
    return micecols, regcols, behcols

def load_data(names=["Krebs", "Waksman", "Robbins"]):
    """
    Load processed data into dictionaries for easy access

    Parameters
    ----------
    names : list
        List of mice names

    Returns
    -------
    ephys : list
        List of dictionaries, each containing the processed neural activity and neuron locations of a mouse
    behav : list
        List of dictionaries, each containing the behavioral variables extracted from the video recording of a mouse
    names : list
        List of names of mice
    """

    ephys = []
    behav = []

    for i in range(len(names)): 
        # neural data
        st = loadmat(f"{data_path}/ephys_{names[i]}.mat")
        st["reglbs"] = list(map(np.ndarray.item, st["reglbs"].flatten()))
        stkeys = ["regIDs", "probeIDs", "heights", "tpoints"]
        for k in stkeys:
            st[k] = st[k].flatten()
        ephys.append(st)

        # behavior variables
        beh = loadmat(f"{data_path}/behav_{names[i]}.mat")
        behkeys = ["frame_diff", "lomot_cont", "whisk_cont", "lomot_disc", "whisk_disc", "time_pts"]
        for k in behkeys:
            beh[k] = beh[k].flatten()
        behav.append(beh)

    return ephys, behav, names