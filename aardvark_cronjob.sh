#!/bin/bash
export AARDVARK_ACCOUNTS
export DATADOG_SECRET


python /tmp/aardvark/dd_event.py start
# redirect to stdout of pid 1, which in our case (docker) will cause the output to be visible for docker logs
/usr/local/bin/aardvark update -a AARDVARK_ACCOUNTS >> /proc/1/fd/1
python /tmp/aardvark/dd_event.py end
