import classTextTranslate
import classAudioTranslate
import  classAudioRecord

# import everything from tkinter
from tkinter import *
from tkinter.filedialog import askopenfilename

OPTIONS_txt = [
    "Arabic (ar)",
    "Chinese (zh)",
    "English (en)",
    "French (fr)",
    "German (de)",
    "Italian (it)",
    "Japanese (ja)",
    "Portuguese (pt)",
    "Russian (ru)",
    "Spanish (es)"
    ]

OPTIONS_wav = [
    "Arabic (ar-AR)",
    "Chinese (zh-CN)",
    "English (en-US)",
    "French (fr-FR)",
    "German (de-DE)",
    "Italian (it-IT)",
    "Japanese (ja-JA)",
    "Portuguese (pt-PT)",
    "Russian (ru-RU)",
    "Spanish (es-ES)"
    ]

class Main_Window(Frame):

    _text_window = None
    _audio_window = None

    _label_msg_1 = "This is a mini translator that can translate audio files and text file!"
    _label_msg_2 = "Please click the corresponding button to select your functionality!"

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    # specification of some details of the code
    def init_window(self):

        # changing the title of our master widget
        self.master.title("Mini Translator")

        # making the size of the window
        self.master.geometry("600x400")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating button instance
        label_1 = Label(self, text=self._label_msg_1)
        label_2 = Label(self, text=self._label_msg_2)

        button_1 = Button(self, text="Text Translator", command=self.open_text_translate_window, height=3, width=20)
        button_2 = Button(self, text="Audio Translator", command=self.open_audio_translate_window, height=3, width=20)
        quit_button = Button(self, text="Quit", command=self.self_exit)

        # placing elements on my window
        label_1.place(x=50, y=100)
        label_2.place(x=50, y=120)
        button_1.place(x=50, y=250)
        button_2.place(x=300, y=250)
        quit_button.place(x=160, y=350)

    def open_text_translate_window(self):
        self._text_window = Text_Window(self)

    def open_audio_translate_window(self):
        self._audio_window = Audio_Window(self)

    def self_exit(self):
        exit(0)


# This is  the definition of the audio translation button

class Audio_Window(Toplevel):

    _input_file_name = ''
    _output_file_name = ''

    _in_language_sel = None
    _out_language_sel = None
    _new_sub_keys = None

    _record_window = None

    REPLACE = False

    _label_msg_1 = 'input language:'
    _label_msg_2 = 'output language:'
    _msg1 = 'Please select target file with "Select Input File" Button.'
    _msg2 = 'Translated file will be stored  with "_translate" postfix.'
    _msg3 = 'If keys need to renew, enter new keys and press button.'
    _msg4 = 'Mini Translator: Audio Translator'

    def __init__(self, master):
        Toplevel.__init__(self)
        self.master = master
        self.init_window()

    def init_window(self):

        self.title("Audio Translator")
        self.geometry("400x500")

        button_1 = Button(self, text="Select Input File", command=self.open_file_selection_window, height=3, width=30)
        button_2 = Button(self, text="Record new Audio", command = self.open_new_record_window, height=3, width=30)
        button_3 = Button(self, text="Return", command=self.close_current_window, height=3, width=15)
        button_4 = Button(self, text="Translate", command=self.translate, height=3, width=15)
        button_5 = Button(self, text="Renew Key", command=self.renew_sub_key, height=1, width=10)

        label_1 = Label(self, text=self._label_msg_1)
        label_2 = Label(self, text=self._label_msg_2)
        label_3 = Label(self, text=self._msg1)
        label_4 = Label(self, text=self._msg2)
        label_5 = Label(self, text=self._msg3)
        label_6 = Label(self, text=self._msg4)

        self._in_language_sel = StringVar()
        self._out_language_sel = StringVar()
        self._in_language_sel.set(OPTIONS_wav[0])
        self._out_language_sel.set(OPTIONS_wav[0])

        options_1 = OptionMenu(self, self._in_language_sel, *OPTIONS_wav)
        options_2 = OptionMenu(self, self._out_language_sel, *OPTIONS_wav)
        options_1.config(width=15)
        options_2.config(width=15)

        self._new_sub_keys = StringVar()
        new_keys = Entry(self, textvariable=self._new_sub_keys)

        button_1.place(x=50, y=300)
        button_2.place(x=50, y=350)
        button_3.place(x=185, y=400)
        button_4.place(x=50, y=400)
        button_5.place(x=250, y=215)

        label_1.place(x=50, y=240)
        label_2.place(x=50, y=270)
        label_3.place(x=20, y=140)
        label_4.place(x=20, y=160)
        label_5.place(x=20, y=180)
        label_6.place(x=100, y=100)

        options_1.place(x=170, y=240)
        options_2.place(x=170, y=270)

        new_keys.place(x=50, y=210, width=200)

    def close_current_window(self):
        self.destroy()

    def open_file_selection_window(self):

        self._input_file_name = askopenfilename(initialdir="/", title="Select inout file",
                                                filetypes=(("wave files", "*.wav"), ("all files", "*.*")))

        self._output_file_name = self._input_file_name[:-4] + '_translate.wav'

    def open_new_record_window(self):
        self._record_window = Record_Window(self)

    def renew_sub_key(self):
        self.REPLACE = TRUE

    def translate(self):
        _in = self._in_language_sel.get()[-6:-1]
        _out = self._out_language_sel.get()[-6:-1]

        translate = classAudioTranslate.AudioTranslate(self._input_file_name, self._output_file_name, _in, _out)

        translate.run()

