"""Sankey visualizations for the retinal vessel segmentation review.

Adapted from the scripts supplied by the authors. The workbook determines the
sample and categories; review its contents and outputs before publication.
"""
import argparse
from collections import Counter
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

METRICS = ['Accuracy', 'Sensitivity', 'Specificity', 'Dice', 'AUCROC', 'F1', 'MCC']

def label(value):
    if pd.isna(value) or not str(value).strip():
        return 'Unknown'
    return str(value).strip()

def binary(value):
    value = label(value).upper()
    return {'Y': 'With', 'N': 'Without'}.get(value, 'Unknown')

def reported(row):
    return [m for m in METRICS if pd.notna(pd.to_numeric(row[m], errors='coerce'))] or ['No Metrics']

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('figure', choices=['main5', 'supp2', 'supp3'])
    parser.add_argument('workbook', help='Path to the source Excel workbook')
    parser.add_argument('--sheet', default=0, help='Excel sheet name; default is the first sheet')
    parser.add_argument('--output', default=None, help='HTML output filename')
    parser.add_argument('--pdf', default=None, help='Optional PDF filename (requires Kaleido and Chrome)')
    args = parser.parse_args()
    df = pd.read_excel(args.workbook, sheet_name=args.sheet)
    columns = {
        'main5': ['Record ID', 'Method Type', 'Subcategory'],
        'supp2': ['Standard test set used?', 'Subcategory'] + METRICS,
        'supp3': ['Subcategory', 'Augmentation', 'Preprocessing', 'Postprocessing'] + METRICS,
    }[args.figure]
    missing = [c for c in columns if c not in df.columns]
    if missing:
        raise SystemExit('Missing columns: ' + ', '.join(missing))
    if df.empty:
        raise SystemExit('Workbook contains no rows.')
    if args.figure == 'main5':
        if df['Record ID'].isna().any() or df['Record ID'].astype(str).str.strip().duplicated().any():
            raise SystemExit('Record ID must be present and unique for each row. Check the workbook.')
        stages = [['All papers', label(r['Method Type']), label(r['Subcategory'])] for _, r in df.iterrows()]
        titles = ['All papers', 'Method type', 'Subcategory']
    elif args.figure == 'supp2':
        stages = [[label(r['Standard test set used?']), label(r['Subcategory']), reported(r)] for _, r in df.iterrows()]
        titles = ['Standard test set used?', 'Subcategory', 'Reported metric']
    else:
        stages = [[label(r['Subcategory']), 'Aug ' + binary(r['Augmentation']), 'Pre ' + binary(r['Preprocessing']), 'Post ' + binary(r['Postprocessing']), reported(r)] for _, r in df.iterrows()]
        titles = ['Subcategory', 'Augmentation', 'Preprocessing', 'Postprocessing', 'Reported metric']
    # Stage-indexed keys prevent identical labels in different columns merging.
    pairs = Counter()
    for row in stages:
        for i in range(len(row)-1):
            right = row[i+1] if isinstance(row[i+1], list) else [row[i+1]]
            for value in right:
                pairs[((i, row[i]), (i+1, value))] += 1
    nodes = sorted({node for pair in pairs for node in pair}, key=lambda x: (x[0], x[1]))
    indexes = {key: i for i, key in enumerate(nodes)}
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    fig = go.Figure(go.Sankey(node=dict(pad=20, thickness=25, line=dict(color='black', width=0.5), label=[n[1] for n in nodes], color=[colors[n[0]] for n in nodes]), link=dict(source=[indexes[a] for a,b in pairs], target=[indexes[b] for a,b in pairs], value=list(pairs.values()))))
    fig.update_layout(title=' → '.join(titles), font=dict(family='Arial', size=13, color='black'), width=1400, height=900)
    output = args.output or args.figure + '.html'
    fig.write_html(output)
    print(f'Rows analyzed: {len(df)}; output: {output}')
    if args.figure in ('supp2', 'supp3'):
        counts = Counter(m for row in stages for m in row[-1])
        print('Metric links (one row may report multiple metrics):', dict(counts))
    if args.pdf:
        try:
            fig.write_image(args.pdf)
            print(f'PDF: {args.pdf}')
        except Exception as e:
            print(f'PDF export failed: {e}. HTML was saved; check Kaleido and Chrome.')

if __name__ == '__main__':
    main()
