#!/bin/bash
MPC="/usr/bin/mpc"
$MPC repeat on
$MPC clear 
$MPC load $1
$MPC play

