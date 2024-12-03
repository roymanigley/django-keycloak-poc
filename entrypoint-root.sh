#!/bin/sh
crond
exec su-exec app-user "$@"