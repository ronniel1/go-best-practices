files=$(find chapters -name "*.md" | sort)
readme=README.md

rm ${readme}

echo "# TOC" >> ${readme}

for chapter in ${files}
do
	echo "* [${chapter}](#${chapter})" >> ${readme}
done

echo "" >> ${readme}


for chapter in ${files}
do
	echo "
## ${chapter}
" >> ${readme}
	cat ${chapter} >> ${readme}
done

