# Figure source data

This directory contains the **processed plotting inputs** used by the six main-figure notebooks and 23 supplementary-figure notebooks of the accompanying drought-propagation manuscript. It also supplies the complete values for Supplementary Tables 1–15. The materials support reproduction of **published figures from derived data**, not reconstruction of the complete upstream event catalogues or statistical workflow.

## Directory layout

The source data are available as ordinary folders in this repository; **no ZIP download or extraction step is required**.

| Directory | Contents |
| --- | --- |
| `main/` | Figure-specific inputs and documentation for the six main figures, including Figure 4 fitting-line coordinates |
| `shared/` | Inputs used across figures; original source-relative GRUN, ERA5-Land and GLDAS branches are retained for path compatibility |
| `supplementary/` | Inputs for Supplementary Figures 1–23, plus 15 complete Supplementary Table CSVs |

```text
figure_source_data/
├── README.md
├── main/
│   ├── figure_01/ ... figure_06/
│   └── figure_04/regional_fit_lines.csv
├── shared/
└── supplementary/
    ├── figure_01/ ... figure_23/
    └── tables/
        ├── Supplementary_Table_01.csv
        └── ... Supplementary_Table_15.csv
```

The plotting notebooks use the relative paths shown above. The `shared/` subtree deliberately preserves source-derived subdirectory names rather than flattening files with potentially identical basenames.

## Data provenance and interpretation

`main/` and `shared/` use the source-data naming conventions needed by the plotting code. File and folder names such as `ERA5_try` in the shared directory are retained for path compatibility; figures describing ERA5 runoff use **ERA5-Land** data, whereas ERA5 soil-water variables come from a separate reanalysis. GRUN is the primary retrospective runoff product and GLDAS is another sensitivity product. Refer to the manuscript and Supplementary Methods for definitions, calibration periods and product-specific eligibility.

These directories contain figure-ready statistical summaries and other derived arrays, not the complete meteorological or hydrological drought-event catalogues. Some source-file basenames and provenance labels point to upstream materials **not distributed here**. Nothing in these directories should be interpreted as a release of the upstream raw NetCDF files, original event-matching computations or model-training code.

## Inventory and validation

The repository-level `manifests/INPUT_DATA_MANIFEST.csv` lists source-data dependencies and hashes; `manifests/FIGURE_SOURCE_MANIFEST.csv` documents figure-input relationships. `VALIDATION_SUMMARY.md` reports the scope of the previously completed 29-figure rendering verification. That verification was performed in a controlled candidate directory; it is not a separate verification of a new user environment or operating system.

Nine NPZ plotting inputs have previously been flagged for embedded local `source_path` metadata. This metadata is not needed to identify the published data source and should be reviewed or redacted in a documented way before any further redistribution. Do not alter scientific arrays or substitute reconstructed figure values when correcting metadata. Consult `THIRD_PARTY_NOTICES.md` for external resources and attribution; public hosting does not override any applicable upstream licensing terms.
