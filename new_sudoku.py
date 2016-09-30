from sudoku import Sudoku, Grid, CommandLineInterface


__author__ = "4280211: Julia Holzmann, 4109208: Philipp Lang"
__copyright__ = "Copyright 2013/14 – EPR-Goethe-Uni" 
__credits__ = "Vielen Dank bei der Hilfe für die Vererbung der Klassen. \
Leider kenn ich nicht den Namen." 
__license__ = "GPL"  
__version__ = "0.7" 
__status__ = "Development"  # oder "Prototype" oder "Production" 


"""Wir haben das Sudokuspiel 0.9.2 verwendet. Sollte es zu Problemen kommen, bitte
   das Basisspiel downgraden auf Version 0.9.2."""


class Item(Sudoku.Item):
    """Diese Klasse legt die Struktur der Elemente fest. Es wird von der
       der Klasse Sudoku.Item aus dem Basisspiel geerbt."""
    
    def __init__(self, value:int = 0, hint:str = "", notes:list = [], \
                 solid:bool = False):
        """Initialisator der Klasse Item. Es werden Standardwerte vorgegeben.
           Diese werden dann in den instanzierten Attributen gespeichert."""
        self.value = value
        self.notes = notes
        self.hint = hint
        self.solid = solid

    def set(self, value:int = 0, solid:bool = False, hint:str = " "):
        """Diese Funktion legt die Speicherung eines Wertes in das Objekt fest.
           Hinzu kommen Eigenschaften (feste Zahl ja/nein) und Notizen."""
        self.value = int(value)
        self.solid = solid
        self.hint = hint

    def set_note(self, hint:str):
        """Legt eine Notiz zu einem Wert an."""
        self.hint = hint

    def get(self):
        """Gibt einen Wert aus dem Objekt zurueck."""
        return(self.value)
    
    def get_solid(self):
        """Gibt die Eigenschaft zurueck, ob dieser Wert fest ist, oder nicht."""
        return(self.solid)

    def get_hint(self):
        """Gibt die zu einem Wert gespeicherte Notiz zurueck."""
        return(self.hint)



class new_Sudoku(Sudoku, Item, Grid):
    """In dieser Klasse wird das Basisspiel Sudoku um weitere Funktionen
       erweitert."""
    def __init__(self, T:Item):
        Grid.__init__(self, T, 9, 3)
        CommandLineInterface.__init__(self)
        Sudoku.__init__(self, T)              #Diese Initialisierung muss ausgefuehrt
                                              #werden, damit wir das Template des
                                              #Spielfeldes erhalten. 

    def fix_field(self, row:str, col:str, value:int):
        """Diese Funktion setzt einen Wert in das Sudoku als festen Wert.
           Somit kann dieser Wert nicht mehr ueberschrieben werden."""
        row, col = self._mapper(row, col)
        self[row][col].set(value, True)
        if self.is_valid_row(row) or self.is_valid_col(col) \
           or self.is_valid_submarix(row, col):            
            return "Conflicted value {0}!\n".format(value)

    def set(self, row:str, col:str, value:int):
        """Diese Funktion setzt einen Wert in das Sudoku der nicht fest ist.
        Dieser Wert kann also ueberschrieben werden."""
        row, col = self._mapper(row, col)
        solid = self[row][col].get_solid()
        if solid == False:
            self[row][col].set(value)
            if self.is_valid_row(row) or self.is_valid_col(col) \
               or self.is_valid_submarix(row, col):            
                return "Conflicted value {0}!\n".format(value)
        else:
            print("Kann nicht ueberschrieben werden.")

    def set_note(self, row: str, col:str, hint:str):
        """Diese Funktion setzt eine Notiz zu einem Wert."""
        row, col = self._mapper(row, col)
        self[row][col].set_note(hint)

    def get_note(self, row: str, col:str) -> Item:
        """Diese Funktion gibt die gespeicherte Notiz aus."""
        row_old, col_old = row, col
        row, col = self._mapper(row, col)
        hint = self[row][col].get_hint()
        return("Notiz in {0}{1}: {2}\n".format(row_old.upper(), col_old, hint))            

    def generate_notes(self):
        """Diese Funktion schreibt einstzbare Zahlen als Hinweis in die Notiz."""
        _hint = ""


        
        for item_row in range(9):
            for item_col in range(9):
                for number in range(9):
                    _value = number + 1
                    string_value = str(_value)
                    old_note = new_Sudoku.get_note(self, chr(item_row + 97), chr(item_col + 49))
                    _hint = _hint + " " + string_value
                    

                    item = self[item_row][item_col].get()
                    self[item_row][item_col].set(number + 1)

                    new_Sudoku.set_note(self, chr(item_row + 97), chr(item_col + 49), "Hinweis: " + _hint)
                    
                    if self.is_valid_row(item_row) or self.is_valid_col(item_col) or self.is_valid_submarix(item_row, item_col):
                        new_Sudoku.set_note(self, chr(item_row + 97), chr(item_col + 49), old_note)

                    self[item_row][item_col].set(item)
                    new_Sudoku.set_note(self, chr(item_row + 97), chr(item_col + 49), "Hinweis: " + _hint)
        
                        
                                        


        # Die beiden folgenden for-Schleifen erzeugen die Werte, die nicht mehr
        # auftauchen duerfen.
##        for items_row in range(9):
##            for items_col in range(9):
##                item = self[items_row][items_col].get()
##                items.append(item)
##        for item_row in range(9):
##            row = Grid.get_row(self, item_row)
##            for item_col in range(9):
##                _hint = ""
##                col = Grid.get_col(self, item_col)
##                submatrix = Grid.get_submarix(self, item_row, item_col)
##                for number in range(9):
##                    _value = number + 1
##                    if not _value in items:
##                        string_value = str(_value)
##                        _hint = _hint + " " + string_value
##                        new_Sudoku.set_note(self, chr(item_row + 97), chr(item_col + 49), "Hinweis: " + _hint)
##            items = []
##            
    
                    



new_Sudoku(Item).mainloop() #Zum ausführen des Skripts


