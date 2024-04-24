PLATFORM = $(shell uname)

PROJECT_NAME=tyler
PROJECT_TAG?=tyler
PUBLIC_PROJECT=true
GITHUB_DOMAIN=github.com
GITHUB_TOKEN?=must be present on your env.mk, create in github at setting/user developer/external token with repo scope
GITHUB_PROJECT=gutomaia/tyler
MAKEFILE_SCRIPT_PATH=extras/makefiles
MAKERY_REPOSITORY=gutomaia/makery
MAKERY_SCRIPT=gutonet.mk
MAKERY_DEFAULT_TASK=default_makery
MAKERY_BASE_URL=https://raw.githubusercontent.com/${MAKERY_REPOSITORY}/master

PYTHON_VERSION?=3.11
PYTHON_MODULES=tyler

CFLAGS =-t nes -Oisr -g --include-dir neslib
CC = cl65

SRC = $(wildcard neslib/*.s)

OBJ = $(SRC:.c=.o)
OBJ := $(OBJ:.s=.o)

FCEUX = fceux


WGET=wget -q
ifeq "true" "${PUBLIC_PROJECT}"
GH_WGET=${WGET}
else
GH_WGET=${WGET} --header "Authorization: token ${GITHUB_TOKEN}"
endif

ifeq "" "$(shell which wget)"
WGET=curl -O -s -L -s
ifeq "true" "${PUBLIC_PROJECT}"
GH_WGET=${WGET}
else
GH_WGET=${WGET} -H "Authorization: token ${GITHUB_TOKEN}"
endif
endif

OK=\033[32m[OK]\033[39m
FAIL=\033[31m[FAIL]\033[39m
CHECK=@if [ $$? -eq 0 ]; then echo "${OK}"; else echo "${FAIL}" ; fi


ifeq "true" "${shell test -f ~/env.mk && echo true}"
include ~/env.mk
HASENV=true
endif


ifeq "true" "${shell test -f env.mk && echo true}"
include env.mk
HASENV=true
endif

ifneq "true" "${HASENV}"
$(shell echo "# Generated file env.mk" > env.mk)
$(shell echo "GITHUB_TOKEN=" > env.mk)
endif

ifeq "" "${GITHUB_TOKEN}"
default:
	echo ${GITHUB_TOKEN} ${shell test -f ~/env.mk && echo true}
	@echo "You must create a GITHUB_TOKEN var in your env.mk file"
	@echo "Create a token with REPO permissions and set as GITHUB_TOKEN in your env.mk"
	@echo "Go to https://github.com/settings/tokens (y/N)?" && read ans && [ $${ans:-N} = y ]
	@open https://github.com/settings/tokens
	@exit 1
else
default: ${MAKEFILE_SCRIPT_PATH}/${MAKERY_SCRIPT}
	@$(MAKE) -C . ${MAKERY_DEFAULT_TASK}
endif

ifeq "true" "${shell test -f ${MAKEFILE_SCRIPT_PATH}/${MAKERY_SCRIPT} && echo true}"
include ${MAKEFILE_SCRIPT_PATH}/${MAKERY_SCRIPT}
endif

${MAKEFILE_SCRIPT_PATH}/${MAKERY_SCRIPT}:
	@echo "Download ${MAKERY_SCRIPT} at extras/makefiles: \c"
	@mkdir -p ${MAKEFILE_SCRIPT_PATH} && \
		cd ${MAKEFILE_SCRIPT_PATH} && \
		${GH_WGET} ${MAKERY_BASE_URL}/${MAKERY_SCRIPT} && \
		touch ${MAKERY_SCRIPT}
	${CHECK}

neslib/Makefile:
	git submodule update --init --recursive

neslib/Makefile.out: neslib/Makefile
	cd neslib && sed 's/$$(CC65DIR)\/bin\///g' Makefile > Makefile.out

neslib/neslib2.lib: neslib/Makefile.out
	$(MAKE) -C neslib -f Makefile.out neslib2.lib && touch $@

%.o: %.c
	$(CC) -c $(CFLAGS) $< -o $@ --listing $<.lst

%.o: %.s
	$(CC) -c $(CFLAGS) $< -o $@ --listing $<.lst

output/%_tiles.s: assets/screens/%_nes_title.png
	${VIRTUALENV} tyler import_image $< -o $@ -b $@
	touch $@

output/%.nes: assets/sources/%.c $(OBJ) output/%_tiles.o
	$(CC) -o $@ -m $@.map $(CFLAGS) -C nes.cfg $<

mario: output/mario.nes
	${FCEUX} $<

bionic: output/bionic.nes
	${FCEUX} $<

castlevania: output/castlevania.nes
	${FCEUX} $<

megaman: output/megaman.nes
	${FCEUX} $<

batman: output/batman.nes
	${FCEUX} $<

title: output/title.nes
	${FCEUX} $< 

gameover: output/gameover.nes
	${FCEUX} $<

assets2: output/mario.nes \
	output/castlevania.nes \
	output/megaman.nes \
	output/batman.nes

assets: output/castlevania.nes

.PHONY: castlevania_tiles.s batman_tiles.s title_tiles.s gameover_tiles.s bionic_tiles.s
