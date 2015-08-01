import pandas as pd
from scipy import stats
import numpy as np

lucene = pd.read_csv("lucene_html.out", names=["topic","Q0","filename","ranking","score","label"], sep=" ")

#metrics = ['flesch_reading_ease', 'flesch_kincaid_grade_level', 'coleman_liau_index', 'gunning_fog_index', \
#        'smog_index', 'ari_index', 'lix_index', 'dale_chall_score', u'perc', u'loga']
metrics = ['flesch_kincaid_grade_level', 'coleman_liau_index', 'gunning_fog_index', 'smog_index', 'ari_index']

def remove_outliers(df, field, minv, maxv):
    return df.drop( df[ (df[field] < minv) | (df[field] > maxv) ].index)

def intify(df, field):
    df[field] = np.round(df[field]).astype(int)

def check_correlation(df, metrics=['flesch_reading_ease', 'flesch_kincaid_grade_level', 'coleman_liau_index', 'gunning_fog_index', 'smog_index', 'ari_index', 'lix_index', 'dale_chall_score', u'perc', u'loga']):

    for metric in metrics:
        metric1 = metric + "_cont"
        metric2 = metric + "_ncont"
        kendall = stats.kendalltau(df[metric1], df[metric2])
        spearman = stats.spearmanr(df[metric1], df[metric2])
        pearson = stats.pearsonr(df[metric1], df[metric2])
        yield metric, kendall, spearman, pearson


for t in ["bs4", "boilerpipe", "justext"]:

    print "File", t

    ncont = pd.read_csv("./readability_scores_" + t + "_ncont.csv")
    cont = pd.read_csv("./readability_scores_" + t + "_cont.csv")

    #ncont = pd.read_csv("./readability_scores_justext_cont.csv")
    #cont = pd.read_csv("./readability_scores_boilerpipe_cont.csv")

    #ncont = remove_outliers(ncont, "flesch_reading_ease", 0, 100)
    #ncont = remove_outliers(ncont, "loga", 0, 1.01)

    #cont = remove_outliers(cont, "flesch_reading_ease", 0, 100)
    #cont = remove_outliers(cont, "loga", 0, 1.01)

    cont["filename"] = cont["filename"].apply(lambda x: x[:-4])
    ncont["filename"] = ncont["filename"].apply(lambda x: x[:-4])

    """
    for metric in metrics:
        intify(cont, metric)
        intify(ncont, metric)
    """

    merged = pd.merge(cont, ncont, on="filename", suffixes=["_cont","_ncont"])

    acc = []
    acc2 = []
    for topic in lucene["topic"].unique():
        #top ranking only:
        tnow = lucene[(lucene["topic"] == topic) & (lucene["ranking"] <= 1000)]
        tdf = pd.merge(merged, tnow, on="filename")

        results = check_correlation(tdf)
        for r in results:
            metric, kendall, spearman, pearson = r
            acc.append([topic, metric, kendall[0], kendall[1], spearman[0], spearman[1], pearson[0], pearson[1]])

        for metric in metrics:
            acc2.append([topic, metric, sum(np.abs(tdf[metric + "_cont"] - tdf[metric + "_ncont"])) / tdf.shape[0],\
                                np.mean(tdf[metric + "_cont"]), np.mean(tdf[metric + "_ncont"])])

    results2014a =pd.DataFrame(acc2, columns=["topic","metric", "meanDiff", "meanCont", "meanNCont"])
    results2014b = pd.DataFrame(acc, columns=["topic","metric","kendall","ken-p","spearman","spea-p", "pearson", "pear-p"])
    results2014 = pd.merge(results2014a, results2014b, on=["topic", "metric"])
    print results2014.groupby("metric")["kendall","meanCont", "meanNCont"].mean()
    print results2014.groupby("metric")["kendall","meanCont", "meanNCont"].sem() * 1.96


    """
    for metric in ['flesch_reading_ease', 'flesch_kincaid_grade_level', 'coleman_liau_index', 'gunning_fog_index',\
            'smog_index', 'ari_index', 'lix_index', 'dale_chall_score', u'perc', u'loga']:
        print "Metric %s\tAbs diff %.2f\tMean Cont: %.2f\tMean nCont: %.2f" % (metric[0:10], sum(np.abs(merged[metric + "_cont"] - merged[ metric + "_ncont"])) / merged.shape[0], np.mean(merged[metric + "_cont"]), np.mean(merged[metric + "_ncont"]))
    print

for metric1 in ['flesch_reading_ease', 'flesch_kincaid_grade_level', 'coleman_liau_index', 'gunning_fog_index',\
            'smog_index', 'ari_index', 'lix_index', 'dale_chall_score', u'perc', u'loga']:
    metric1 = metric1 + "_cont"
    for metric2 in ['flesch_reading_ease', 'flesch_kincaid_grade_level', 'coleman_liau_index', 'gunning_fog_index',\
            'smog_index', 'ari_index', 'lix_index', 'dale_chall_score', u'perc', u'loga']:
        metric2 = metric2 + "_cont"
        if metric1 != metric2:
            print "%s and %s:\t%.2f\t%.2f\t%.2f" % (metric1[0:10], metric2[0:10], stats.kendalltau(merged[metric1], merged[metric2])[0], stats.spearmanr(merged[metric1], merged[metric2])[0], stats.pearsonr(merged[metric1], merged[metric2])[0])

    """

