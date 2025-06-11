# Exploring repetitions in Homeric speeches

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15637935.svg)](https://doi.org/10.5281/zenodo.15637935)


Authors: [Ombretta Cesca (UNIL)](https://orcid.org/0000-0002-0658-8998) and [Matteo Romanello (UNIL)](https://orcid.org/0000-0002-7406-6286).

This repository contains code & data concerning the automatic extraction of repetitions from Homeric speeches contained in the [DICES](https://github.com/cwf2/dices) database with [passim](https://github.com/dasmiq/passim), as described in the following publication:

> O. Cesca and M. Romanello. (forthcoming) "A Computational Approach to Characters’ Intentional Repetitions in Homeric Epic" in *A Computational Approach to Characters’ Intentional Repetitions in Homeric Epic*, C. W. Forstall & B. Verhelst (edds.), De Gruyter Brill. 

## Code

Here is an overview of the notebooks contained in this repository:

| Notebook  | Description |
| ------------- | ------------- |
| [Get data.ipynb](./notebooks/Get%20data.ipynb) | Retrieve Homeric speeches from DICES DB; fetch full-text from Perseus and apply CLTK processing (lemmatisation); convert data to a Pandas dataframe and then to passim's JSON format.  |
| [Experiments.ipynb](./notebooks/Experiments.ipynb) | Run the passim experiments according to the configurations specified in files `data/experiments_*.json`.  |
| [Evaluation.ipynb](./notebooks/Evaluation.ipynb) | Run (some) evaluation and inspect closely the results. | 
| [Final evaluation.ipynb](./notebooks/Final%20evaluation.ipynb) |  Run the (final) evaluation of all epxeriments and produce the results table for the publication. | 
| [Analysis.ipynb](./notebooks/Final%20evaluation.ipynb) | Some basic stats of repetitions extracted with the best performing configuration, before and after manual curation (to remove embedded speeches). |

## Data

The file [`homeric_repetitions_dataset.tsv`](./data/homeric_repetitions_dataset.tsv) contains the ground-truth dataset used to evaluate the accuracy of automatically extracting repetitions with [passim](https://github.com/dasmiq/passim). This dataset was created manually by O. Cesca and contains repetitions found in the *Iliad*.  It consists of 69 sets of repetitions (i.e. clusters), each containing two or more text passages where the repeated text is found, for a total of 147 repeated passages of varying length. Each passage is linked to the corresponding speech in the DICES database.

## DICE tags

<details>
<summary>
Show table with expansion of tags
</summary>

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
</details>