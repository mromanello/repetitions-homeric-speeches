# Exploring repetitions in Homeric speeches

Authors: Ombretta Cesca (UNIL) and Matteo Romanello (UNIL)

This repository contains work-in-progress code & data concerning the automatic extraction of repetitions from Homeric speeches contained in the DICES database with passim (v. 1.0).

## Experiments


| Experiment ID     | Passim parameters | Explanation  | \# of extracted clusters | Evaluation |
| ----------- | ----------- |----------|------------|-------------------|
| `exp0`      | `-n 1 --min-match 1 -a 5` | reused passages consist of at least 1 shared n-grams of size 1 (uni-gram) | 6419 (lemmatised); 7993 (raw) | # of ground-truth cluster: 69, # of matched clusters: 22, # of unmatched clusters: 47, # of partially matched clusters: 2, # of exactly matched clusters: 2, # of clusters with spurious passages: 18|
| `exp4`|`-n 2 --min-match 2 --max-repeat 100 -a 10`|reused passages consist of at least 2 shared n-grams of size 2 (bi-grams), and the aligned passage should be at least 10 characters long (default is `20`)|1909 (lemmatised), 2078 (raw)|# of ground-truth cluster: 69, # of matched clusters: 46, # of unmatched clusters: 23, # of partially matched clusters: 2, # of exactly matched clusters: 20, # of clusters with spurious passages: 24|
| `exp5`|`-n 3 --min-match 1 --max-repeat 100 -a 10`|reused passages consist of at least 1 shared n-grams of size 3 (tri-grams), and the aligned passage should be at least 10 characters long (default is `20`)|350 (lemmatised), 431 (raw)|# of ground-truth cluster: 69, # of matched clusters: 58, # of unmatched clusters: 11, # of partially matched clusters: 3, # of exactly matched clusters: 44, # of clusters with spurious passages: 11|
| `exp6`|`-n 4 --min-match 1 --max-repeat 100 -a 10`|reused passages consist of at least 1 shared n-grams of size 4 (bi-grams), and the aligned passage should be at least 10 characters long (default is `20`)|284 (lemmatised), 341 (raw)|# of ground-truth cluster: 69, # of matched clusters: 58, # of unmatched clusters: 11, # of partially matched clusters: 3, # of exactly matched clusters: 47, # of clusters with spurious passages: 8|
| `exp7`|`-n 3 --min-match 2 --max-repeat 100 -a 10`|reused passages consist of at least 1 shared n-grams of size 3 (tri-grams), and the aligned passage should be at least 10 characters long (default is `20`)|350 (lemmatised), 431 (raw)|# of ground-truth cluster: 69, # of matched clusters: 58, # of unmatched clusters: 11, # of partially matched clusters: 3, # of exactly matched clusters: 44, # of clusters with spurious passages: 11|

## Dices tags

Since these are not commented anywhere, here is the full list of tags and their explanation:

| Dices tag      | Expansion |
| ----------- | ----------- |
| cha         | Challenge |
| com | Command |
| con | Consolation|
| del | Deliberation|
| des | Desire and Wish|
| exh | Exhortation and Self-Exhortation|
| far | Farewell|
| gre | Greeting and Reception|
| inf | Information and Description|
| ins | Instruction|
| inv | Invitation |
| lam | Lament |
| lau | Praise and Laudation |
| mes | Message|
| nar | Narration|
| ora | Prophecy, Oracular Speech, and Interpretation|
| per | Persuasion|
| pra | Prayer|
| que | Question|
| req | Request|
| res | Reply to Question|
| tau | Taunt|
| thr | Threat|
| und | Undefined|
| vit | Vituperation|
| vow | Promise and Oath|
| war | Warning|