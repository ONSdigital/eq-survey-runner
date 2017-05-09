#!/bin/bash

shred -u -v secure-data.tar

shred -u -v secure-data/*
rm -rf secure-data

shred -u -v $Keys
rm -f $Keys

shred -u -v key_mat/*
rm -rf key_mat
