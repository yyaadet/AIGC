#!/bin/sh

PIP="/data/envs/sd/bin/pip"
PY="/data/envs/sd/bin/python"


function python_libs() {
    ${PIP} install -r requirements.txt

    ${PY} -c "import nltk;nltk.download('wordnet');nltk.download('stopwords');nltk.download('omw-1.4');nltk.download('punkt');nltk.download('words')"

    #${PY} -m spacy download en_core_web_sm
    #${PY} -m spacy download en_core_web_lg
    ${PY} -m spacy download en_core_web_trf
}


function python_bins() {
    cd /home/aminer && \
    tar zxf Python-3.9.16.tgz && \
    cd Python-3.9.16 && \
    ./configure --enable-optimizations --prefix=/usr/local/python39 && \
    make && \
    make install && \
    mkdir /data/envs && \
    /usr/local/python39/bin/virtualenv /data/envs/rms
}

function system_bins() {
    sudo yum install -y git
    sudo yum install -y wget
}


function upload_python() {
    hosts=`seq 49 57`
    for h in $hosts
    do
        ssh -i ~/Documents/gitroom/devops/deploy/id_rsa aminer@192.168.0.${h} "sudo hostname ${h} && sudo echo '${h}' > /etc/hostname"
    done
    #for h in $hosts
    #do
    #    scp -i ~/Documents/gitroom/devops/deploy/id_rsa ~/Downloads/Python-3.9.16.tar aminer@192.168.0.${h}:/home/aminer
    #done
}

function remote_install() {
    hosts="54"
    for h in $hosts
    do
        echo "Host ${h}"
ssh -t -i ~/Documents/gitroom/devops/deploy/id_rsa aminer@192.168.0.${h} <<EOF
            sudo yum install -y gcc openssl-devel bzip2-devel libffi-devel && \
            cd /home/aminer && \
            tar zxf Python-3.9.16.tgz && \
            cd Python-3.9.16 && \
            ./configure --enable-optimizations --prefix=/usr/local/python39 --with-ensurepip=install && \
            sudo make clean install && \
            mkdir /data/envs && \
            /usr/local/python39/bin/pip install virtualenv && \
            /usr/local/python39/bin/virtualenv /data/envs/rms
EOF
    done
}

case $1 in
upload)
    upload_python
;;
install)
    #python_bins
    python_libs
;;
remote)
    remote_install
;;
*)
    echo "Usage: ./install.sh upload|install"
;;
esac
