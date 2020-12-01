#===========================
# Imports
#===========================
import tkinter as tk
from tkinter import ttk, colorchooser as cc, Menu, Spinbox as sb, scrolledtext as st, messagebox as mb, filedialog as fd, simpledialog as sd

import PyPDF2
import pyttsx3

#===========================
# Main App
#===========================
class App(tk.Tk):
    """Main Application."""
    #------------------------------------------
    # Initializer
    #------------------------------------------
    def __init__(self):
        super().__init__()
        self.init_config()
        self.init_vars()
        self.init_widgets()

    #-------------------------------------------
    # Window Settings
    #-------------------------------------------
    def init_config(self):
        self.resizable(True, True)
        self.title('Extract Text from PDF Version 1.0')
        self.iconbitmap('python.ico')
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

    def init_vars(self):
        self.text = ''

    #-------------------------------------------
    # Widgets / Components
    #-------------------------------------------
    def init_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        fieldset = ttk.LabelFrame(frame, text='Select PDF')
        fieldset.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        button = ttk.Button(fieldset, text='Browse', command=self.browse_file)
        button.pack(side=tk.LEFT)

        self.filepath = tk.StringVar()
        self.entry = ttk.Entry(fieldset, width=80, textvariable=self.filepath)
        self.entry.pack(side=tk.LEFT, ipady=5)

        button = ttk.Button(frame, text='Extract', command=self.extract_pdf)
        button.pack(side=tk.TOP, anchor=tk.E, padx=(0, 10), pady=(0, 10))

        self.textarea = st.ScrolledText(frame, wrap=tk.WORD)
        self.textarea.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        button = ttk.Button(frame, text='Play Audio', command=self.play_audio)
        button.pack(side=tk.TOP, anchor=tk.E, padx=(0, 10), pady=(0, 10))

    # ------------------------------------------
    def browse_file(self):
        """Open and loads the pdf file."""
        try:
            file_type = [('PDF Files', '*.pdf')]
            self.filename = fd.askopenfilename(title='Open', initialdir='/', filetypes=file_type)
            self.filepath.set(self.filename)
            self.entry.config(state=tk.DISABLED)

        except Exception as e:
            return

    def extract_pdf(self):
        pdf_file = open(self.filename,'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)

        for page_number in range(0, pdf_reader.numPages):
            page_object = pdf_reader.getPage(page_number)
            self.text += page_object.extractText()

        pdf_file.close()

        self.textarea.insert(tk.INSERT, self.text)

    def play_audio(self):
        engine = pyttsx3.init()
        engine.setProperty('rate', 125)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.say(self.text)
        engine.runAndWait()

#===========================
# Start GUI
#===========================
def main():
    app = App()
    app.mainloop()

if __name__ == '__main__':
    main()