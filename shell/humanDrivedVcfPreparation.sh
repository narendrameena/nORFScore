

#mapped only variants 
bedtools intersect -a  ../../../data/input/variants/humanDerived_SNVs_with_id.vcf.gz -b  ../../../data/input/nORF/nORF_db_v2_without_chr.bed.gz   -wa | sort | uniq -c | awk '{print  $2 "\t" $3 "\t" $4 "\t" $5 "\t" $6}' > human_drive_mapped_to_norfs_db_v2.vcf

#mapped with norf infor 
bedtools intersect -a  ../../../data/input/variants/humanDerived_SNVs_with_id.vcf.gz -b  ../../../data/input/nORF/nORF_db_v2_without_chr.bed.gz  -wo | sort | uniq -c | awk '{print  $0}' > human_drive_mapped_to_norfs_db_v2_with_norfs.txt
