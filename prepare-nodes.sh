#!/bin/sh
ANSIBLE_CONFIG="pipelining = False" ansible-playbook -i hosts prepare-nodes.yml
