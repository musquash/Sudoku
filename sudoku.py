# -*- coding: utf-8 -*-
__author__ = "123456: Carsten Heep"
__copyright__ = "Copyright (C) 2013 Carsten Heep"
__license__ = "WTFPL except publishing outside the accompanying moodle course!"
__version__ = "0.9.2"

import os, re
import pickle

class CommandLineInterface():
    class Command():
        def __init__(self, function:str, regex:str, description:str=""):
            self.function = function
            self.regex = regex
            self.description = description
    
    def __init__(self, prompt=">>> "):
        self.prompt = prompt
        self._commands = []
        self._run = False
    
    def get_commands(self):
        return self._commands
    
    def add_command(self, function:str, regex:str, description:str):
        """ Fügt den Befehl Function in die Liste hinzu."""
        self._commands.append(CommandLineInterface.Command(function, regex, description))
    
    def add_commands(self, commnads:list):
        """Fügt sämtliche Befehle aus Command in eine neue Liste zusammen."""
        for function, regex, description in commnads:
            self.add_command(function, regex, description)
    
    def clear_screen(self, string:str):
        if os.name == "posix":
            os.system('clear')
        elif os.name in ("nt", "dos", "ce"):
            os.system('cls')
        else:
            print(80 * "\n")
        print(string)
    
    def read_command(self, message:str) -> tuple:
        string = input(message + self.prompt)
        for command in self.get_commands():
            if re.search(command.regex, string):
                return command.function, re.split(command.regex, string)[1:-1]
        return None, None
    
    def mainloop(self):
        """ Ist die Hauptschleife. Sie läuft solange bis ein bekannter Befehl eingegeben wird.
            Sonst wird weiter nach einer Eingabe gefragt."""
        msg = ""
        self._run = True
        while self._run:
            self.clear_screen(self)
            function, args = self.read_command(msg)
            if function == None:
                msg = "Invalid input "
                continue
            try:
                args = "" if len(args) == 0 else "'{0}'".format("', '".join(args))                
                msg = eval("self.{0}({1})".format(function, args))                
            except Exception as e:
                msg = "This function is not implemented :(\n{0}\n".format(e)
            finally:
                msg = "" if msg == None else msg

    def help(self):
        return "".join([cmd.description for cmd in self.get_commands()])
             
    def quit(self):
        print("{0:^79}".format("ByeBye!"))
        self._run ^= True

class Grid():
    class Item(object):
        def __init__(self, value:int=0):  #Init in unserer Klasse neu schreiben
            self.set(value)
        
        def __str__(self):
            return str(self.get())
        
        def __repr__(self):
            return self.get()
        
        def __eq__(self, other):
            return self.get() == other.get()
        
        def __ne__(self, other):
            return self.get() != other.get()
    
        def set(self, value:int):       # Für feste Felder wichtig!
            self._value = int(value)
            
        def get(self):
            return self._value #liest was in einem Feld drin steht.
    
    def __init__(self, T:object, size=9, sub_size=3):
        self._base_type = T
        self._size = size
        self._sub_size = sub_size
        self.reset()             
    
    def __repr__(self):
        return self._data    
    
    def __getitem__(self, index:int):
        """Liest den Wert zu einer gegebenen Indexposition an."""
        return self._data[index]
    
    def remove(self, row:int, col:int) -> None:
        """Löscht einen Eintrag zur gegeben Position."""
        self[row][col] = self.get_empty()
    
    def get_row(self, index:int) -> list:
        if 0 <= index <= self._size:
            return self._data[index][:]## Copy List
    
    def get_col(self, index:int) -> list:
        if 0 <= index <= self._size:          #Indexpositionierung falsch? Entweder 0 < oder index <
            return [row[index] for row in self._data]
    
    def get_submarix(self, row:int, col:int) -> list:
        """ Liefert das kleine 3*3 Feld des Sudokus."""
        def mapper(index:int) -> (int, int):
            temp = index // self._sub_size * self._sub_size
            return temp, temp + self._sub_size
        
        row_min, row_max = mapper(row)
        col_min, col_max = mapper(col)
        submatrix = []
        for row in range(row_min, row_max):
            for col in range(col_min, col_max):
                submatrix.append(self._data[row][col])
        return submatrix
    
    def get_size(self, offset:int=0) -> int:
        return self._size + offset
    
    def get_subsize(self) -> int:
        return self._sub_size
    
    def get_empty(self) -> object:
        return self._base_type()
    
    def reset(self) -> None:
        self._data = [[self.get_empty() for col in range(self._size)]
                      for row in range(self._size)]
    
