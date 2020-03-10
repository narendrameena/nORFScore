#map hgmd variants to norfs db v2
bedtools intersect -a  ../../../data/input/variants/HGMD_PRO_2016.4_hg38.vcf.gz -b  ../../../data/input/nORF/nORF_db_v2_without_chr.bed.gz  -wa | sort | uniq -c | awk '{print  $2 "\t" $3 "\t" $4 "\t" $5 "\t" $6"\t" $7 "\t" $8 "\t" $9}' > hgmd_mapped_to_norfs_db_v2.txt 

#variants with norfs info 
bedtools intersect -a  ../../../data/input/variants/HGMD_PRO_2016.4_hg38.vcf.gz -b  ../../../data/input/nORF/nORF_db_v2_without_chr.bed.gz  -wo | sort | uniq -c | awk '{print  $0}' > hgmd_mapped_to_norfs_db_v2_with_norf_info.txt 

#slecting pathogenic ones
 cat hgmd_mapped_to_norfs_db_v2.txt | grep -v "##" | awk '{split($8,a,"CLASS=");split(a[2],b,";");split($8,c,"DB=");split(c[2],d,";"); print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $5 "\t" b[1] "\t"d[1]}' | awk '$6=="DM"{ print $0}'  > hgmd_mapped_db_v2_pathogenic_DM.txt

#converting into proper vcf
cat hgmd_mapped_to_norfs_db_v2.txt | awk '{print $1 "\t" $2 "\t.\t"$4 "\t" $5"\t.\t.\t."}' > hgmd_db_v2_Pathogenic_only.vcf

##adding header 
##fileformat=VCFv4.2
#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO