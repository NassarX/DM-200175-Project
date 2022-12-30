import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zscore
import seaborn as sns
import os


def load_data(file_path):
    """Loads data from a file and returns a Pandas dataframe.

    :param: path: str The file path of the data files.

    :returns pandas.DataFrame The data as a Pandas dataframe.
    """
    # load train data sets
    df = pd.read_sas(file_path)

    return df


def detect_outliers(data, metrics, method='iqr'):
    """ Detects outliers of data using the IQR,  Z-score or empirical rule method.

    :param:
    data: pandas.DataFrame - The data to be analyzed.
    method: string, optional - emp, z_score, iqr

    :returns
    pandas.DataFrame
    """

    outliers_summary = {}
    outliers = pd.DataFrame()
    if method == 'iqr':
        """Identify the  outliers by IQR rule."""

        q25 = data.quantile(.25)
        q75 = data.quantile(.75)
        iqr = (q75 - q25)
        upper_lim = q75 + 1.5 * iqr
        lower_lim = q25 - 1.5 * iqr

        for metric in metrics:
            llim = lower_lim[metric]
            ulim = upper_lim[metric]
            outlier_rows = data[(data[metric] < llim) | (data[metric] > ulim)]
            if len(outlier_rows) > 0:
                outliers = outliers.append(outlier_rows)
                outliers_summary[metric] = {'lower': round(llim, 2), 'upper': round(ulim, 2),
                                            'count': len(outlier_rows)}

        return [outliers_summary, outliers.drop_duplicates().sort_index()]
    elif method == 'z_score':
        for metric in metrics:

            # Calculate the mean and standard deviation
            data_mean, data_std = np.mean(data[metric]), np.std(data[metric])

            # Calculate the z-scores for each value
            z_scores = zscore(data[metric])

            # Set the threshold for identifying outliers
            threshold = 3

            outlier_rows = data[(abs(z_scores) > threshold)]
            if len(outlier_rows) > 0:
                outliers = outliers.append(outlier_rows)
                outliers_summary[metric] = {'threshold': threshold, 'count': len(outlier_rows)}
        return [outliers_summary, outliers.drop_duplicates().sort_index()]


def get_education_rank(degree):
    """ Define function for ranking education degree

    :param:
    Education Degree
    :return: string
    """

    if degree == b'1 - Basic':
        return 1
    elif degree == b'2 - High School':
        return 2
    elif degree == b'3 - BSc/MSc':
        return 3
    elif degree == b'4 - PhD':
        return 4
    else:
        return degree


def heatmap_corr(cor, figures_path, title):

    p_corr = round(cor.iloc[1:, :-1].copy(), 2)

    # Setting up a diverging palette
#    plt.subplots(figsize=(12, 6))

    # Prepare figure
    fig = plt.figure(figsize=(10, 8))

    # Build annotation matrix (values above |0.5| will appear annotated in the plot)
    mask_annot = np.absolute(p_corr.values) >= 0.5
    annot = np.where(mask_annot, p_corr.values,
                     np.full(p_corr.shape, ""))  # Try to understand what this np.where() does

    # Plot heatmap of the correlation matrix
    sns.heatmap(data=p_corr, annot=annot, cmap=sns.diverging_palette(220, 10, as_cmap=True),
                fmt='s', vmin=-1, vmax=1, center=0, square=True, linewidths=.5)

    # Layout
    fig.subplots_adjust(top=0.95)

    plt.title(title)
    plt.savefig(os.path.join(figures_path, title.replace(" ", "_") + '_heatmap.png'),
                dpi=200)
    plt.show()


class Helper:
    def __init__(self):
        pass