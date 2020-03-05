ls -lrth ../../../data/encode/Open_chromatin_DNase-seq/ | awk '{split($9,a,".bed"); print a[1]}' | xargs -I {} -P 40 sh -c 'bedtools intersect -a ../../../data/input/nORF/all_38.6.bed -b ../../../data/encode/Open_chromatin_DNase-seq/{}.bed.gz -f 0.50 > {}_overlap.bed'



#closest command 

#open chromatin 

ls -lrth ../../../data/encode/Open_chromatin_DNase-seq/ | awk '{split($9,a,".bed"); print a[1]}' | grep -v  'meta' |  grep -v '^[[:space:]]' | xargs -n 2  -P 80 sh -c 'bedtools closest -a ../../../data/input/nORF/all_38.6.bed -b ../../../data/encode/Open_chromatin_DNase-seq/$0.bed.gz ../../../data/encode/Open_chromatin_DNase-seq/$1.bed.gz  -names $0 $1 -D a -t all -k 10  > $0_$1_closest.bed'


#histon marks 

ls -lrth ../../../data/encode/Histone_mark_enrichment_ChIP-seq/ |grep 'bed.gz'| awk '{split($9,a,".bed"); print a[1]}' | grep -v  'meta' |  grep -v '^[[:space:]]' | xargs -n 2  -P 80 sh -c 'zcat  ../../../data/encode/Histone_mark_enrichment_ChIP-seq/$0.bed.gz | sort -k 1,1 -k2,2n > ../../../data/encode/Histone_mark_enrichment_ChIP-seq/$0_sort.bed.gz ;zcat  ../../../data/encode/Histone_mark_enrichment_ChIP-seq/$1.bed.gz | sort -k 1,1 -k2,2n > ../../../data/encode/Histone_mark_enrichment_ChIP-seq/$1_sort.bed.gz ;bedtools closest -a ../../../data/input/nORF/all_38.6.bed -b ../../../data/encode/Histone_mark_enrichment_ChIP-seq/$0_sort.bed.gz ../../../data/encode/Histone_mark_enrichment_ChIP-seq/$1_sort.bed.gz  -names $0 $1 -D a -t all -k 10  > $0_$1_closest.bed;rm ../../../data/encode/Histone_mark_enrichment_ChIP-seq/$0_sort.bed.gz;rm ../../../data/encode/Histone_mark_enrichment_ChIP-seq/$1_sort.bed.gz '


#Transcription factor binding (TF ChIP-seq)

ls -lrth ../../../data/encode/Transcription_factor_binding_TF_ChIP-seq/ |grep 'bed.gz'| awk '{split($9,a,".bed"); print a[1]}' | grep -v  'meta' |  grep -v '^[[:space:]]' | xargs -n 2  -P 80 sh -c 'zcat  ../../../data/encode/Transcription_factor_binding_TF_ChIP-seq/$0.bed.gz | sort -k 1,1 -k2,2n > ../../../data/encode/Transcription_factor_binding_TF_ChIP-seq/$0_sort.bed.gz ;zcat  ../../../data/encode/Transcription_factor_binding_TF_ChIP-seq/$1.bed.gz | sort -k 1,1 -k2,2n > ../../../data/encode/Transcription_factor_binding_TF_ChIP-seq/$1_sort.bed.gz ;bedtools closest -a ../../../data/input/nORF/all_38.6.bed -b ../../../data/encode/Transcription_factor_binding_TF_ChIP-seq/$0_sort.bed.gz ../../../data/encode/Transcription_factor_binding_TF_ChIP-seq/$1_sort.bed.gz  -names $0 $1 -D a -t all -k 10  > $0_$1_closest.bed;rm ../../../data/encode/Transcription_factor_binding_TF_ChIP-seq/$0_sort.bed.gz;rm ../../../data/encode/Transcription_factor_binding_TF_ChIP-seq/$1_sort.bed.gz '

#Topologically associating domains (TADs) and compartments (Hi-C)

