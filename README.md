# CS 170 Fall 2019 Project

Matthew Tang, Christianna Xu: Group 117

## Usage 
* Generate outputs: `py .\solver.py --all inputs outputs` (~5min w/ multicore)
* Local Autograder: `py .\autograder.py --all inputs outputs` (~7min w/ multicore, caching)
* Superscorer: `py .\superscorer.py inputs outputs_folder1 ... outputs_foldern` (~1.5hrs)
* Add `--disableMulticore` to disable Multicore for autograder and solver
    * Note that Multicore supresses runtime errors
* Add `-v` for verbose autograder output

## Scores
Footsteps v0: 40.7345 (Deprecated)

Footsteps v2: 39.28

Footsteps v3: 39.273

Footsteps v3.5: 43.645

Footsteps v4: 39.019

Christofides v1: 60.780

Final superscore: 

## Instructions:
* Footsteps is the default solver. To switch to Christofides, uncomment out and return the solve call in `solver.py`
* Footsteps v4 is the final version
* Footsteps v2 uses `smart_output` instead of `smarter_output`. See the final report for more details.
* Footsteps v3 does not use a saturated set. See the final report for more details.
* Footsteps v3.5 had a bug where the newHomes was incorrectly calculated. But somehow, some of the outputs were better so the outputs were still superscored. See the final report for more details.
