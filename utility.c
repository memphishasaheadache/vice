#include "utility.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int categorizeFile(char *filename) {

	char *musicFiles[] = { "mp3", "wav", NULL };
	char *videoFiles[] = { "avi", "mpeg", "mpg", "divx", "xvid", NULL };
	char *dvdFiles[] = { "dvd://", NULL };

	int i = 0;
	char *ext;
	char *fileExt;

	while (NULL != musicFiles[i]) {
		ext = musicFiles[i];
		fileExt = filename + (strlen(filename)-strlen(ext));
		if (!strcasecmp(ext, fileExt)) {
			return MUSIC_FILE;
		}
		i++;
	}

	i = 0;

	while (NULL != videoFiles[i]) {
		ext = videoFiles[i];
		fileExt = filename + (strlen(filename)-strlen(ext));
		if (!strcasecmp(ext, fileExt)) {
			return VIDEO_FILE;
		}
		i++;
	}

	i = 0;

	while (NULL != dvdFiles[i]) {
		ext = videoFiles[i];
		if (!strncasecmp(ext, filename, strlen(ext))) {
			return DVD_FILE;
		}
		i++;
	}

	return UNKNOWN_FILE;
}
