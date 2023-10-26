import customtkinter
import TeamAssigner as module

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

def toggle_text_field():
    if checkbox.get() == 1:
        maxTeams.grid(row=2, column=0, pady=12, padx=10)
    else:
        maxTeams.grid_forget()

root = customtkinter.CTk()
root.title("Sci Oly Team Assigner")
root.geometry("500x350")

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)
label = customtkinter.CTkLabel(master=frame, text="Sci Oly Team Assigner", font=("Arial", 20))
label.grid(row=0, column=0, pady=12, padx=10)

checkbox = customtkinter.CTkCheckBox(master=frame, text="Remove low preference teams if max teams reached", command=toggle_text_field)
checkbox.grid(row=1, column=0, pady=12, padx=10)

maxTeams = customtkinter.CTkEntry(master=frame, placeholder_text="Max Teams for each Event")
maxTeams.configure(width=170)  # Adjust the width as needed

button = customtkinter.CTkButton(master=frame, text="Assign Teams", command=lambda: module.main(checkbox.get(), maxTeams.get()))
button.grid(row=3, column=0, pady=12, padx=10)

root.mainloop()