# This is the definition of the text translation button


class Text_Window(Toplevel):

    _input_file_name = ''
    _output_file_name = ''

    _msg1 = 'Please select target file with "Select Input File" Button.'
    _msg2 = 'Translated file will be stored  with "_translate" postfix.'
    _msg3 = 'If keys need to renew, enter new keys and press button.'
    _msg4 = 'Mini Translator: Text Translator'

    _language_selection = None
    _new_sub_keys = None

    REPLACE = False

    def __init__(self, master):
        Toplevel.__init__(self)
        self.master = master
        self.init_window()

    def init_window(self):

        self.title("Text Translator")
        self.geometry("400x400")

        button_1 = Button(self, text="Select Input File", command=self.open_file_selection_window, height=3, width=30)
        button_2 = Button(self, text="Translate", command=self.translate, height=3, width=15)
        button_3 = Button(self, text="Return", command=self.close_current_window, height=3, width=15)
        button_4 = Button(self, text="Renew Key", command=self.renew_sub_key, height=1, width=10)

        label_1 = Label(self, text=self._msg1)
        label_2 = Label(self, text=self._msg2)
        label_3 = Label(self, text=self._msg3)
        label_4 = Label(self, text=self._msg4)

        self._language_selection = StringVar()
        self._language_selection.set(OPTIONS_txt[0])
        options = OptionMenu(self, self._language_selection, *OPTIONS_txt)
        options.config(width=27)

        self._new_sub_keys = StringVar()
        new_keys = Entry(self, textvariable=self._new_sub_keys)

        button_1.place(x=50, y=250)
        button_2.place(x=50, y=300)
        button_3.place(x=185, y=300)
        button_4.place(x=250, y=215)

        label_1.place(x=20, y=100)
        label_2.place(x=20, y=120)
        label_3.place(x=20, y=140)
        label_4.place(x=100, y=50)

        options.place(x=50, y=180)
        new_keys.place(x=50, y=210, width=200)

    def open_file_selection_window(self):

        self._input_file_name = askopenfilename(initialdir="/", title="Select inout file",
                                          filetypes=(("text files", "*.txt"), ("all files", "*.*")))

        self._output_file_name = self._input_file_name[:-4] + '_translate.txt'

    def translate(self):
        language = self._language_selection.get()[-3:-1]
        translate = classTextTranslate.TranslateText(language, self._input_file_name, self._output_file_name)

        if self.REPLACE:
            translate.renew_sub_key(self._new_sub_keys.get())

        translate.translate()

    def renew_sub_key(self):
        self.REPLACE = TRUE

    def close_current_window(self):
        self.destroy()


class Record_Window(Toplevel):

    def __init__(self, master):
        Toplevel.__init__(self)
        self.master = master
        self.init_window()

    def init_window(self):
        self.title("Recorder")
        self.geometry("400x400")


main_window_frame = Tk()  # Create the root window
main_window = Main_Window(main_window_frame)  # Create the instance of the root window.
main_window.mainloop()
