#!/bin/bash

if [[ -n $SSH_ORIGINAL_COMMAND ]] # command given, so run it
then
	echo "`date` $SSH_ORIGINAL_COMMAND" >> /root/sshd.sh.log
	exec /bin/bash -c "$SSH_ORIGINAL_COMMAND"
else # no command, so interactive login shell
	echo "`date` Interactive login" >> /root/sshd.sh.log
	exec /bin/bash -il
fi
