# GROUP MEMBERS
# LORIA, BRIAN ANGELO I.
# DOLOR, RONEL DYLAN JOSHUA A.
# ENRIQUEZ, CHAD ANDREI A.

from tkinter.filedialog import askopenfilename
from tkinter import *
from tkinter import ttk
from lexer import *
from lextypes import *
from symbol_table import *
from syntax_analyzer import *
from type_identifier import *
import copy

class GUI:
    def __init__(self, root):
        self.root = root
        self.items = []

    def create_file_explorer_widget(self):
        self.label_info = StringVar()
        self.file_path = ''

        self.project_label = Label(self.root, text = "LOLCODE Interpreter", relief=FLAT , width=136, height=1, anchor='w', bg= "Black", fg='White')
        self.file_explorer_label = Label(self.root, textvariable=self.label_info, relief=GROOVE, width=70, height=1, anchor='w')
        self.file_explorer_button = Button(text ="Open File", width=7, height=1, command=self.read_file)

        self.file_explorer_label.place(x = 3, y = 3)
        self.file_explorer_button.place(x = 505, y = 1)
        self.project_label.place(x = 570, y = 3)

    def create_text_editor_widget(self):

        self.text_editor_text_scroll = Scrollbar(self.root, orient='vertical')
        self.text_editor_text = Text(self.root, font=("Georgia, 12"), yscrollcommand=self.text_editor_text_scroll.set, width = 62, height = 25)
        self.text_editor_text_scroll.config(command=self.text_editor_text.yview)
        self.text_editor_text.place(x = 3, y = 27)

    def create_list_of_tokens_widget(self):
        headings = ('lex', 'lexClass')

        self.data_tree_lex = ttk.Treeview(self.root, columns=headings, show='headings', height=21)
        self.data_tree_lex.heading('lex', text='Lexeme')
        self.data_tree_lex.column("lex", minwidth=0, width=300, stretch=NO)
        self.data_tree_lex.heading('lexClass', text='Classification')
        self.data_tree_lex.column("lexClass", minwidth=0, width=300, stretch=NO)
        self.data_tree_lex.place(x = 570, y = 28)

    def create_symbol_table_widget(self):
        headings = ('varident', 'value', 'type')

        self.data_tree_sym = ttk.Treeview(self.root, columns=headings, show='headings', height=21)
        self.data_tree_sym.heading('varident', text='identifier')
        self.data_tree_sym.column("varident", minwidth=0, width=115, stretch=NO)
        self.data_tree_sym.heading('value', text='Value')
        self.data_tree_sym.column("value", minwidth=0, width=115, stretch=NO)
        self.data_tree_sym.heading('type', text='Type')
        self.data_tree_sym.column("type", minwidth=0, width=115, stretch=NO)
        self.data_tree_sym.place(x = 1180, y = 28)

    def create_execute_button_widget(self):
        self.execute_button = Button(self.root, text = 'Execute', command = self.execute, width = 106, height = 3)
        self.execute_button.place(x = 4, y = 485)

    def create_clear_button_widget(self):
        self.execute_button = Button(self.root, text = 'Clear', command = self.clear, width = 106, height = 3)
        self.execute_button.place(x = 773, y = 485)

    def create_console_log(self):
        self.listbox = Listbox(
            self.root,
            height = 21,
            width = 253,
            bg="black",
            fg="orange"
        )
        self.listbox.place(x = 4, y = 545)

    def read_file(self):
        self.clear_text_data()
        self.file_path = askopenfilename()
        self.file_info = open(self.file_path, 'r+')
        self.file_info = self.file_info.read()
        self.label_info.set(self.file_path)
        self.open_file(self.file_info)

    def open_file(self, file_contents):
        self.text_editor_text.delete("1.0", "end")
        self.text_editor_text.insert(END, file_contents)

    def clear_text_data(self):
        for index in self.data_tree_lex.get_children():
            self.data_tree_lex.delete(index)

        for index in self.data_tree_sym.get_children():
            self.data_tree_sym.delete(index)

    def determine_lexemes(self):
        self.lexemes = Lexemes(self.file_path)
        self.lexemes.create_lexers()
        for i in self.lexemes.lexers:
            self.data_tree_lex.insert("", END, values=(i.lexeme, i.lexClassification))

    def initialize_symbol_table(self):
        self.symbol_table = Symbol_Table()

    def determine_entries_in_symbol_table(self):
        for i in self.symbol_table.symbol_table:
            self.data_tree_sym.insert("", END, values=(i, self.symbol_table.symbol_table[i], get_type(self.symbol_table.symbol_table[i])))

    def execute(self):
        self.clear()
        with open(self.file_path, "w") as f:
            f.write(self.text_editor_text.get(1.0,END))
        self.initialize_symbol_table()
        self.determine_lexemes()
        self.test()
        self.determine_entries_in_symbol_table()

    def clear(self):
        self.listbox.delete(0, END)
        self.clear_text_data()

    def test(self):
        list_of_tokens = copy.deepcopy(self.lexemes.lexers)
        program_abstraction(list_of_tokens, self.symbol_table, self.listbox)

def main():
    root = Tk()
    # root.state("zoomed")
    root.geometry("1530x890")
    root.title("Lolcode Interpreter")
    root.resizable(False, False)
    root['background'] = '#D3D3D3'

    LOL_CODE_GUI = GUI(root)

    LOL_CODE_GUI.create_file_explorer_widget()
    LOL_CODE_GUI.create_text_editor_widget()
    LOL_CODE_GUI.create_list_of_tokens_widget()
    LOL_CODE_GUI.create_symbol_table_widget()
    LOL_CODE_GUI.create_execute_button_widget()
    LOL_CODE_GUI.create_clear_button_widget()
    LOL_CODE_GUI.create_console_log()

    root.mainloop()

main()
