struct _playlistItem {
	char *location;
	int type;
	struct _playlistItem *nextItem;
	struct _playlistItem *prevItem;
	struct _playlist *playlist;
};

struct _playlist {
	unsigned int count;
	struct _playlistItem *firstItem;
	struct _playlistItem *lastItem;
	struct _playlistItem *currItem;
};

struct _playlist *createPlaylist(void);
int freePlaylist(struct _playlist *playlist);
struct _playlistItem *createPlaylistItem(char *file);
int appendToList(struct _playlist *list, char *file);
int destroyPlaylistItem(struct _playlistItem *item);
int _destroyPlaylistItem(struct _playlistItem *item);
void printPlaylist(struct _playlist *list);
