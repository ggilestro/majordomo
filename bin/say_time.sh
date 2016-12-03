#!/bin/bash
TIME=`date +"%H e %M minuti"`
TEXT="Sono le ore ${TIME}"
TOGGLE="/opt/majordomo/bin/mpc_toggle.sh"
SAY_CMD="/opt/majordomo/bin/say"

$TOGGLE
$SAY_CMD -l IT -s "${TEXT}"
$TOGGLE
