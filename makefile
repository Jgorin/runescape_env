.SILENT: run
MKFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
MKFILE_DIR := $(dir $(MKFILE_PATH))

build:
	@cd ${MKFILE_DIR} && docker build . -t rs_docker -f dockerfile
run:
	@xhost +
	@docker run -it --rm --name rs_docker -e DISPLAY=${DISPLAY} -v ${MKFILE_DIR}/runescape_parser:/root/runescape_parser -v /tmp/.X11-unix:/tmp/.X11-unix rs_docker:latest /bin/bash
	@xhost - 