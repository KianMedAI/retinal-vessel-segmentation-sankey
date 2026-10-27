# Retinal vessel segmentation review: Sankey scripts

A cleaned, adapted implementation of the authors' supplied scripts for main Figure 5 and supplementary Figures 2 and 3. It generates new figures, not guaranteed pixel-identical copies of the submitted figures. Compare diagrams, category assignments, counts, and captions against the original outputs before replacing any figure. The input spreadsheets and original figures are not included.

## Installation
Install Python and run `pip install pandas openpyxl plotly`. Optional PDF export requires Kaleido and a working Chrome installation, following Plotly documentation.

## Running
The script reads the first Excel sheet by default; use `--sheet SHEETNAME` to choose another. Run from a terminal in the folder with the script and workbooks:

```
python create_sankey.py main5 "SANKEY_Category (10).xlsx"
python create_sankey.py supp2 "sankey_1 (1).xlsx"
python create_sankey.py supp3 "sankey_1 (1).xlsx"
```
Add `--pdf figure.pdf` for optional PDF export. HTML outputs open in a web browser. Main Figure 5 requires `Record ID`, `Method Type`, and `Subcategory`. Supplementary Figure 2 requires `Standard test set used?`, `Subcategory`, and all seven metric columns. Supplementary Figure 3 requires `Subcategory`, `Augmentation`, `Preprocessing`, `Postprocessing`, and all seven metric columns. Metric columns: Accuracy, Sensitivity, Specificity, Dice, AUCROC, F1, MCC.

Each spreadsheet row is treated as one observation. Verify unique studies and inclusion, and avoid claiming a row count is a study count until verified. For main Figure 5 unique Record IDs are required. The `Standard test set used?` column is plotted verbatim; it must not be called a dataset unless workbook values support that interpretation. Y/N fields have Y = With, N = Without, and all other values = Unknown. Metrics are counted only when values parse as numbers; missing and nonnumeric values are not counted. One row may contribute to multiple metric links; No Metrics denotes no recognized numeric values, not proof that no metrics were reported in the paper. Adjacent-stage links in supplementary Figure 3 do not preserve complete individual paths through intermediary nodes. The diagrams show counts, not performance or causal effects.

The cleaned script is derived from the supplied scripts. It removes hard-coded statistics, validates required columns, and distinguishes missing Y/N values. It uses stage-specific node identifiers to prevent node-name collisions. It changes layout and may change classification of whitespace, missing entries and repeated identifiers. Validate differences against the original files.
