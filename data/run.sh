. ./config.sh
rm -rf Data
python getFiles.py
SQLDIR=${PWD}/sql
(cd Data
 python ../convert-xlsx-to-csv.py sample_contexts.xlsx
)
(cd Data
for i in *.csv *.tab Population\ genetics\ data/* Miscellaneous/*
do
	DIR=`echo $i | sed -e 's/.zip//'`
	if [ "${DIR}" = "$i" ]
	then
		BASE=`basename "$i"`
		LOAD=${PWD}/../sql/${BASE}
		if [ -f "${LOAD}" ]
		then
			PDIR=`dirname "$i"`
			(cd "${PDIR}"
			fromdos ${BASE}
mysql --local-infile=1 -u ${DBUSER} -p${DBPASS} ${DB} < ${SQLDIR}/${BASE}
			)
			if [ $? -ne 0 ]
			then
				echo "Error loading:"${i}
			fi
		fi
	else
		rm -rf ${DIR}
		mkdir ${DIR}
		cd ${DIR}
		unzip ../$i
		for j in *
		do
			LOAD=../../../sql/${DIR}#$j
			if [ -f ${LOAD} ]
			then
mysql --local-infile=1 -u ${DBUSER} -p${DBPASS} ${DB} < ${LOAD}
			fi
		done
		cd ..
	fi
done
)
for i in ${SQLDIR}/*.sql
do
	echo $i
	mysql -u ${DBUSER} -p${DBPASS} ${DB} < ${i}
	if [ $? -ne 0 ]
	then
		echo "Error loading:"${i}
	fi
done
