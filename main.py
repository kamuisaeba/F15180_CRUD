#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk
import MySQLdb


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

        #Generamos el item del combo
        query= "SELECT pkUser FROM user;" 
        micursor = Conexion.cursor()   
        micursor.execute(query);
        bdData = micursor.fetchall()
        micursor.close()
        self.comboboxFila = builder.get_object("comboboxFila")
        set_combo_from_list(self.comboboxFila,bdData)

        #Generamos el iterador para el modelo TreeView
        self.treeview  = builder.get_object('VistaTabla')
        self.store = builder.get_object('Datos')
        refresh(self)

        #Mostramos la ventana inicial
        self.window.show_all()
        self.window.resize(300,300)

    #definición de las señales
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
    micursor.close()
    return 0


def set_combo_from_list (cb, items):
    """Setup a ComboBox or ComboBoxEntry based on a list of strings."""           
    model = Gtk.ListStore(int)
    for i in items:
        print i
        model.append(i)
    cb.set_model(model)
    cell = Gtk.CellRendererText()
    cb.pack_start(cell, True)
    cb.add_attribute(cell, 'text', 0)

def create_user():
    return 0
def refresh(cb,*args):
    query = "select nombre,apellidos,edad,color,sexo from user"
    micursor = Conexion.cursor(MySQLdb.cursors.DictCursor)  
    micursor.execute(query);
    bdData = micursor.fetchall()
    for currentData in bdData:
        print currentData
        cb.store.append([currentData['nombre'],
            currentData['apellidos'],
            currentData['edad'],
            currentData['color'],
            currentData['sexo']
            ])
    for i, column_title in enumerate(["Nombre","Apellidos","Edad","Color","Sexo"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            cb.treeview.append_column(column)




if __name__ == '__main__':
    Conexion = MySQLdb.connect(host='localhost', user='acastillo', passwd ='acastillo', db='crud')  
    main()

