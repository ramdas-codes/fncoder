import tkinter as ui
import time

window = ui.Tk()


def update_clock():
    hours = time.strftime("%I")
    minutes = time.strftime("%M")
    seconds = time.strftime("%S")
    am_or_pm = time.strftime("%p")
    time_text = hours + ":" + minutes + ":" + seconds + " " + am_or_pm
    digital_clock_lbl.config(text=time_text)
    digital_clock_lbl.after(1000, update_clock)


digital_clock_lbl = ui.Label(window, text="00:00:00", font="Helvetica 72 bold")
digital_clock_lbl.pack()

update_clock()

window.mainloop()
