#!/bin/bash
set -e

{
    docker compose exec django sh /check.sh
} || {
    docker-compose exec django sh /check.sh
}