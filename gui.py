import tkinter as tk
from master import Master

class MasterGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Servidor Master - Sistema Distribuído")

        tk.Label(self.root, text="🧠 Servidor Master Ativo").pack(pady=5)
        self.log_box = tk.Text(self.root, height=20, width=60)
        self.log_box.pack(padx=10, pady=10)

        self.master = Master(log_callback=self.adicionar_log)

        self.root.mainloop()

    def adicionar_log(self, mensagem):
        self.log_box.insert(tk.END, mensagem + "\n")
        self.log_box.see(tk.END)

if __name__ == "__main__":
    MasterGUI()
