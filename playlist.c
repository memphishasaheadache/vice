#include <stdlib.h>
#include "playlist.h"
#include "utility.h"

struct _playlist *createPlaylist(void) {

	struct _playlist *newPlaylist;

	newPlaylist = (struct _playlist *)malloc(sizeof(struct _playlist));
	newPlaylist->count = 0;
	newPlaylist->firstItem = NULL;
	newPlaylist->lastItem = NULL;
	newPlaylist->currItem = NULL;

	return newPlaylist;
}

int freePlaylist(struct _playlist *playlist) {

	struct _playlistItem *item;

	// First remove all items
	while (NULL != (item = playlist->firstItem)) {
		destroyPlaylistItem(item);
	}

	// Second destroy the list itself
	free(playlist);
	return 0;
}

struct _playlistItem *createPlaylistItem(char *file) {

	struct _playlistItem *newItem = NULL;
	int category = 0;

	category = categorizeFile(file);
	if (UNKNOWN_FILE == category) {
		return NULL;
	}

	newItem = (struct _playlistItem *)malloc(sizeof(struct _playlistItem));
	newItem->location = (char *)g_strdup(file);
	newItem->type = category;
	newItem->nextItem = NULL;
	newItem->prevItem = NULL;

	return newItem;
}

int appendToList(struct _playlist *list, char *file) {

	struct _playlistItem *newItem = NULL;

	if (NULL != (newItem = createPlaylistItem(file))) {
		newItem->playlist = list;
		newItem->prevItem = list->lastItem;
		newItem->nextItem = NULL;
		list->count++;

		if (NULL != list->lastItem) {
			list->lastItem->nextItem = newItem;
		} else {
			list->firstItem = newItem;
		}
		list->lastItem = newItem;
	}

	return 0;
}

int destroyPlaylistItem(struct _playlistItem *item) {

	struct _playlistItem *next, *prev;
	struct _playlist *list;

	next = item->prevItem;
	prev = item->nextItem;
	list = item->playlist;
	list->count--;

	// Reconcile current item pointer
	if (list->currItem == item) {
		if (NULL != next) {
			list->currItem = next;
		} else if (NULL != prev) {
			list->currItem = prev;
		} else {
			list->currItem = NULL;
		}
	}

	// Reconcile last pointer
	if (item == list->lastItem) {
		list->lastItem = prev;
	}

	// Reconcile first pointer
	if (item == list->firstItem) {
		list->firstItem = next;
	}


	if (NULL != next) {
		next->prevItem = prev;
	}

	if (NULL != prev) {
		prev->nextItem = next;
	}

	_destroyPlaylistItem(item);
	return 0;

}

int _destroyPlaylistItem(struct _playlistItem *item) {

	free(item->location);
	free(item);
	return 0;

}

void printPlaylist(struct _playlist *list) {

	struct _playlistItem *item = NULL;

	printf("Total items: %d\n", list->count);

	item = list->firstItem;
	while (NULL != item) {
		printf("Type: %d\n", item->type);
		printf("Location: %s\n", item->location);
		printf("\n");
		item = item->nextItem;
	}

}
