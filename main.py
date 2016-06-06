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
            "onSelectTableRow" : self.onSelectTableRow,
            "onCloseResponse" : self.onCloseResponse
        }
        self.builder.connect_signals(self.handlers)

        #configure windows
        self.window  = self.builder.get_object("principal")
        self.about   = self.builder.get_object("aboutdialog")
        self.form    = self.builder.get_object("newEditForm")
        self.delform = self.builder.get_object("DeleteDialog")
        self.errorMessage = self.builder.get_object("ErrorMessage")

        #Generamos el item del combo
        self.init_combo()

        #Generamos el iterador para el modelo TreeView
        self.treeview  = self.builder.get_object('VistaTabla')
        self.store = self.builder.get_object('Datos')
        self.initColumns()
        refresh(self)

        #Mostramos la ventana inicial
        self.window.show_all()
        self.window.resize(300,300)

    #Inicia las columnas del treeView
    def initColumns(cb):
        for index,col in enumerate (cb.treeview.get_columns()):
            print col
            print index
            cell = Gtk.CellRendererText()
            col.pack_start (cell,True)
            # Attributes for the column - make it display text of column 0
            col.add_attribute (cell, "text", index)    
    #Inicia el combo
    def init_combo (self):
        """Setup a ComboBox or ComboBoxEntry based on a list of strings."""  
        query= "SELECT pkUser FROM user;" 
        micursor = Conexion.cursor()   
        micursor.execute(query);
        items = micursor.fetchall()
        Conexion.commit()
        micursor.close()
        cb = self.comboboxFila = self.builder.get_object("comboboxFila")         
        model = Gtk.ListStore(int)
        for i in items:
            model.append(i)
        cb.set_model(model)
        cell = Gtk.CellRendererText()
        cb.pack_start(cell, True)
        cb.add_attribute(cell, 'text', 0)

    #definición de las señales
    def onDeleteWindow(self, *args):
        print 'close'
        Gtk.main_quit(*args)
    #EVENTOS VENTANA FORMULARIO
    def onSaveForm(self,*args):
        print 'save form'
        if validate_form(self):
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
            self.delform.hide()
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
        clear_form(self)
        self.builder.get_object("filaSeleccionada").set_text(str(self.selectedRow))
        self.form.show()
        print 'edit_user'  

    def onNewUser(self,*args):
        clear_form(self)
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

    def onCloseResponse(self, widget, data=None):
        widget.hide()



def main():
    window = Handler()
    Gtk.main()
    return 0


#Elimina un item del combo
def delete_from_combo(cb,combo):
    print 'delete from combo'
    tree_iter = combo.get_active_iter()
    model = combo.get_model()
    model.remove(tree_iter)


#añade item al combo
def add_to_combo(cb,combo,id):
    print 'add to combo'
    print id
    model = combo.get_model()
    print model
    model.append([id])


#refresca los elementos del combo
def refresh_combo(combo):
    model = combo.get_model()
    model.clear()
    query = "SELECT pkUser FROM user;" 
    micursor = Conexion.cursor()
    micursor.execute(query)
    bdData = micursor.fetchall()
    Conexion.commit()
    micursor.close()
    for i in bdData:
        model.append(i)



#Crea un usuario desde el formulario
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



#Refresca los datos (combo y tabla)
def refresh(cb,*args):
    print 'refreshing'
    query = "select pkUser,nombre,apellidos,edad,color,sexo from user"
    micursor = Conexion.cursor(MySQLdb.cursors.DictCursor)  
    micursor.execute(query);
    bdData = micursor.fetchall()
    cb.store.clear()
    for currentData in bdData:
        print currentData
        cb.store.append([
            currentData['pkUser'],
            currentData['nombre'],
            currentData['apellidos'],
            currentData['edad'],
            currentData['color'],
            currentData['sexo']
            ])
    micursor.close()
    Conexion.commit()
    refresh_combo(cb.builder.get_object("comboboxFila"))


#limpia el formulario
def clear_form(window):
    print 'clear'
    window.builder.get_object("form_nombre").set_text('')
    window.builder.get_object("form_apellidos").set_text('')
    window.builder.get_object("form_edad").set_text('')


#Valida los datos del formulario
def validate_form(cb):
    print 'validate'
    return None




if __name__ == '__main__':
    Conexion = MySQLdb.connect(host='localhost', user='acastillo', passwd ='acastillo', db='crud')  
    main()

