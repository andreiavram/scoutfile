#/bin/bash

ssh gatekeeper "mysqldump -pme11on_ -uroot scoutfile3_base > /home/yeti/dmp.sql"
scp gatekeeper:dmp.sql .
ssh gatekeeper "rm -rf /home/yeti/dmp.sql"

mysqldump -psql123. -uroot scoutfile3_base --add-drop-table --no-data | grep ^DROP > ./tmp.sql

sed -i '1s/^/SET FOREIGN_KEY_CHECKS = 0;\n/' ./tmp.sql
sed -i '1s/$/SET FOREIGN_KEY_CHECKS = 1;\n/' ./tmp.sql
 
mysql -psql123. -uroot scoutfile3_base < ./tmp.sql
mysql -psql123. -uroot scoutfile3_base < ./dmp.sql

rm -rf tmp.sql
rm -rf dmp.sql
