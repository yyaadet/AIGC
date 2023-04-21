#!/bin/sh

PIP="/data/envs/sd/bin/pip"
PY="/data/envs/sd/bin/python"

HOSTS="61.160.198.62"


function install_python() {
    for h in ${HOSTS}
    do
        echo "Host ${h}"
ssh -t -i ~/Documents/gitroom/devops/deploy/id_rsa root@${h} <<EOF
            sudo yum install -y gcc openssl-devel bzip2-devel libffi-devel git make gcc wget sqlite-devel && \
            cd /root && \
            tar zxf Python-3.9.16.tgz && \
            cd Python-3.9.16 && \
            ./configure --enable-optimizations --prefix=/usr/local/python39 --with-ensurepip=install && \
            sudo make clean install && \
            mkdir /data/envs && \
            /usr/local/python39/bin/pip install virtualenv && \
            /usr/local/python39/bin/virtualenv /data/envs/sd
EOF
    done
}


function install_source() {
    for h in ${HOSTS}
    do
        echo "Host ${h}"
ssh -t -i ~/Documents/gitroom/devops/deploy/id_rsa root@${h} <<EOF
            cd /data/webapp
            git clone https://github.com/yyaadet/m1-stable-diffusion-webui.git

            cd m1-stable-diffusion-webui && \
            /data/envs/sd/bin/pip install -r requirements.txt && \
            cd stable_diffusion_webui && \
            useradd sd && \
            sudo -u sd /data/envs/sd/bin/python manage_pro.py download_models

EOF
    done
}


install_nginx() {
    sudo yum install -y epel-release && \
    sudo yum install -y nginx
}


case $1 in
python)
    install_python
;;
source)
    install_source
;;
*)
    echo "Usage: ./remote_install.sh python"
;;
esac