class Sudoku(Grid, CommandLineInterface):
    def __init__(self, T:Grid.Item):
        Grid.__init__(self, T, 9, 3)
        CommandLineInterface.__init__(self)
        commands = [## Set
                    ("set", "^set\s+([a-iA-I])([1-9])\s+([1-9])$", """Setzen eines Wertes (set):
        Der Befehl zum setzen einer Zahl ist "set ReiheSpalte Wert" also z.B. "set A1 2"
        Der Befehl set kann als "ReiheSpalte Wert" abgekürzt werden -> a1 2" \n"""),
                    ("set", "^([a-iA-I])([1-9])\s+([1-9])$", ""),
                    ## Del
                    ("remove", "^del\s+([a-iA-I])([1-9])$", """Löschen eines Wertes (del):
        Der Befehl zum löschen einer Zahl ist "del ReiheSpalte Wert" also z.B. "del A1 8"\n"""),
                    ## Quit
                    ("quit", "^quit$|^exit$|^close$", """Beenden des Programms
        Das Programm kann jederzeit mit einem der Wörter "quit", "exit" oder "close" beendet werde
        Alternativ können die Anfangsbuchstaben der Befehle verwendet werden.\n"""),
                    ("quit", "^q$|^e$|^c$", ""),
                    ## Reset
                    ("reset", "^clear$|^cls$", ""),
                    ## Load / Save
                    ("load", "^load\s+(\w+)$", """Laden eines Spiels (load|save):
        Mit dem Befehl "load Name" kann ein Spiel mit dem angegebenem Name geladen werden; z.B "load dummy_game".
        Mit "save Name" wird es unter dem angegebenem Name gespeichert; z.B "save dummy_game".
        Nemen "load" und "save" gibt es die Abkürzungen "l" und "s".
        Diese Befehle haben zur Folge, dass ein 'default' Datei (sudoku.lev) geladen bzw. geschrieben wird.
        Sie sind somit gleichbedeutend zu "load sudoku" bzw. "save sudoku".\n"""),
                    ("save", "^save\s+(\w+)$", ""),
                    ("load", "^l$", ""),
                    ("save", "^s$", ""),
                    ##
                    ("list_games", "^games$", """Spielstände (games):
                    Der Befehl "games" listet alle vorhandenen Speilstände auf.\n"""),
                    ## Help
                    ("help", "^help$", ""),
                     
                    ## TODO :)
                    ("fix_field", "^fix\s+([a-iA-I])([1-9])\s+([1-9])$", ""),
                    
                    ("set_note", "^note\s+([a-iA-I])([1-9])\s+(\w*)$", ""),
                    ("get_note", "^note\s+([a-iA-I])([1-9])$", ""),
                    ("generate_notes", "^notes$", ""),
                    
                    ("get_free", "^hint$", ""),
                    ("solve", "^next$", ""),
                    ("solve", "^next\s+([1-9]\d*)$", ""),
                    
                    ("level", "^level$", ""),
                    
                    ("undo", "^undo", ""),
                    ("undo", "^undo\s+([1-9]\d*)$", ""),
                    ("redo", "^redo", ""),
                    ("redo", "^redo\s+([1-9]\d*)$", "")
                   ]
        
        self.add_commands(commands) #übergibt die Befehle.
        
        self.extention = ".lev"
        self._default_path = "{0}{1}{2}{1}".format(os.curdir, os.sep, "level")        
        folder = os.path.dirname(self._default_path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        self._default_name = "sudoku"
        self._template = "\n   ╔═══════════╦═══════════╦═══════════╗\nA  ║ .0. │ .1. │ .2. ║ .3. │ .4. │ .5. ║ .6. │ .7. │ .8. ║\n   ║───┼───┼───║───┼───┼───║───┼───┼───║\nB  ║ .9. │ .10. │ .11. ║ .12. │ .13. │ .14. ║ .15. │ .16. │ .17. ║\n   ║───┼───┼───║───┼───┼───║───┼───┼───║\nC  ║ .18. │ .19. │ .20. ║ .21. │ .22. │ .23. ║ .24. │ .25. │ .26. ║\n   ╠═══════════╬═══════════╬═══════════╣\nD  ║ .27. │ .28. │ .29. ║ .30. │ .31. │ .32. ║ .33. │ .34. │ .35. ║\n   ║───┼───┼───║───┼───┼───║───┼───┼───║\nE  ║ .36. │ .37. │ .38. ║ .39. │ .40. │ .41. ║ .42. │ .43. │ .44. ║\n   ║───┼───┼───║───┼───┼───║───┼───┼───║\nF  ║ .45. │ .46. │ .47. ║ .48. │ .49. │ .50. ║ .51. │ .52. │ .53. ║\n   ╠═══════════╬═══════════╬═══════════╣\nG  ║ .54. │ .55. │ .56. ║ .57. │ .58. │ .59. ║ .60. │ .61. │ .62. ║\n   ║───┼───┼───║───┼───┼───║───┼───┼───║\nH  ║ .63. │ .64. │ .65. ║ .66. │ .67. │ .68. ║ .69. │ .70. │ .71. ║\n   ║───┼───┼───║───┼───┼───║───┼───┼───║\nI  ║ .72. │ .73. │ .74. ║ .75. │ .76. │ .77. ║ .78. │ .79. │ .80. ║\n   ╚═══════════╩═══════════╩═══════════╝\n     1   2   3   4   5   6   7   8   9  \n"
    
    def __str__(self):
        index, template = 0, self._template[:]
        for row in self:
            for item in row:
                item = "   " if item == self.get_empty() else "{0:^3}".format(item)
                template = template.replace(" .{0}. ".format(index), item, 1)
                index += 1
        return template
    
    def _mapper(self, row:str, col:str) -> tuple:
        return ord(row.lower()) - ord('a'), ord(col) - ord('1')
    
    def set(self, row:str, col:str, value:int):
        row, col = self._mapper(row, col)
        self[row][col].set(value)
        if self.is_valid_row(row) or self.is_valid_col(col) or self.is_valid_submarix(row, col):            
            return "Conflited value {0}!\n".format(value)
        
    
    def get(self, row:str, col:str) -> Grid.Item:
        row, col = self._mapper(row, col)
        return self[row][col]
    
    def remove(self, row:str, col:str) -> None:
        row, col = self._mapper(row, col)
        self[row][col] = self.get_empty()
        
    def _is_valid(self, values:list):
        for value in values:
            if value != self.get_empty() and values.count(value) > 1:
                return True
        return False
    
    def is_valid_row(self, row:int):
        return self._is_valid(self.get_row(row))       
    
    def is_valid_col(self, col:int):        
        return self._is_valid(self.get_col(col))
    
    def is_valid_submarix(self, row:int, col:int):
        return self._is_valid(self.get_submarix(row, col))
    
    def get_fullname(self, filename):
        if filename == "":
            return "{0}{1}{2}".format(self._default_path, self._default_name, self.extention)
        else:
            return "{0}{1}{2}".format(self._default_path, filename, self.extention)
    
    def save(self, filename:str=""):
        try:
            with open(self.get_fullname(filename), "wb") as file:
                pickle.dump(self._data, file) 
        except:
            return "File '{0}' Not Written! ".format(filename)

    def load(self, filename:str=""):
        try:
            print(self.get_fullname(filename))
            with open(self.get_fullname(filename), "rb") as file:
                self._data = pickle.load(file)
        except:
            return "File '{0}' Not Found! ".format(filename)
    
    def list_games(self):
        files = [f for f in os.listdir(self._default_path) if f.endswith(self.extention)]
        return "Spielstände:\n\t" + "\n\t".join([f[:-4] for f in files]) + "\n"
