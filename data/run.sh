. ./config.sh
rm -rf Population\ genetics\ data/
python getFiles.py
cd Population\ genetics\ data/
for i in *
do
	DIR=`echo $i | sed -e 's/.zip//'`
	if [ ${DIR} = $i ]
	then
		LOAD=../sql/$i
		if [ -f ${LOAD} ]
		then
mysql --local-infile=1 -u ${DBUSER} -p${DBPASS} ${DB} < ${LOAD}
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
			LOAD=../../sql/${DIR}#$j
			if [ -f ${LOAD} ]
			then
mysql --local-infile=1 -u ${DBUSER} -p${DBPASS} ${DB} < ${LOAD}
			fi
		done
		cd ..
	fi
done
cd ..
for i in sql/*.sql
do
	echo $i
	mysql -u ${DBUSER} -p${DBPASS} ${DB} < ${i}
	if [ $? -ne 0 ]
	then
		echo "Error loading:"${i}
	fi
done
