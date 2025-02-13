#! /bin/bash

for f in $(find /lustre_xc50/ioper/models/SMNA-Oper/SMG/datainout/gsi/dataout -name fort.220)
do

  nf=$(echo $f | sed "s,ioper,carlos_bastarz/lucas,g")

  mkdir -p $(dirname $nf)

  cp -v $f $nf

done

exit 0
