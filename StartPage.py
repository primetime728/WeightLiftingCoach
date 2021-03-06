from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from importlib import reload
#import subprocess

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
fontStyle = "Consolas"


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.attributes('-fullscreen', True)
window.geometry("1920x1080")
window.configure(bg="#FFFFFF")


def SelWkt():
    window.destroy()
    #subprocess.run("python3 SelectWorkout.py", shell=True)
    #window.destroy()
    #quit()
    import SelectWorkout
    reload(SelectWorkout)



canvas = Canvas(
    window,
    bg="#264653",
    height=1080,
    width=1920,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_text(
    960.0,
    220.0,
    anchor="center",
    justify="center",
    text="Enhance Your Lift",
    fill="#FFFFFF",
    font=(fontStyle, 48 * -1)
)

canvas.create_text(
    960.0,
    100.0,
    anchor="center",
    text="Smart Lifting",
    fill="#FFFFFF",
    font=(fontStyle, 144 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("Begin.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: SelWkt(),
    relief="flat"
)
button_1.place(
    x=660.0,
    y=627.0,
    width=600.0,
    height=106.0
)

window.resizable(False, False)
window.mainloop()
