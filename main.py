#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk

class Handler:
    def __init__(self):
        # Iniciamos el GtkBuilder para tirar del fichero de glade
        builder = Gtk.Builder()
        builder.add_from_file("crud.glade")
        self.handlers = {
            "onDeleteWindow": self.onDeleteWindow,
            "onOpenAbout": self.onOpenAbout,
            "onCloseAboutResponse": self.onCloseAboutResponse,
            "onSaveForm" : self.onSaveForm,
            "onCancelForm" : self.onCancelForm,
            "onDelConfirm" : self.onDelconfirm,
            "onDelCancel" : self.onDelCancel,
            "onRefresh" : self.onRefresh,
            "onDelUser" : self.onDelUser,
            "onEditUser" : self.onEditUser,
            "onNewUser" : self.onNewUser,
            "onCloseMain" : self.onDeleteWindow 
        }
        builder.connect_signals(self.handlers)

        #configure windows
        self.window  = builder.get_object("principal")
        self.about   = builder.get_object("aboutdialog")
        self.form    = builder.get_object("newEditForm")
        self.delform = builder.get_object("DeleteDialog")
        self.window.show_all()
        self.window.resize(300,300)

    def onDeleteWindow(self, *args):
        print 'close'
        Gtk.main_quit(*args)
    #EVENTOS VENTANA FORMULARIO
    def onSaveForm(self,*args):
        print 'save form'
    def onCancelForm(self,*args):
        self.form.hide()
        print 'cancel_form'

    #EVENTOS VENTANA ELIMINAR
    def onDelconfirm(self,*args):
        print 'del confirm'
    def onDelCancel(self,*args):
        self.delform.hide()
        print 'del cancel'   

    #EVENTOS MENU
    def onRefresh(self,*args):
        print 'refresh_users'
    def onDelUser(self,*args):
        print 'del_user'
        self.delform.show()
    def onEditUser(self,*args):
        self.form.show()
        print 'edit_user'  
    def onNewUser(self,*args):
        self.form.show()
        print 'new_user'

    #ABOUT
    def onOpenAbout(self,*args):
        print 'open_about'
        self.about.show()
    def onCloseAboutResponse(self,window,data=None):
        print 'closeAbout'
        self.about.hide()



def main():
    window = Handler()
    Gtk.main()
    print 'exit'
    return 0

if __name__ == '__main__':
    main()

