#!/bin/sh

WORK_DIR="/data/webapp/m1-stable-diffusion-webui"
NAME="sd-webui"
CMD="/data/envs/sd/bin/python ${WORK_DIR}/manage_pro.py"
TIMEOUT_CMD="/bin/timeout"


function safeRun() {
    fullCmd="[$*]"
    file="/tmp/${NAME}_$1.lock"

    (
        flock -xn -w 10 200 || exit 1
        start_time=`date +%s`
        echo "Run ${fullCmd} at `date`"
        #${TIMEOUT_CMD} 72000 ${CMD} $*
        ${CMD} $*
        ret=$?
        end_time=`date +%s`
        echo "Done ${fullCmd}. Spend `expr $end_time - $start_time` s"
        return $ret
    ) 200>${file}

}

safeRun $*
