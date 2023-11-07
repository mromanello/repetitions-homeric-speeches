import pandas as pd
from typing import List
from .utils import read_jsonl

class TextReuseCluster(object):

    def __init__(self, cluster_id, passages):
        self._id = cluster_id
        self._passages = passages

    @property
    def id(self):
        return self._id

    @property
    def size(self):
        return len(self._passages)

    @property
    def passages(self):
        return self._passages
    
    @property
    def dices_speech_ids(self) -> List:
        return [p.dices_speech_id for p in self._passages]
    

    @property
    def labels(self):
        return [p.label for p in self._passages]

    def __repr__(self) -> str:
        return repr(f"<TextReuseCluster id={self.id}, size={self.size}, passages='{'; '.join(self.labels)}'>")


class TextReusePassage(object):
    
    def __init__(self, cluster_id : str, label : str, text : str, dices_speech_id : int, raw_data = None):
        if raw_data:
            self._data = raw_data
        else:
            self._data = None
        
        self._cluster = None
        self._cluster_id = cluster_id
        self.dices_speech_id = dices_speech_id
        self.label = label
        self._text = text

    @property
    def cluster_id(self):
        return self._cluster_id

    @property
    def cluster(self):
        return self._cluster

    @property
    def text(self):
        return self._text

class TextReuseEvaluator(object):

    def __init__(self) -> None:
        self._gt_clusters = []
        self._pred_clusters = []

    @property
    def gt_clusters(self):
        """Get groundtruth clusters."""
        return self._gt_clusters
    
    @property
    def predicted_clusters(self):
        """Get predicted clusters."""
        return self._pred_clusters

    def read_predictions(self, path : str) -> None:
        try:
            pred_clusters = read_passim_output(path)
            self._pred_clusters = {
                c.id: c
                for c in pred_clusters
            }
        except Exception as e:
            print(e)
            print(f'Unable to read predictions from {path}.')

    def read_groundtruth(self, path : str) -> None:
        try:
            gt_clusters = read_groundtruth_dataset(path)
            self._gt_clusters = {
                c.id: c
                for c in gt_clusters
            }
        except Exception as e:
            print(e)
            print(f'Unable to read groundtruth from {path}.')

def read_passim_output(path : str) -> List[TextReusePassage]:
        passages = read_jsonl(path)

        obj_clusters = []
        
        # in passim's output each record is a text reuse passage
        # we need to group them by cluster ID before we create
        # TextReuseCluster objects
        cluster_idx = {}
        for passage in passages:
            cluster_id = passage.get('cluster')
            if cluster_id in cluster_idx:
                cluster_idx[cluster_id].append(passage)
            else:
                cluster_idx[cluster_id] = [passage]

        for cluster_id in cluster_idx:
            passages = cluster_idx[cluster_id]
            obj_passages = [
                TextReusePassage(p['cluster'], p['label'], p['text'], p['id'], p)
                for p in passages
            ]
            cluster = TextReuseCluster(cluster_id, obj_passages)
            obj_clusters.append(cluster)
        
        return obj_clusters

def read_groundtruth_dataset(path : str) -> List[TextReusePassage]:
    df = pd.read_csv(path, sep='\t')
    obj_clusters = []

    cluster_ids = df.cluster.unique()

    for id in cluster_ids:
        obj_passages = []
        passages = df[df.cluster == id]
        for _, passage in passages.iterrows():
            obj_passages.append(
                TextReusePassage(
                    cluster_id=passage.cluster,
                    label=passage.reference,
                    text=passage.text,
                    dices_speech_id=passage.dices_speech_id,
                    raw_data=passage.to_dict())
            )
        cluster = TextReuseCluster(cluster_id=id, passages=obj_passages)
        obj_clusters.append(cluster)

    return obj_clusters