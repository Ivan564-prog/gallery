.PHONY: up down start stop restart destroy build logs ps sh manage check makemigrations migrate shell dbshell collectstatic changepassword

RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))


THIS_FILE := $(lastword $(MAKEFILE_LIST))

# Defining the user's UID and GID. It is used to avoid file permission issues
UID := $(shell id -u)
GID := $(shell id -g)


# Avoiding issue with "docker compose" and "docker-compose" by checking which one is used in the system
DOCKER_COMPOSE := $(shell command -v docker-compose 2> /dev/null || echo docker compose)

# Sometimes this file is called "docker-compose.yml" and Sometimes "docker-compose.yaml", this line sets which one is gonna be used
COMPOSE_FILE := $(if $(wildcard docker-compose.yaml),docker-compose.yaml,docker-compose.yml)

# Generic targets
help:
	@make -pRrq  -f $(THIS_FILE) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

# Docker Compose
up:
	UID=$(UID) GID=$(GID)	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) up -d $(RUN_ARGS)
down:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) down $(RUN_ARGS)
start:
	UID=$(UID) GID=$(GID)	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) start $(RUN_ARGS)
stop:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) stop $(RUN_ARGS)
restart:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) stop $(RUN_ARGS)
	UID=$(UID) GID=$(GID)	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) up -d $(RUN_ARGS)
destroy:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) down -v $(RUN_ARGS)
build:
	UID=$(UID) GID=$(GID)	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) build $(RUN_ARGS)
exec:
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec $(RUN_ARGS)
logs:
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) logs -f $(RUN_ARGS)
ps:
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) ps $(RUN_ARGS)
sh:
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec $(RUN_ARGS) sh -c 'if command -v bash &> /dev/null; then bash; else sh; fi'


# Django 
DJANGO_CONTAINER_NAME := "django"
manage:
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec $(DJANGO_CONTAINER_NAME) python3 manage.py $(RUN_ARGS)
check:
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec $(DJANGO_CONTAINER_NAME) python3 manage.py check $(RUN_ARGS)
makemigrations:
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec $(DJANGO_CONTAINER_NAME) python3 manage.py makemigrations $(RUN_ARGS)
migrate:
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec $(DJANGO_CONTAINER_NAME) python3 manage.py migrate $(RUN_ARGS)
shell:
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec $(DJANGO_CONTAINER_NAME) python3 manage.py shell $(RUN_ARGS)
dbshell:
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec $(DJANGO_CONTAINER_NAME) python3 manage.py dbshell $(RUN_ARGS)
collectstatic:
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec $(DJANGO_CONTAINER_NAME) python3 manage.py collectstatic $(RUN_ARGS)
createsuperuser:
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec $(DJANGO_CONTAINER_NAME) python3 manage.py createsuperuser $(RUN_ARGS)
changepassword:
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec $(DJANGO_CONTAINER_NAME) python3 manage.py changepassword $(RUN_ARGS)


# Overriding targets other then the first one, so we could use targets as positional arguments (e.g: make manage check)
$(RUN_ARGS):
	@:
