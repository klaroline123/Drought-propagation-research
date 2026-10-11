# Temporal representation of multievent meteorological antecedents alters inferred global drought propagation trends

## Overview

This repository provides the **figure-generation notebooks and processed plotting inputs** accompanying the manuscript *Temporal representation of multievent meteorological antecedents alters inferred global drought propagation trends*. It contains notebooks for all **six main figures** and **23 supplementary figures**, together with the source data used to draw them and the complete data for **Supplementary Tables 1–15**.

The repository is a **figure-level reproducibility resource**, not a release of the complete upstream research workflow. In particular, it does not include raw global climate/runoff archives, the full drought-event catalogues, or code for event detection and pairing, propagation-time estimation, upstream trend and statistical analyses, or pseudo-prospective model fitting.

## Repository contents

| Path | Contents |
| --- | --- |
| `main_figures/` | Six figure notebooks: `Figure01.ipynb`–`Figure06.ipynb` |
| `supplementary_figures/` | 23 notebooks: `Supplementary_Figure01.ipynb`–`Supplementary_Figure23.ipynb` |
| `figure_source_data/` | Processed plotting inputs in `main/`, `shared/` and `supplementary/`; see its README |
| `assets/` | Geographic boundary and plotting-layout resources |
| `plot_utils/` | Figure-rendering helpers and local validation scripts |
| `manifests/` | Input/dependency inventories, checksums and reproduction-status records |
| `requirements.txt`, `environment.yml` | Python environment specifications |
| `VALIDATION_SUMMARY.md` | Scope, results and limitations of the packaging validation |
| `THIRD_PARTY_NOTICES.md` | Attribution and third-party resource notices |
| `CITATION.cff` | Provisional software citation metadata; update when final bibliographic information is available |

## Figure source data layout

The processed data are provided as ordinary directories in the repository and **do not require extraction**. The plotting notebooks resolve inputs relative to the repository root:

```text
figure_source_data/
    main/
    shared/
    supplementary/
```

The recovered Figure 4 plotting-line coordinates are located at `figure_source_data/main/figure_04/regional_fit_lines.csv`. Full supplementary tables are in `figure_source_data/supplementary/tables/`, named `Supplementary_Table_01.csv` through `Supplementary_Table_15.csv`.

See [the source-data README](figure_source_data/README.md) for a directory guide and `manifests/INPUT_DATA_MANIFEST.csv` for the recorded input inventory.

## Install and reproduce figures

The candidate package was tested with Python **3.13.5** and the dependencies recorded in `requirements.txt`. An independent installation into a completely fresh environment and interactive Jupyter-kernel execution were **not** established by the validation report.

```bash
python -m venv .venv
# Activate the environment for your operating system.
python -m pip install -r requirements.txt
python plot_utils/verify_package.py
python plot_utils/run_notebooks.py main_figures/Figure01.ipynb
```

`python plot_utils/run_notebooks.py` without a notebook argument runs all figure notebooks under its supported execution workflow. Alternatively, the notebooks may be opened in Jupyter with the supplied data directories; reproducing identical pixels outside the tested environment can depend on installed fonts and rendering libraries.

Figure outputs are written beneath `outputs/main/` and `outputs/supplementary/` by the corresponding notebooks. These generated outputs are not required to be committed to the repository.

## Reproducibility record and limitations

The release-validation report records **29/29 notebook executions** and pixel-identical rendered PNGs against the manuscript's frozen figure images in an isolated copy of the package using an installed Python environment. That result supports **figure generation from supplied processed inputs**; it does not independently reproduce the upstream analyses or establish that all software environments will render identical pixels. Refer to `VALIDATION_SUMMARY.md` and `manifests/REPRODUCTION_STATUS.csv` for the tested scope.

The source data include processed statistical summaries, grid/display products, stored uncertainty draws and data used in individual panels. GRUN is the principal retrospective runoff representation; the labels `ERA5` in runoff figures refer to **ERA5-Land runoff**, whereas **ERA5 soil moisture** comes from a separate ECMWF dataset. GLDAS is a third runoff representation. The three products are not independent observational replications.

Nine NPZ plotting inputs were flagged in the earlier validation record as potentially retaining original `source_path` metadata associated with supplementary figures. These paths are provenance metadata, not additional analysis inputs. Whether the current public copies have been redacted should be verified before treating the repository as privacy-reviewed. The original validation report also notes that source-data redistribution permissions and the repository-wide code/data licence had not been finally resolved; public availability does not itself establish third-party relicensing rights.

## Citation and data sources

Please cite the associated manuscript when bibliographic details become available, and cite the underlying SPEIbase, GRUN, ERA5/ERA5-Land and GLDAS data sources as described in the manuscript. See `CITATION.cff` for the currently available citation metadata and `THIRD_PARTY_NOTICES.md` for third-party acknowledgements. No paper DOI or archival dataset DOI is asserted here.
