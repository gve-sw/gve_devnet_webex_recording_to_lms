#!/bin/sh

export PYTHONPATH=/usr/local/lib/python3.8/site-packages
export PATH=/usr/local/lib/python3.8/site-packages/numpy/.libs:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
export KUBERNETES_SERVICE_PORT_HTTPS=443
export UWSGI_CHEAPER=2
export KUBERNETES_SERVICE_PORT=443
export no_proxy=localhost,127.0.0.1,10.96.0.1,cole
export HOSTNAME=cole-9675b4f49-xz6bz
export PYTHON_VERSION=3.8.2
export COLE_PORT=tcp://10.96.7.12:8090
export WEBEX_TOKEN=OTdkYWU4NTctYTJhMy00Yzg4LWI2ODgtOWM4OWU1MTQ5ZGMxMjYwMmVlZjMtMzAz_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f
export WEBEX_REFRESH_TOKEN=ZGY2YjQ2NjAtOTkyNC00OWQ0LWExYTMtMjEzODc1Y2ZiNzQwNTE5ODE4ODQtYmUz_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f
export NGINX_MAX_UPLOAD=0
export COLE_PORT_8090_TCP_PORT=8090
export STATIC_PATH=/app/static
export PWD=/app
export WEBEX_BOT_TOKEN=MTI3NDFhZTEtMDA3My00N2ZhLWFlNWQtNTkwZTkyN2EzMjg1NGI2NWQ4MDctZDI1_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f
export HOME=/root
export LANG=C.UTF-8
export KUBERNETES_PORT_443_TCP=tcp://10.96.0.1:443
export LISTEN_PORT=80
export GPG_KEY=E3FF2839C048B25C084DEBE9B26995E310250568
export https_proxy=http://proxy-wsa.esl.cisco.com:80/
export COLE_PORT_8090_TCP=tcp://10.96.7.12:8090
export COLE_ACCESS_TOKEN=9881~0i08XTt7tTLPBBUFXtOeLdVSs72lPmXm4G2KeXKyINu6tygrL9O3R3bytg5Lu3mM
export COLE_PORT_8090_TCP_ADDR=10.96.7.12
export TERM=xterm
export COLE_SERVICE_PORT=8090
export COLE_URL=https://ciscoacademy.instructure.com:443/api/v1/courses/891/pages/Recording_Test
export SHLVL=1
export KUBERNETES_PORT_443_TCP_PROTO=tcp
export COLE_SERVICE_PORT_8090=8090
export PYTHON_PIP_VERSION=20.1
export http_proxy=http://proxy-wsa.esl.cisco.com:80/
export KUBERNETES_PORT_443_TCP_ADDR=10.96.0.1
export PYTHON_GET_PIP_SHA256=ce486cddac44e99496a702aa5c06c5028414ef48fdfd5242cd2fe559b13d4348
export NGINX_WORKER_PROCESSES=1
export UWSGI_INI=/app/uwsgi.ini
export WEBEX_NOTIFIER_TOKEN=ZmI5NGE1ZGUtMDk1Ny00NWRiLWJhY2MtYWZhZmY0M2I4NDU1NzRlNDhiZjItZmIw_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f
export KUBERNETES_SERVICE_HOST=10.96.0.1
export COLE_SERVICE_HOST=10.96.7.12
export KUBERNETES_PORT=tcp://10.96.0.1:443
export KUBERNETES_PORT_443_TCP_PORT=443
export PYTHON_GET_PIP_URL=https://github.com/pypa/get-pip/raw/1fe530e9e3d800be94e04f6428460fc4fb94f5a9/get-pip.py
export STATIC_INDEX=1
export UWSGI_PROCESSES=16
export STATIC_URL=/static
export COLE_PORT_8090_TCP_PROTO=tcp

python3 /app/cronscript.py