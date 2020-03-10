#bed without chr 

zcat norf_db_v2.bed.gz | sed 's/^.\{,3\}//'   > nORF_db_v2_without_chr.bed

#map variants and only get varaints information 
bedtools intersect -a  ../../../data/input/variants/clinvar_20190429.vcf.gz -b  ../../../data/input/nORF/nORF_db_v2_without_chr.bed.gz  -wa | sort | uniq -c | awk '{print  $2 "\t" $3 "\t" $4 "\t" $5 "\t" $6"\t" $7 "\t" $8 "\t" $9}' > clinvar_vriants_mapped_to_norf_db_v2.vcf

#map variants with norf info 
bedtools intersect -a  ../../../data/input/variants/clinvar_20190429.vcf.gz -b  ../../../data/input/nORF/nORF_db_v2_without_chr.bed.gz  -wa -wb | sort | uniq -c | awk '{print  $0}' > clinvar_vriants_mapped_to_norf_db_v2_all_info.txt

#slect only pathgenic variants 
cat clinvar_vriants_mapped_to_norf_db_v2.vcf  | grep -v "^##" | awk '{split($8,a,"CLNSIG=");split(a[2],b,";");split($8,c,"RS=");split(c[2],d,";"); print $1 "\t" $2 "\t" $3 "\t" $4 "\t"$5"\t" b[1] "\t" d[1]}' | awk '$6=="Pathogenic"{print $0}' > clivar_db_v2_mapped_Pathogenic.txt

#convert into poper vcf file 
cat clivar_db_v2_mapped_Pathogenic.txt | awk '{print $1 "\t" $2 "\t.\t"$4 "\t" $5"\t.\t.\t."}' > clivar_db_v2_Pathogenic_only.txt

#sort vcf file 
sort -k1,1V -k2,2n clivar_db_v2_Pathogenic_only.txt > clivar_db_v2_Pathogenic_only_sort.vcf

bgzip < clivar_db_v2_Pathogenic_only_with_chr_sort.vcf> clivar_db_v2_Pathogenic_only_with_chr_sort.vcf.bgz

#add header to vcf file 
##fileformat=VCFv4.2
#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO

