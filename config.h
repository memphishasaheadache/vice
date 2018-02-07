#define EXIT_SCREEN_QUERY 0x8
#define EXIT_DISPLAY_QUERY 0x10

struct _config {
	GdkDisplay *display;
	GdkScreen *screen;
	int screenWidth;
	int screenHeight;
	double aspectRatio;
	char *dvdStore;
	char *movieStore;
	char *musicStore;
	char *dvdDevice;
	int fontSize;
	double menuWidth;
} config;

int configExit(int exitCode, char *exitString);
int initConfig(void);
