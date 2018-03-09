#!/bin/bash

if [ "$1" = "install" ]
then
  echo "Installing python modules..."
  for i in imapclient pick pyzmail; do
    pip install "$i"
  done
fi
if [ "$1" = "view" ]
then
  echo "The following are the python modules needed to run Message2.py"
  for i in imapclient pick pyzmail; do
    echo "$i"
  done
fi
