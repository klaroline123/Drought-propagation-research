# Temporal representation of multievent meteorological antecedents alters inferred global drought propagation trends

Local public-release candidate for the manuscript's frozen main and supplementary figures. **6/6 main figures and 23/23 supplementary figures independently reproduced with exact frozen-PNG pixel equality. Figure 4 recovery is documented in audits/FIGURE04_FROZEN_LINE_RECOVERY.md.**

The package contains 29 notebook entries, 15 complete supplementary-table CSVs and 237 CSV plus 24 non-CSV plotting/resource files (32,097,114 bytes). Counts exclude manifests, documentation and generated outputs. Publication authorization and a code/data license remain pending; do not upload this entire working directory.

## Install and run

Tested with Python 3.13.5 and the versions pinned in `requirements.txt`:

```sh
python -m venv .venv
# Activate .venv for your operating system, then:
python -m pip install -r requirements.txt
python plot_utils/verify_package.py
python plot_utils/run_notebooks.py main_figures/Figure01.ipynb
```

Alternatively, `conda env create -f environment.yml`. Start `jupyter lab` in this repository, open any notebook, restart its kernel and run all cells. Notebook root discovery supports the repository root, its notebook directories, and a parent containing a `github` directory. There is no workstation-specific source path.

`python plot_utils/run_notebooks.py` executes all code cells in a fresh Python process for each of the 29 notebooks, continues after failures and returns a nonzero exit code if a notebook fails. This is also the validated execution method. Jupyter kernel-protocol launch was attempted but did not complete in the local execution environment; a successful Jupyter frontend run is not claimed. Notebooks contain ordinary Python cells and no kernel magics. The pinned environment is a tested installed runtime, not a separately installed clean virtual environment.

Main outputs are in `outputs/main/figure_XX/`; SI outputs are in `outputs/supplementary/figure_XX/02_FIGURES/`. PNG, PDF and SVG exports retain their original source stems. Font names and style are preserved. Arial and Times New Roman are system fonts and are not redistributed; systems without them can produce font/layout differences. No network download is needed for plotting inputs.

## Figure entries

| Figure | Notebook | Status |
|---|---|---|
| Main Figure 1 | main_figures/Figure01.ipynb | READY |
| Main Figure 2 | main_figures/Figure02.ipynb | READY |
| Main Figure 3 | main_figures/Figure03.ipynb | READY |
| Main Figure 4 | main_figures/Figure04.ipynb | READY |
| Main Figure 5 | main_figures/Figure05.ipynb | READY |
| Main Figure 6 | main_figures/Figure06.ipynb | READY |
| SI Figure 1 | supplementary_figures/Supplementary_Figure01.ipynb | READY |
| SI Figure 2 | supplementary_figures/Supplementary_Figure02.ipynb | READY |
| SI Figure 3 | supplementary_figures/Supplementary_Figure03.ipynb | READY |
| SI Figure 4 | supplementary_figures/Supplementary_Figure04.ipynb | READY |
| SI Figure 5 | supplementary_figures/Supplementary_Figure05.ipynb | READY |
| SI Figure 6 | supplementary_figures/Supplementary_Figure06.ipynb | READY |
| SI Figure 7 | supplementary_figures/Supplementary_Figure07.ipynb | READY |
| SI Figure 8 | supplementary_figures/Supplementary_Figure08.ipynb | READY |
| SI Figure 9 | supplementary_figures/Supplementary_Figure09.ipynb | READY |
| SI Figure 10 | supplementary_figures/Supplementary_Figure10.ipynb | READY |
| SI Figure 11 | supplementary_figures/Supplementary_Figure11.ipynb | READY |
| SI Figure 12 | supplementary_figures/Supplementary_Figure12.ipynb | READY |
| SI Figure 13 | supplementary_figures/Supplementary_Figure13.ipynb | READY |
| SI Figure 14 | supplementary_figures/Supplementary_Figure14.ipynb | READY |
| SI Figure 15 | supplementary_figures/Supplementary_Figure15.ipynb | READY |
| SI Figure 16 | supplementary_figures/Supplementary_Figure16.ipynb | READY |
| SI Figure 17 | supplementary_figures/Supplementary_Figure17.ipynb | READY |
| SI Figure 18 | supplementary_figures/Supplementary_Figure18.ipynb | READY |
| SI Figure 19 | supplementary_figures/Supplementary_Figure19.ipynb | READY |
| SI Figure 20 | supplementary_figures/Supplementary_Figure20.ipynb | READY |
| SI Figure 21 | supplementary_figures/Supplementary_Figure21.ipynb | READY |
| SI Figure 22 | supplementary_figures/Supplementary_Figure22.ipynb | READY |
| SI Figure 23 | supplementary_figures/Supplementary_Figure23.ipynb | READY |

## Data and scope

- Complete tables: `figure_source_data/supplementary/tables/Supplementary_Table_01.csv` through `Supplementary_Table_15.csv`.
- SI frozen panel inputs: `figure_source_data/supplementary/figure_01/` through `figure_23/`.
- Main and cross-figure inputs: `figure_source_data/shared/`. Their relative source subdirectories are retained to distinguish product branches and avoid duplication. Per-main-figure folders provide pointers to the exact shared files.
- Geography and frozen label resources: `assets/geography/` and `assets/other/`.
- `manifests/INPUT_DATA_MANIFEST.csv` lists actual included files, hashes, consumers, transformations and release decisions. `FIGURE_SOURCE_MANIFEST.csv` records the runtime dependency graph.

GRUN is the primary runoff representation. ERA5-Land is a runoff sensitivity product; runoff labeled ERA5 in the figures refers to ERA5-Land. ERA5 soil moisture comes from the separate ERA5 reanalysis. GLDAS is the third runoff product. SPEIbase metadata and the corrected product descriptions in Supplementary Table 1 follow the final SI. Only candidate metadata text and source-path labels were edited; numerical table values retain source precision. Source-file basenames in provenance fields identify archival sources, not additional files promised in this repository.

Included data are frozen summaries, stored bootstrap draws, gridded display summaries, geographic resources and a two-column same-event display dataset. MI pickle summaries were losslessly converted to Parquet; pickle is not shipped. The same-event Parquet retains every one of the 189,254 plotted rows and only the two distance columns, without event identifiers. No raw global NetCDF, complete event catalogue, event identification, matching, PT computation, trend estimation, bootstrap execution, explanatory/severity fitting or pseudo-prospective training is supplied or run. Drawing operations such as the original hexbin and violin rendering remain unchanged.

Current copy hashes establish current identity, not universal historical execution provenance. Final Word image hashes and exact regenerated pixels provide additional figure-specific evidence. Unplotted supporting columns do not acquire a historical freeze claim from pixel equality.

`audits/internal/`, outputs, executed notebooks, backups and local evidence are excluded by `.gitignore`. Consult `GITHUB_UPLOAD_CHECKLIST.md` and `audits/FINAL_GITHUB_RELEASE_REPORT.md` before any future release. No upload, remote push, DOI creation or license assignment was performed. `CITATION.cff` has a provisional title only; authors and the eventual paper citation must be completed without inventing a DOI.
