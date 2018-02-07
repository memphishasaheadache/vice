C_FILES=vice.c menu.c config.c utility.c playlist.c
O_FILES=vice.o menu.o config.o utility.o playlist.o
LIBS=-L/usr/X11R6/lib -lX11 -lm
PACKAGE_CFLAGS=`pkg-config --cflags --libs libxine gtk+-2.0 gthread-2.0`
CFLAGS=-Wall -ggdb -O2 ${PACKAGE_CFLAGS}
OUT_FILE=vice

.c.obj:
	gcc ${COMPILE_OPTIONS} -c ${CFLAGS} ${PACKAGE_CFLAGS} ${LIBS} ${C_FILES}
all: ${O_FILES}
	gcc ${COMPILE_OPTIONS} ${CFLAGS} ${PACKAGE_CFLAGS} ${LIBS} -o ${OUT_FILE} ${O_FILES}
clean:
	rm ${OUT_FILE} *.o
