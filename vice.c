/*
** Copyright (C) 2003 Daniel Caujolle-Bert <segfault@club-internet.fr>
**	
** This program is free software; you can redistribute it and/or modify
** it under the terms of the GNU General Public License as published by
** the Free Software Foundation; either version 2 of the License, or
** (at your option) any later version.
**	
** This program is distributed in the hope that it will be useful,
** but WITHOUT ANY WARRANTY; without even the implied warranty of
** MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
** GNU General Public License for more details.
**	
** You should have received a copy of the GNU General Public License
** along with this program; if not, write to the Free Software
** Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
**	
* $Id: muxine.c,v 1.4 2005/09/12 00:47:03 miguelfreitas Exp $
*/
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <math.h>
#include <sys/time.h>

#include <glib.h>
#include <pthread.h>
#include <gdk/gdk.h>

#include <X11/X.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>

#include <xine.h>
#include <xine/xineutils.h>

#include "menu.h"
#include "config.h"
#include "playlist.h"

static xine_t *xine;
static xine_stream_t *stream;
static xine_video_port_t *vo_port;
static xine_audio_port_t *ao_port;
static xine_event_queue_t *event_queue;

static Display *display;
static int screen;
static Window window;
static int xpos, ypos, width, height;
static double pixel_aspect;
static int running = 0;

extern struct _config config;
GtkWidget *menuWindow;

#define INPUT_MOTION (ExposureMask | ButtonPressMask | KeyPressMask | \
											ButtonMotionMask | StructureNotifyMask |				\
											PropertyChangeMask | PointerMotionMask)

static void dest_size_cb(void *data, int video_width, int video_height, double video_pixel_aspect,
			 int *dest_width, int *dest_height, double *dest_pixel_aspect)	{

	*dest_width				= width;
	*dest_height			 = height;
	*dest_pixel_aspect = pixel_aspect;
}

static void frame_output_cb(void *data, int video_width, int video_height,
					double video_pixel_aspect, int *dest_x, int *dest_y,
					int *dest_width, int *dest_height, 
					double *dest_pixel_aspect, int *win_x, int *win_y) {
	*dest_x						= 0;
	*dest_y						= 0;
	*win_x						 = xpos;
	*win_y						 = ypos;
	*dest_width				= width;
	*dest_height			 = height;
	*dest_pixel_aspect = pixel_aspect;
}

static void event_listener(void *user_data, const xine_event_t *event) {
	switch(event->type) { 
	case XINE_EVENT_UI_PLAYBACK_FINISHED:
		running = 0;
		break;
	}
}

void *xinePlay(char **file) {
	char configfile[2048];
	x11_visual_t vis;
	double res_h, res_v;
	char *vo_driver = "auto";
	char *ao_driver = "auto";
	char  *mrl = NULL;

	mrl = file;

	if (!XInitThreads()) {
		printf("XInitThreads() failed\n");
		return NULL;
	}

	xine = xine_new();
	sprintf(configfile, "%s%s", xine_get_homedir(), "/.xine/config");
	xine_config_load(xine, configfile);
	xine_init(xine);
 
	if((display = XOpenDisplay(getenv("DISPLAY"))) == NULL) {
		printf("XOpenDisplay() failed.\n");
		return NULL;
	}
		
	screen = XDefaultScreen(display);
	xpos = 0;
	ypos = 0;
	width = 320;
	height = 200;

	XLockDisplay(display);
	window = XCreateSimpleWindow(display, XDefaultRootWindow(display),
		xpos, ypos, width, height, 1, 0, 0);
	
	XSelectInput (display, window, INPUT_MOTION);

	XMapRaised(display, window);
	
	res_h = (DisplayWidth(display, screen) * 1000 / DisplayWidthMM(display, screen));
	res_v = (DisplayHeight(display, screen) * 1000 / DisplayHeightMM(display, screen));
	XSync(display, False);
	XUnlockDisplay(display);

	vis.display	= display;
	vis.screen = screen;
	vis.d = window;
	vis.dest_size_cb = dest_size_cb;
	vis.frame_output_cb = frame_output_cb;
	vis.user_data = NULL;
	pixel_aspect = res_v / res_h;

	if(fabs(pixel_aspect - 1.0) < 0.01) {
		pixel_aspect = 1.0;
	}
	
	if((vo_port = xine_open_video_driver(xine, 
		vo_driver, XINE_VISUAL_TYPE_X11, (void *) &vis)) == NULL) {
		printf("I'm unable to initialize '%s' video driver. Giving up.\n", vo_driver);
		return NULL;
	}

	ao_port = xine_open_audio_driver(xine , ao_driver, NULL);
	stream = xine_stream_new(xine, ao_port, vo_port);
	event_queue = xine_event_new_queue(stream);
	xine_event_create_listener_thread(event_queue, event_listener, NULL);

	xine_gui_send_vo_data(stream, XINE_GUI_SEND_DRAWABLE_CHANGED, (void *) window);
	xine_gui_send_vo_data(stream, XINE_GUI_SEND_VIDEOWIN_VISIBLE, (void *) 1);

	if((!xine_open(stream, mrl)) || (!xine_play(stream, 0, 0))) {
		printf("Unable to open mrl '%s'\n", mrl);
		return NULL;
	}

	running = 1;

	while(running) {
		XEvent xevent;
		int got_event;

		XLockDisplay(display);
		got_event = XPending(display);
		if( got_event ) {
			XNextEvent(display, &xevent);
		}
		XUnlockDisplay(display);
		
		if( !got_event ) {
			xine_usec_sleep(20000);
			continue;
		}

		switch(xevent.type) {

		case Expose:
			if(xevent.xexpose.count != 0) {
				break;
			}
			xine_gui_send_vo_data(stream, XINE_GUI_SEND_EXPOSE_EVENT, &xevent);
			break;
			
		case ConfigureNotify:
			{
				XConfigureEvent *cev = (XConfigureEvent *) &xevent;
				Window tmp_win;
	
				width	= cev->width;
				height = cev->height;
	
				if ((cev->x == 0) && (cev->y == 0)) {
					XLockDisplay(display);
					XTranslateCoordinates(display, cev->window,
						DefaultRootWindow(cev->display),
						0, 0, &xpos, &ypos, &tmp_win);
					XUnlockDisplay(display);
				} else {
					xpos = cev->x;
					ypos = cev->y;
				}
			}
			break;

		}
	}
	
	xine_close(stream);
	xine_event_dispose_queue(event_queue);
	xine_dispose(stream);
	if(ao_port) {
		xine_close_audio_driver(xine, ao_port);
	}
	xine_close_video_driver(xine, vo_port);	
	xine_exit(xine);
	
	XLockDisplay(display);
	XUnmapWindow(display,	window);
	XDestroyWindow(display, window);
	XUnlockDisplay(display);
	
	XCloseDisplay (display);

	return NULL;
}

int main (int argc, char **argv) {

	struct _playlist *list;

	pthread_t xine_tid;

	g_thread_init(NULL);
	gdk_threads_init();
	gdk_threads_enter();
	gtkInit();
	initConfig();

	list = createPlaylist();
	appendToList(list, "/mp3/A Perfect Circle/eMOTIVe/05-Passive.mp3");
	appendToList(list, "/mp3/A Perfect Circle/Thirteenth_Step/04-Blue.mp3");

	printf("First location: %s\n", list->firstItem->location);
	pthread_create( &xine_tid, NULL, xinePlay, list->firstItem->location);

	menuWindow = createMenuWindow();

	enterMain();
	gdk_threads_leave ();

	return 0;
}
