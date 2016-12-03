#!/bin/bash
MPC="/usr/bin/mpc"
ALBUM_TITLE=$1

$MPC clear
#$MPC findadd ALBUM_TITLE ${ALBUM_TITLE}
$MPC search album "$ALBUM_TITLE" | $MPC add
$MPC play
