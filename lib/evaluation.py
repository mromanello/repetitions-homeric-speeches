import pandas as pd
from typing import List, Optional
from .utils import read_jsonl

class Locus(object):

    def __init__(self, reference_string) -> None:
        self._raw_string = reference_string
        raw_scope, self. author, self.work = self._parse(reference_string)
        self.begin, self.end = self._parse_scope(raw_scope)

    def _parse_scope(self, scope_string) -> List[int]:
        try:
            begin_scope, end_scope = scope_string.split('-')
        except ValueError as e:
            begin_scope = end_scope = scope_string
        
        begin_levels = [int(level) for level in begin_scope.split('.')]
        end_levels = [int(level) for level in end_scope.split('.')]
        
        if len(end_levels) < len(begin_levels):
            end_levels.insert(0, begin_levels[0])

        return begin_levels, end_levels

    def _parse(self, reference_string):
        if "Il." in reference_string or "Iliad" in reference_string:
            clean_string = reference_string.replace("Hom. Il.", "").replace("Homer, Iliad", "").strip()
            return clean_string, "Homer", "Iliad"
        elif "Od." in reference_string or "Odyssey" in reference_string:
            clean_string = reference_string.replace("Hom. Od.", "").replace("Homer, Odyssey", "").strip()
            return clean_string, "Homer", "Odyssey"
        
    def contains(self, other_locus):
        if self.begin[0] == other_locus.begin[0]:
            if self.begin[1] <= other_locus.begin[1]:
                if self.end[1] >= other_locus.end[1]:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
        
    def __repr__(self) -> str:
        begin_scope_string = ".".join([str(l) for l in self.begin])
        end_scope_string = ".".join([str(l) for l in self.end])
        return repr(f"<Locus: {self.author}, {self.work} {begin_scope_string}-{end_scope_string}>")

class TextReuseCluster(object):

    def __init__(self, cluster_id, passages):
        self._id = cluster_id
        self._passages = passages
        self._matched_predictions = []

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
    def matched_predictions(self):
        # TODO return a list sorted by some criterion
        return self._matched_predictions
    
    @matched_predictions.setter
    def matched_predictions(self, match):
        self._matched_predictions.append(match)
    
    @property
    def loci(self):
        return [p.locus for p in self._passages]
    
    @property
    def dices_speech_ids(self) -> List:
        return [p.dices_speech_id for p in self._passages]

    @property
    def labels(self):
        return [p._label for p in self._passages]

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
        self._label = label
        self.locus = Locus(label)
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

    def _match_predictions(self) -> None:
        """
        Iterate through GT clusters and find predicted
        clusters that match, based on loci (done) + textual overlap (tbd)
        """
        for gt_cluster in self.gt_clusters.values():
            for pred_cluster in self.predicted_clusters.values():
                
                gt_works = set([l.work for l in gt_cluster.loci])
                pred_works =  set([l.work for l in pred_cluster.loci])
                if gt_works != pred_works:
                    continue

                match = compare_tr_clusters(gt_cluster, pred_cluster)
                if match:
                    gt_cluster.matched_predictions = match

    def evaluate(self) -> None:
        """
        Evaluate the predicted clusters and print an evaluation summary.
        """

        self._match_predictions()

        n_matched = sum([
            len(cluster.matched_predictions) > 0
            for cluster in self.gt_clusters.values()    
        ])

        n_unmatched = len(self.gt_clusters.values()) - n_matched

        n_exact = len([
            m
            for m in self.matches
            if m.is_exact()
        ])

        n_partial = len([
            m
            for m in self.matches
            if m.is_partial()
        ])

        n_spurious = len([
            m
            for m in self.matches
            if m.is_spurious()
        ])

        print(f'# of ground-truth cluster: {len(self.gt_clusters.values())}')
        print(f'# of matched clusters: {n_matched}')
        print(f'# of unmatched clusters: {n_unmatched}')
        print('\n')
        print(f'# of partially matched clusters: {n_partial}')
        print(f'# of exactly matched clusters: {n_exact}')
        print(f'# of clusters with spurious passages: {n_spurious}')
        return
    
    @property
    def matches(self) -> None:
        return [
            c.matched_predictions[0]
            for c in self.gt_clusters.values()
            if c.matched_predictions
        ]

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
            print(f'{len(self._pred_clusters)} predicted clusters found')
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
            print(f'{len(self._gt_clusters)} groundtruth clusters found')
        except Exception as e:
            raise e
            #print(e)
            #print(f'Unable to read groundtruth from {path}.')

class ClusterMatch(object):
    
    def __init__(self, gt_cluster, pred_cluster, loci_overlap) -> None:
        self.gt_cluster = gt_cluster
        self.pred_cluster = pred_cluster
        self._loci_overlap = loci_overlap
        self._n_spurious_passages = pred_cluster.size - gt_cluster.size if pred_cluster.size > gt_cluster.size else 0
        self._n_missing_passages = gt_cluster.size - pred_cluster.size if  gt_cluster.size > pred_cluster.size else 0

    @property
    def type(self) -> str:
        if self.is_exact():
            match_type = 'exact'
        elif self.is_partial():
            match_type = 'partial'
        elif self.is_spurious():
            match_type = 'spurious'
        else:
            match_type = None
        return f"{match_type}-match"
    
    def is_exact(self) -> bool:
        return self.gt_cluster.size == self.pred_cluster.size

    def is_partial(self) -> bool:
        return self.gt_cluster.size > self.pred_cluster.size
    
    def is_spurious(self) -> bool:
        return self.pred_cluster.size > self.gt_cluster.size
    
    def inspect(self) -> None:
        print(f'Match type: {self.type}')
        print(f'GT cluster {self.gt_cluster.id}')
        for p in self.gt_cluster.passages:
            print(f"\t({p.locus}) {p.text}")
        print('\n')
        print(f'Predicted cluster {self.pred_cluster.id}')
        for p in self.pred_cluster.passages:
            print(f"\t({p.locus}) {p.text}")
        print('\n#####\n')
        

    @property
    def n_spurious_passages(self) -> int:
        return self._n_spurious_passages
    
    @property
    def n_missing_passages(self) -> int:
        return self._n_missing_passages

    def __repr__(self) -> str:
        return f"<Match: GT cluster[{self.gt_cluster.id}] with predicted cluster[{self.pred_cluster.id}] ({self.type})>"

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

def compute_loci_overlap(cluster_a, cluster_b):
    result = []
    for locus_a in cluster_a.loci:
        for locus_b in cluster_b.loci:
            match = locus_a.contains(locus_b)
            result.append(match)
            if match:
                # TODO: to logging instead
                #print(f"{locus_a} contains {locus_b}")
                pass
    return sum(result)

def compare_tr_clusters(gt_cluster, pred_cluster) -> Optional[ClusterMatch]:
    
    overlap = compute_loci_overlap(pred_cluster, gt_cluster)
    
    if overlap >= 2:
        return ClusterMatch(gt_cluster, pred_cluster, overlap)