#!/bin/bash

brew_cmd () {
    if type "boost" > /dev/null 2>&1
    then
        echo "boost is already installed"
    else
        brew install boost
    fi
}

juman_install () {
    export CPATH=$CPATH:/usr/local/Cellar/boost/1.64.0_1/include
    export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/Cellar/boost/1.64.0_1/lib

    # Juman Install
    wget http://lotus.kuee.kyoto-u.ac.jp/nl-resource/jumanpp/jumanpp-1.01.tar.xz
    tar xJvf jumanpp-1.01.tar.xz
    cd jumanpp-1.01
    ./configure
    make
    make install

    # PyKnp Install
    wget http://nlp.ist.i.kyoto-u.ac.jp/nl-resource/knp/pyknp-0.3.tar.gz
    tar xvf pyknp-0.3.tar.gz
    cd pyknp-0.3
    sudo python setup.py install
}

if type "brew" > /dev/null 2>&1
then
    if type "pip" > /dev/null 2>&1
    then
        brew_cmd
        juman_install
        pip install -r requirements.txt
    else
        echo "no command: pip"
    fi
else
    echo "no command: brew"
fi
