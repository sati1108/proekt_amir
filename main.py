import tkinter as tk
from tkinter import messagebox, Listbox
import requests
import json
import os

class GitHubUserFinder:
    def __init__(self, master):
        self.master = master
        master.title("GitHub User Finder")

        self.label = tk.Label(master, text="Введите имя пользователя GitHub:")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.search_button = tk.Button(master, text="Поиск", command=self.search_user)
        self.search_button.pack()

        self.listbox = Listbox(master)
        self.listbox.pack()

        self.favorites_button = tk.Button(master, text="Добавить в избранное", command=self.add_to_favorites)
        self.favorites_button.pack()

        self.load_favorites()

    def search_user(self):
        username = self.entry.get()
        if not username:
            messagebox.showwarning("Ошибка", "Поле поиска не должно быть пустым.")
            return

        response = requests.get(f"https://api.github.com/users/{username}")
        if response.status_code == 200:
            user_data = response.json()
            self.listbox.delete(0, tk.END)
            self.listbox.insert(tk.END, f"{user_data['login']} - {user_data['html_url']}")
        else:
            messagebox.showerror("Ошибка", "Пользователь не найден.")

    def add_to_favorites(self):
        selected_user = self.listbox.curselection()
        if not selected_user:
            messagebox.showwarning("Ошибка", "Выберите пользователя для добавления в избранное.")
            return

        user_info = self.listbox.get(selected_user)
        username = user_info.split(" - ")[0]
        
        favorites = self.load_favorites()
        if username not in favorites:
            favorites.append(username)
            with open('favorites.json', 'w') as f:
                json.dump(favorites, f)
            messagebox.showinfo("Успех", f"{username} добавлен в избранное.")
        else:
            messagebox.showinfo("Информация", f"{username} уже в избранных.")

    def load_favorites(self):
        if os.path.exists('favorites.json'):
            with open('favorites.json', 'r') as f:
                return json.load(f)
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubUserFinder(root)
    root.mainloop()