#.txt 
ls -lrth ../../../data/encode/Topologically_associating_domains_TADs_and_compartments_Hi_C/tad_hg38 |grep '.txt'| awk '{split($9,a,".txt"); print a[1]}' | grep -v  'meta' |  grep -v '^[[:space:]]' | xargs -n 2  -P 80 sh -c 'zcat  ../../../data/encode/Topologically_associating_domains_TADs_and_compartments_Hi_C/tad_hg38/$0.txt | sort -k 1,1 -k2,2n > ../../../data/encode/Topologically_associating_domains_TADs_and_compartments_Hi_C/tad_hg38/$0_sort.bed.gz ;zcat  ../../../data/encode/Topologically_associating_domains_TADs_and_compartments_Hi_C/tad_hg38/$1.txt | sort -k 1,1 -k2,2n > ../../../data/encode/Topologically_associating_domains_TADs_and_compartments_Hi_C/tad_hg38/$1_sort.bed.gz ;bedtools closest -a ../../../data/input/nORF/all_38.6.bed -b ../../../data/encode/Topologically_associating_domains_TADs_and_compartments_Hi_C/tad_hg38/$0_sort.bed.gz ../../../data/encode/Topologically_associating_domains_TADs_and_compartments_Hi_C/tad_hg38/$1_sort.bed.gz  -names $0 $1 -D a -t all -k 10  > $0_$1_closest.bed;rm ../../../data/encode/Topologically_associating_domains_TADs_and_compartments_Hi_C/tad_hg38/$0_sort.bed.gz;rm ../../../data/encode/Topologically_associating_domains_TADs_and_compartments_Hi_C/tad_hg38/$1_sort.bed.gz;gzip $0_$1_closest.bed'

#.domains 

ls -lrth ../../../data/encode/Topologically_associating_domains_TADs_and_compartments_Hi_C/tad_hg38 |grep '.domains'| awk '{split($9,a,".domains"); print a[1]}' | grep -v  'meta' |  grep -v '^[[:space:]]' | xargs -n 2  -P 80 sh -c 'sed 's/^/chr/' ../../../data/encode/Topologically_associating_domains_TADs_and_compartments_Hi_C/tad_hg38/$0.domains| sort -k 1,1 -k2,2n > ../../../data/encode/Topologically_associating_domains_TADs_and_compartments_Hi_C/tad_hg38/$0_sort.bed.gz ;sed 's/^/chr/'  ../../../data/encode/Topologically_associating_domains_TADs_and_compartments_Hi_C/tad_hg38/$1.domains| sort -k 1,1 -k2,2n > ../../../data/encode/Topologically_associating_domains_TADs_and_compartments_Hi_C/tad_hg38/$1_sort.bed.gz ;bedtools closest -a ../../../data/input/nORF/all_38.6.bed -b ../../../data/encode/Topologically_associating_domains_TADs_and_compartments_Hi_C/tad_hg38/$0_sort.bed.gz ../../../data/encode/Topologically_associating_domains_TADs_and_compartments_Hi_C/tad_hg38/$1_sort.bed.gz  -names $0 $1 -D a -t all -k 10  > $0_$1_closest.bed;rm ../../../data/encode/Topologically_associating_domains_TADs_and_compartments_Hi_C/tad_hg38/$0_sort.bed.gz;rm ../../../data/encode/Topologically_associating_domains_TADs_and_compartments_Hi_C/tad_hg38/$1_sort.bed.gz '




#Promoter_enhancer_links_ChIA-PET

