#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk
import MySQLdb


class Handler:
    def __init__(self):
        # Iniciamos el GtkBuilder para tirar del fichero de glade
        self.builder = Gtk.Builder()
        self.builder.add_from_file("crud.glade")

        self.selectedRow = None



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
            "onCloseMain" : self.onDeleteWindow,
            "onSelectTableRow" : self.onSelectTableRow
        }
        self.builder.connect_signals(self.handlers)

        #configure windows
        self.window  = self.builder.get_object("principal")
        self.about   = self.builder.get_object("aboutdialog")
        self.form    = self.builder.get_object("newEditForm")
        self.delform = self.builder.get_object("DeleteDialog")
        self.errorMessage = self.builder.get_object("ErrorMessage")

        #Generamos el item del combo
        query= "SELECT pkUser FROM user;" 
        micursor = Conexion.cursor()   
        micursor.execute(query);
        bdData = micursor.fetchall()
        Conexion.commit()
        micursor.close()
        self.comboboxFila = self.builder.get_object("comboboxFila")
        set_combo_from_list(self.comboboxFila,bdData)

        #Generamos el iterador para el modelo TreeView
        self.treeview  = self.builder.get_object('VistaTabla')
        self.store = self.builder.get_object('Datos')
        initColumns(self)
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
        create_user(self,*args)
        refresh(self)
        self.form.hide()

    def onCancelForm(self,*args):
        self.form.hide()
        print 'cancel_form'

    #EVENTOS VENTANA ELIMINAR
    def onDelconfirm(self,*args):
        print 'del confirm'
        if not self.selectedRow:
            self.errorMessage.show()
            return 0
        query = "delete from user where pkUser = "+ str(self.selectedRow)
        micursor = Conexion.cursor()
        micursor.execute(query)
        Conexion.commit()
        micursor.close()
        self.delform.hide()
        refresh(self)
        delete_from_combo(self,self.builder.get_object("comboboxFila"))
        self.selectedRow = None

    def onDelCancel(self,*args):
        self.delform.hide()
        print 'del cancel'   

    #EVENTOS MENU
    def onRefresh(self,*args):
        print 'refresh_users'
        refresh(self)

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

    #Atendemos al posible cambio del combobox de items
    def onSelectTableRow(self,combo):
        tree_iter = combo.get_active_iter()

        if tree_iter != None:
            model = combo.get_model()
            row_id = model[tree_iter][0]
            print("Selected: ID=%d" % (row_id))
            self.selectedRow = row_id




def main():
    window = Handler()
    Gtk.main()
    micursor.close()
    return 0


def delete_from_combo(cb,combo):
    print 'delete from combo'
    tree_iter = combo.get_active_iter()
    model = combo.get_model()
    model.remove(tree_iter)
def add_to_combo(cb,combo,id):
    print 'add to combo'
    print id
    model = combo.get_model()
    print model
    model.append([id])

def set_combo_from_list (cb, items):
    """Setup a ComboBox or ComboBoxEntry based on a list of strings."""           
    model = Gtk.ListStore(int)
    for i in items:
        model.append(i)
    cb.set_model(model)
    cell = Gtk.CellRendererText()
    cb.pack_start(cell, True)
    cb.add_attribute(cell, 'text', 0)

def create_user(self,*args):
    nombre = self.builder.get_object("form_nombre").get_text()
    apellidos = self.builder.get_object("form_apellidos").get_text()
    edad = self.builder.get_object("form_edad").get_text()
    color = self.builder.get_object("form_color").get_color().to_string()
    if self.builder.get_object("form_sexoH").get_active():
        sexo = 'Hombre'
    else:
        sexo = 'Mujer'
    query = "insert into user (nombre,apellidos,edad,color,sexo) values ("\
        +"'"+nombre+"',"\
        +"'"+apellidos+"',"\
        +""+edad+","\
        +"'"+color+"',"\
        +"'"+sexo+"');"
    print query
    micursor = Conexion.cursor()
    micursor.execute(query)
    Conexion.commit()
    add_to_combo(self,self.builder.get_object("comboboxFila"),micursor.lastrowid)
    micursor.close()


def initColumns(cb,*args):
    for index,col in enumerate (cb.treeview.get_columns()):
        print col
        print index
        cell = Gtk.CellRendererText()
        col.pack_start (cell,True)
        # Attributes for the column - make it display text of column 0
        # from the model
        col.add_attribute (cell, "text", index)    


def refresh(cb,*args):
    print 'refreshing'
    query = "select nombre,apellidos,edad,color,sexo from user"
    micursor = Conexion.cursor(MySQLdb.cursors.DictCursor)  
    micursor.execute(query);
    bdData = micursor.fetchall()
    cb.store.clear()
    for currentData in bdData:
        print currentData
        cb.store.append([currentData['nombre'],
            currentData['apellidos'],
            currentData['edad'],
            currentData['color'],
            currentData['sexo']
            ])
    micursor.close()
    Conexion.commit()




if __name__ == '__main__':
    Conexion = MySQLdb.connect(host='localhost', user='acastillo', passwd ='acastillo', db='crud')  
    main()

