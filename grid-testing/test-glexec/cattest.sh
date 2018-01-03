#!/bin/bash
NEWFILE=./new-payload.sh
echo "Start"
cat > $NEWFILE <<'EOF'
#!/bin/bash
echo "****************************************"
date
whoami
id
hostname
pwd
env | sort
echo "*****************************************"
EOF

chmod +x ./new-payload.sh

echo "Done."
./new-payload.sh
