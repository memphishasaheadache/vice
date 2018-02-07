#include <gtk/gtk.h>
#include <gdk/gdk.h>
#include "config.h"

int configExit(int exitCode, char *exitString) {
	fprintf(stdout, "%s\n", exitString);
	exit(exitCode);
}

int initConfig(void) {

	if (NULL == (config.screen = gdk_screen_get_default())) {
		configExit(EXIT_SCREEN_QUERY, "Unable to query default screen");
	}
	if (NULL == (config.display = gdk_screen_get_display(config.screen))) {
		configExit(EXIT_DISPLAY_QUERY, "Unable to query display");
	}
	config.screenWidth = gdk_screen_get_width(config.screen);
	config.screenHeight = gdk_screen_get_height(config.screen);

	config.aspectRatio = (double)config.screenWidth/(double)config.screenHeight;

	//FIXXIF: Should be queried from sqllite

	config.movieStore = (char *)g_strdup("/store/dvds");
	config.musicStore = (char *)g_strdup("/mp3");
	config.dvdDevice = (char *)g_strdup("/dev/dvd1");
	config.dvdStore = (char *)malloc(strlen(config.dvdDevice) + strlen("dvd://"));
	g_sprintf(config.dvdStore, "dvd://%s", config.dvdDevice);
	config.fontSize = 18;
	config.menuWidth = 0.30;

	return 0;
}