ls -lrth ../../../data/encode/Promoter_enhancer_links_ChIA-PET_hg19/hg38 |grep 'bed.gz'| awk '{split($9,a,".bed"); print a[1]}' | grep -v  'meta' |  grep -v '^[[:space:]]' | xargs -n 3  -P 80 sh -c 'zcat  ../../../data/encode/Promoter_enhancer_links_ChIA-PET_hg19/hg38/$0.bed.gz | sort -k 1,1 -k2,2n > ../../../data/encode/Promoter_enhancer_links_ChIA-PET_hg19/hg38/$0_sort.bed.gz ;zcat  ../../../data/encode/Promoter_enhancer_links_ChIA-PET_hg19/hg38/$1.bed.gz | sort -k 1,1 -k2,2n > ../../../data/encode/Promoter_enhancer_links_ChIA-PET_hg19/hg38/$1_sort.bed.gz ;zcat  ../../../data/encode/Promoter_enhancer_links_ChIA-PET_hg19/hg38/$2.bed.gz | sort -k 1,1 -k2,2n > ../../../data/encode/Promoter_enhancer_links_ChIA-PET_hg19/hg38/$2_sort.bed.gz ;bedtools closest -a ../../../data/input/nORF/all_38.6.bed -b ../../../data/encode/Promoter_enhancer_links_ChIA-PET_hg19/hg38/$0_sort.bed.gz ../../../data/encode/Promoter_enhancer_links_ChIA-PET_hg19/hg38/$1_sort.bed.gz ../../../data/encode/Promoter_enhancer_links_ChIA-PET_hg19/hg38/$2_sort.bed.gz -names $0 $1 $2 -D a -t all -k 10  > $0_$1_$2_closest.bed;rm ../../../data/encode/Promoter_enhancer_links_ChIA-PET_hg19/hg38/$0_sort.bed.gz;rm ../../../data/encode/Promoter_enhancer_links_ChIA-PET_hg19/hg38/$1_sort.bed.gz;rm ../../../data/encode/Promoter_enhancer_links_ChIA-PET_hg19/hg38/$2_sort.bed.gz ;gzip $0_$1_closest.bed '


#DNA methylation 

ls -lrth ../../../data/encode/DNA_methaylation_hg38/ |grep 'bed.gz'| awk '{split($9,a,".bed"); print a[1]}' | grep -v  'meta' |  grep -v '^[[:space:]]' | xargs -n 2  -P 80 sh -c 'zcat  ../../../data/encode/DNA_methaylation_hg38/$0.bed.gz |sort -k 1,1 -k2,2n > ../../../data/encode/DNA_methaylation_hg38/$0_sort.bed.gz ;zcat  ../../../data/encode/DNA_methaylation_hg38/$1.bed.gz | sort -k 1,1 -k2,2n > ../../../data/encode/DNA_methaylation_hg38/$1_sort.bed.gz ;bedtools closest  -a ../../../data/input/nORF/all_38.6.bed -b ../../../data/encode/DNA_methaylation_hg38/$0_sort.bed.gz ../../../data/encode/DNA_methaylation_hg38/$1_sort.bed.gz -names $0 $1  -D a -t all -k 10  > $0_$1_closest.bed;rm ../../../data/encode/DNA_methaylation_hg38/$0_sort.bed.gz;rm ../../../data/encode/DNA_methaylation_hg38/$1_sort.bed.gz;gzip $0_$1_closest.bed'


#gene Expression 

ls -lrth ../../../data/encode/Gene_expression_RNA-seq/bedFiles |grep 'bed.gz'| awk '{split($9,a,".bed"); print a[1]}' | grep -v  'meta' |  grep -v '^[[:space:]]' | xargs -n 2  -P 80 sh -c 'zcat   ../../../data/encode/Gene_expression_RNA-seq/bedFiles/$0.bed.gz |sort -k 1,1 -k2,2n > ../../../data/encode/Gene_expression_RNA-seq/bedFiles/$0_sort.bed.gz ;zcat  ../../../data/encode/Gene_expression_RNA-seq/bedFiles/$1.bed.gz |  sort -k 1,1 -k2,2n > ../../../data/encode/Gene_expression_RNA-seq/bedFiles/$1_sort.bed.gz ;bedtools closest  -a ../../../data/input/nORF/all_38.6.bed -b ../../../data/encode/Gene_expression_RNA-seq/bedFiles/$0_sort.bed.gz  ../../../data/encode/Gene_expression_RNA-seq/bedFiles/$1_sort.bed.gz -names $0 $1  -D a -t all -k 10  > $0_$1_closest.bed;rm ../../../data/encode/Gene_expression_RNA-seq/bedFiles/$0_sort.bed.gz;rm  ../../../data/encode/Gene_expression_RNA-seq/bedFiles/$1_sort.bed.gz;gzip $0_$1_closest.bed'
