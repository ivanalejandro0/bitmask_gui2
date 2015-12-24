#!/bin/bash
# thanks to: https://gist.github.com/2042882

if [[ -z $1 ]]; then
    echo "You need to specify a python3 virtualenv path parameter."
    echo "You should NOT be sourced inside that venv"
fi

# This script can be used as a hook, run after a new virtualenv is activated.
# ~/.virtualenvs/postmkvirtualenv
 
# libs=( PyQt4 sip.so )
# if PyQt4 is compiled with 'kde' flag, needs the PyKDE4 lib
libs=( PyQt5 sip.cpython-34m-x86_64-linux-gnu.so )
 
# python_version=python$(python3 -c "import sys; print (str(sys.version_info[0])+'.'+str(sys.version_info[1]))")
# var=( $(which -a $python_version) )
#  
get_python_lib_cmd="from distutils.sysconfig import get_python_lib; print (get_python_lib())"
# lib_system_path=$(${var[-1]} -c "$get_python_lib_cmd")
lib_system_path=$(python3 -c "$get_python_lib_cmd")

source $1/bin/activate
lib_virtualenv_path=$(python3 -c "$get_python_lib_cmd")
 
for lib in ${libs[@]}
do
    ln -s $lib_system_path/$lib $lib_virtualenv_path/$lib
done
