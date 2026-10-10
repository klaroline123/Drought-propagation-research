# Clean candidate validation

The exact 29 candidate notebooks were copied to an isolated repository and executed in fresh Python processes, with every code cell run in order. All **29/29 passed** and all **29 rendered PNGs match the final frozen images pixel for pixel** (RGB and RGBA). These results come from new execution, not file existence. Source notebook, helper and frozen-input hashes are unchanged from the verified working package.

An audit hook restricted writes to the isolated repository and blocked reads of private scientific data outside it; installed runtime libraries and fonts remained available. Actual candidate dependency reads were checked against candidate files. Native GIS sidecars were additionally retained and checked. Generated images, logs, runtime caches and executed notebooks stay outside this upload candidate.

Integrity checks cover 261 inputs/resources, all 15 full SI tables, six main notebooks, 23 SI notebooks, required helper modules and manifest dependencies. The alignment helper is a required import for all 29 figures and is included with its verified upstream license. Historical Python bytecode/cache access edges are excluded from the public dependency list; the required source modules remain included.

The safety review checks text for workstation paths and credential-like values, Parquet metadata/string columns, NPZ string arrays and archive member paths. **Safety check NOT PASSED:** nine required NPZ files contain workstation paths in their source_path string metadata. They remain byte-identical because frozen-data modification is explicitly prohibited. The sanitized issue list is in manifests/REDACTION_REVIEW_REQUIRED.csv. No credential-like pattern or archive traversal was found. This finite scan is not a guarantee against every possible secret. No internal reports, outputs, backups, test copies or obsolete missing-input notice are distributed.

Limitations: this is an isolated package copy in the installed Python environment, not an independently installed environment or an OS-level sandbox. Jupyter kernel-protocol execution and clean environment installation remain unverified. Font availability can affect exact pixels elsewhere. `manifests/REPRODUCTION_STATUS.csv` describes this execution separately from publication authorization.

**Release status remains HOLD:** nine embedded-path redactions require a separate author decision; 256 data/resource author approvals, the authors' code/data license decision and citation metadata are unresolved. No upload has occurred.
