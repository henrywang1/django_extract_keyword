from collections import Counter
from collections import defaultdict
import pytrends
import pytrends
from pytrends.request import TrendReq
pytrends = TrendReq(hl='zh-tw', tz=360)
import pickle
import gensim
from sklearn import cluster
import math
import pandas as pd

tmp_path = './extract/'
with open (tmp_path + 'cluster_dict.pickle', 'rb') as f:
     cluster_dict = pickle.load(f)

model = gensim.models.Word2Vec.load(tmp_path + 'skip-gram-mc1') 
dict_relate = {}

def get_cluster(input_list):
    NUM_CLUSTERS = math.ceil(len(input_list)/5)
    input_list_new = [i for i in input_list if i in cluster_dict]
    kmeans = cluster.KMeans(n_clusters=NUM_CLUSTERS)
    X = model[input_list_new]
    kmeans.fit(X)
    labels = kmeans.labels_

    final_list = [[] for i in range(NUM_CLUSTERS)]
    for idx, item in enumerate(input_list_new):
        gp = labels[idx]
        final_list[gp].append(item)

    input_list_old = [i for i in input_list if i not in input_list_new]
    final_list.append(input_list_old)
    
    return final_list

def get_topk_related(keyword, k=3):

    if keyword in dict_relate:
        return dict_relate[keyword]
    pytrends.build_payload([keyword], cat=0, timeframe='today 1-m', geo='', gprop='')
    ret = list(pytrends.related_topics().values())[0]
    ret = set(ret.title[0:k].values) if ret is not None else None
    dict_relate[keyword] = ret
    return ret

def extend_result(item_list): 
    if len(item_list) >=5:
        return item_list

    all_relate = [get_topk_related(item) for item in item_list]
    all_relate = [item for sublist in all_relate if sublist for item in sublist]
    all_relate = Counter(all_relate).most_common()
    all_relate = [item[0] for item in all_relate if item[0] not in item_list]
    length = (len(item_list)+1)*2
    return (item_list+all_relate)[:length]

def get_trend_result(result):
    result_list = []
    for r in result:
        if len(r)<2:
            continue
        length = len(r)
        if length <= 5:   
            
            pytrends.build_payload(r, cat=0, timeframe='today 1-m')
            interest_over_time_df = pytrends.interest_over_time()
            interest_over_time_df = interest_over_time_df.mean()[:-1]
            interest_over_time_df = interest_over_time_df.map(lambda x: '%d' % round(x))
            interest_over_time_df = interest_over_time_df.to_dict()
            result_list.append(interest_over_time_df)
        else:
            l_r = r[0:length//2][:5]
            r_r = r[length//2-1:][:5]
            pytrends.build_payload(l_r, cat=0, timeframe='today 1-m')
            df_1 = pytrends.interest_over_time()
            df_1 = df_1.mean()[:-1]            
            pytrends.build_payload(r_r, cat=0, timeframe='today 1-m')
            df_2 = pytrends.interest_over_time()
            df_2 = df_2.mean()[:-1]
            
            if(df_1[-1] > 0 and df_2[0] >0):
                r1 = df_1/df_1[-1]
                r2 = df_2/df_2[0]
            else:
                r1=df_1
                r2=df_2
            interest_over_time_df = pd.concat([r1, r2])
            interest_over_time_df = interest_over_time_df.map(lambda x: '%d' % round(x))
            interest_over_time_df = interest_over_time_df.to_dict()
            result_list.append(interest_over_time_df)

    return result_list

def word_related(tags):
    tag_cluster = get_cluster(tags)
    cluster_result = [extend_result(r) for r in tag_cluster]
    result_list = get_trend_result(cluster_result)
    return result_list