##author narumeena
##description annotated using annovar 

#downlaod data source 

perl annotate_variation.pl -buildver hg38 -downdb -webfrom annovar refGene humandb/
perl annotate_variation.pl -buildver hg38 -downdb -webfrom annovar  knownGene humandb/
perl annotate_variation.pl -buildver hg38 -downdb -webfrom annovar ensGene humandb/
perl annotate_variation.pl -buildver hg38 -downdb -webfrom annovar ljb26_all humandb/
perl annotate_variation.pl -buildver hg38 -downdb -webfrom annovar dbnsfp31a_interpro humandb/
perl annotate_variation.pl -buildver hg38 -downdb -webfrom annovar dbnsfp33a humandb/
perl annotate_variation.pl -buildver hg38 -downdb -webfrom annovar dbscsnv11 humandb/
perl annotate_variation.pl -buildver hg38 -downdb -webfrom annovar intervar_20180118 humandb/
perl annotate_variation.pl -buildver hg38 -downdb -webfrom annovar cosmic70 humandb/
perl annotate_variation.pl -buildver hg38 -downdb -webfrom annovar mcap humandb/
perl annotate_variation.pl -buildver hg38 -downdb -webfrom annovar revel humandb/
perl annotate_variation.pl -buildver hg38 -downdb -webfrom annovar regsnpintron humandb/