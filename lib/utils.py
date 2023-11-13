from typing import List, Dict
import glob, itertools, json
import pandas as pd

def read_jsonl_file(f) -> List[Dict]:
  """Read one JSON record per line."""
  res = []
  for line in f:
    res.append(json.loads(line))
  return res

def read_jsonl(d) -> List:
  """Read a directory of JSON line files."""
  return list(itertools.chain.from_iterable([read_jsonl_file(open(f)) for f in glob.glob(d + '/*.json')]))

def passim_output_to_dataframe(output_path, dataframe_path, columns_to_keep=['cluster', 'id', 'label', 'dices_tags', 'text', 'raw_text']) -> pd.DataFrame:
    tr_clusters = pd.DataFrame(read_jsonl(output_path))
    print(f'There are {tr_clusters.cluster.unique().size} text reuse clusters in {output_path}')
    output_df = tr_clusters[columns_to_keep]
    output_df.to_csv(dataframe_path)
    return output_df