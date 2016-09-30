if __name__ == '__main__':
    from sudoku import Sudoku
    
    ## Workaround 4 Pickleing nested classes
    class Item(Sudoku.Item):
        pass
    
    Sudoku(Item).mainloop()