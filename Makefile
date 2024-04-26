PLATFORM = $(shell uname)
.PRECIOUS: %.s

PROJECT_NAME=Tylerd
PROJECT_TAG?=tylerd
PUBLIC_PROJECT=true
GITHUB_DOMAIN=github.com
GITHUB_TOKEN?=must be present on your env.mk, create in github at setting/user developer/external token with repo scope
GITHUB_PROJECT=gutomaia/TylerD
MAKEFILE_SCRIPT_PATH=extras/makefiles
MAKERY_REPOSITORY=gutomaia/makery
MAKERY_SCRIPT=gutonet.mk
MAKERY_DEFAULT_TASK=default_makery
MAKERY_BASE_URL=https://raw.githubusercontent.com/${MAKERY_REPOSITORY}/master

PYTHON_VERSION?=3.11
PYTHON_MODULES=tylerd
HTML_PATH=docs/_build/html
CFLAGS =-t nes -Oisr -g --include-dir neslib
CC = cl65

SRC = $(wildcard neslib/*.s)

OBJ = $(SRC:.c=.o)
OBJ := $(OBJ:.s=.o)

FCEUX = fceux
FCEUX_ARGS = --loadlua screenshot.lua


IMGS = $(wildcard assets/screens/*.png)
TILES := $(patsubst assets/screens/%.png,output/%_tiles.s,$(IMGS))
NES_FILES := $(patsubst assets/screens/%.png,output/%.nes,$(IMGS))
SCREENSHOTS := $(patsubst assets/screens/%.png,output/%_screenshot.png,$(IMGS))
EMULATED := $(patsubst assets/screens/%.png,output/%_emulated.png,$(IMGS))
DIFFS := $(patsubst assets/screens/%.png,output/%_diff.png,$(IMGS))


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

download:
	${VIRTUALENV} python scripts/download_assets.py assets/screens

%.o: %.c
	$(CC) -c $(CFLAGS) $< -o $@ --listing $<.lst

%.o: %.s
	$(CC) -c $(CFLAGS) $< -o $@ --listing $<.lst

output/%_tiles.s: assets/screens/%.png
	${VIRTUALENV} echo $@ |  sed 's|.*/\(.*\)_tiles\.s|\1|' | xargs -I [] echo tylerd -p nes -f 2bpp_metatiles -b [] $< -o $@
	${VIRTUALENV} echo $@ |  sed 's|.*/\(.*\)_tiles\.s|\1|' | xargs -I [] tylerd -p nes -f 2bpp_metatiles -b [] $< -o $@ && touch $@

output/%_game.c:
	${VIRTUALENV} echo $@ | sed 's|.*/\(.*\)_game\.c|\1|' | xargs -I [] python scripts/generate_source.py -o $@ -b []

output/%.nes: output/%_game.c nes.cfg $(OBJ) output/%_tiles.o
	@echo $@ | sed 's|.*/\(.*\)\.nes|\1|' | xargs -I [] $(CC) -o $@ -m $@.map $(CFLAGS) -C nes.cfg $< ${OBJ} output/[]_tiles.o

output/%_emulated.png: output/%_tiles.s
	${VIRTUALENV} python scripts/emulator_screen.py $< -o $@

output/%_screenshot.png: output/%.nes
	${FCEUX} $< ${FCEUX_ARGS}

output/%_diff.png: output/%_emulated.png
	${VIRTUALENV} echo $@ | sed 's|.*/\(.*\)_diff\.png|\1|' | xargs -I [] python scripts/compare.py assets/screens/[].png $< -o $@

nes: ${NES_FILES}

screenshots: ${SCREENSHOTS}

emulated: ${EMULATED}

diffs: ${DIFFS}

results: ${TILES} ${NES_FILES} ${SCREENSHOTS} ${EMULATED}

site: ${REQUIREMENTS_TEST}
	${VIRTUALENV} ghp-import -n -o -f -p $(HTML_PATH)
