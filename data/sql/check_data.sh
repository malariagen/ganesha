for j in *
do
  for i in `grep -A 1 '(' ${j} | grep -v ')' | grep -v '(' | grep , | grep -v double | grep -v text | grep -v int | sed -e 's/ //g'`
  do
	FILE=${j}
	HEAD=`echo $i | sed -e "s/${FILE}-//" -e 's/\`//g'`
	FILE2=`find ../Data -name "${FILE}"`
	if [ "${FILE2}" != "" -a -f "${FILE2}" -a ${FILE} != "images.csv" ]
	then
			HEAD2=`head -1 "${FILE2}"`
			HEAD3=`echo "${HEAD2}" | sed -e 's/\t/,/g' -e 's/#T//g'`
			if [ ${HEAD} != ${HEAD3} ]
			then
				echo "Column mismatch between ${FILE} and ${FILE2}"
				echo "###"${HEAD}"###"
				echo "###"${HEAD3}"###"
			fi
	fi
  done
done
