# Exploring repetitions in Homeric speeches

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

## TR detection with Passim/Seriatim

First results available [here](https://docs.google.com/spreadsheets/d/1Aa0YiP9nzp-58UZ6u1dtRxNCAxoCdroQuWEhGIcZfoI/edit#gid=928319534) for exploration. 

## Experiments

| Experiment ID     | Passim parameters | Explanation  | \# of extracted clusters |
| ----------- | ----------- |----------|------------|
| `exp0`      | `-n 1 --min-match 1 -a 5` | reused passages consist of at least 1 shared n-grams of size 1 (uni-gram) | 1066 |
| `exp1`| `-n 3 --max-repeat 100`|reused passages consist of at least 5 shared n-grams of size 3 (uni-gram)|23|
| `exp2`|`-n 3 --min-match 3 --max-repeat 100 -w 1`|reused passages consist of at least 3 shared n-grams of size 3 (tri-grams)|24|
| `exp3`|`-n 3 --min-match 3 --max-repeat 100 -a 10`|reused passages consist of at least 3 shared n-grams of size 3, and the aligned passage should be at least 10 characters long (default is `20`)|41|
| `exp4`|`-n 2 --min-match 2 --max-repeat 100 -a 10`|reused passages consist of at least 2 shared n-grams of size 2 (bi-grams), and the aligned passage should be at least 10 characters long (default is `20`)|212|
| `exp5`|`-n 3 --min-match 1 --max-repeat 100 -a 10`|reused passages consist of at least 1 shared n-grams of size 3 (tri-grams), and the aligned passage should be at least 10 characters long (default is `20`)|41|
| `exp6`|`-n 4 --min-match 1 --max-repeat 100 -a 10`|reused passages consist of at least 1 shared n-grams of size 4 (bi-grams), and the aligned passage should be at least 10 characters long (default is `20`)|36|
