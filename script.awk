## Process first file of arguments. Save 'id' as key and 'No' as value
## of a hash.
FNR == NR {
    if ( FNR == 1 ) { 
        header = $2
        next
    }   
    hash[ $1 ] = $2
    next
}

## Process second file of arguments. Print header in first line and for
## the rest check if first field is found in the hash.
FNR < NR {
    if ( $1 in hash || FNR == 1 ) { 
        printf "%s %s\n", $0, ( FNR == 1 ? header : hash[ $1 ] ) 
    }   
}
