#!/bin/bash
set -e

curl -dH -X POST "$(terraform output -raw webhook_url)"