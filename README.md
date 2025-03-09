# ARC

## NCBI searches based on genomic keywords.
~~~
python Download_Genomic.py
~~~

## Search the papers for the genome storage Bioproject number.
~~~
bash Down.sh -p PRNA**** -o PRNA****
~~~

## Annotate the genome using gtdbtk.
~~~
bash gtdbtk.sh
~~~

## The target genome was screened according to the gtdbtk annotation results.
~~~
python select.py

### example:PRJEB38681  PRJEB38681.gtdbtk.ar53.summary.tsv
~~~
