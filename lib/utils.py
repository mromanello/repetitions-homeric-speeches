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

def passim_output_to_dataframe(output_path, dataframe_path, columns_to_keep=['cluster', 'id', 'label', 'dices_tags', 'text', 'raw_text', 'speaker', 'addressee']) -> pd.DataFrame:
    tr_clusters = pd.DataFrame(read_jsonl(output_path))
    print(f'There are {tr_clusters.cluster.unique().size} text reuse clusters in {output_path}')
    output_df = tr_clusters[columns_to_keep]
    output_df.to_csv(dataframe_path)
    return output_df

def speeches_to_passim(
      speeches_df : pd.DataFrame, json_path : str, lemmatised : bool = False, filtered : bool = False
      ) -> None:
    """
    Transform a DataFrame containing DICES speeches into a JSON file amenable to passim.
    """
    docs = []
    for idx, row in speeches_df.iterrows():
      doc = {
            "id" : idx,
            "group": row.group,
            "label": row.label,
            "dices_speech_id": row.speech_id,
            "dices_tags": row.dices_tags,
            "speaker": row.speaker,
            "addressee": row.addressee,
            "text": None,
            "raw_text": row.text if lemmatised else None,
            "passage_urn": row.passage_urn
        }
      if lemmatised:
         if filtered:
            doc['text'] = row.lemmatised_filtered_text
         else:
            doc['text'] = row.lemmatised_text
      else:
       doc['text'] = row.text
       
      docs.append(doc)


    # write passim docs to JSON file
    with open(json_path, 'w', encoding='utf-8') as f:
        for d in docs:
            print(json.dumps(d, ensure_ascii=False), file=f)