#include <gtk/gtk.h>

void gtkInit(void) {
	gtk_set_locale();
	gtk_init(0, NULL);
}

GtkWidget *createMenuWindow(void) {

	GtkWidget *window;

	window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
	gtk_window_set_default_size(GTK_WINDOW(window), 300, 600);
	gtk_window_set_keep_above(GTK_WINDOW(window), TRUE);
	gtk_window_set_opacity(GTK_WINDOW(window), 0.50);

	gtk_widget_show_all(window);

	return window;

}

void enterMain(void) {

	while(1) {
		gtk_main();
		
	}

}
