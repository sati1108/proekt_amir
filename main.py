import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os

FAVORITES_FILE = "favorites.json"

class GitHubFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub User Finder")
        self.root.geometry("400x500")

        self.favorites = self.load_favorites()

        # Интерфейс
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Введите логин GitHub:").pack(fill="x")
        
        self.search_entry = ttk.Entry(main_frame)
        self.search_entry.pack(fill="x", pady=5)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=5)
        
        ttk.Button(btn_frame, text="Найти", command=self.search_user).pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(btn_frame, text="В избранное", command=self.add_to_favorites).pack(side="left", expand=True, fill="x", padx=2)

        # Список результатов/избранного
        self.results_list = tk.Listbox(main_frame, height=15)
        self.results_list.pack(fill="both", expand=True, pady=10)
        
        ttk.Button(main_frame, text="Показать избранное", command=self.show_favorites).pack(fill="x")

    def search_user(self):
        username = self.search_entry.get().strip()
        if not username:
            messagebox.showwarning("Внимание", "Поле поиска не должно быть пустым!")
            return

        response = requests.get(f"https://github.com{username}")
        
        self.results_list.delete(0, tk.END)
        if response.status_code == 200:
            data = response.json()
            self.results_list.insert(tk.END, f"Логин: {data['login']}")
            self.results_list.insert(tk.END, f"Имя: {data.get('name') or 'Не указано'}")
            self.results_list.insert(tk.END, f"Репозитории: {data['public_repos']}")
            self.results_list.insert(tk.END, f"Ссылка: {data['html_url']}")
        else:
            self.results_list.insert(tk.END, "Пользователь не найден")

    def load_favorites(self):
        if os.path.exists(FAVORITES_FILE):
            with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def add_to_favorites(self):
        username = self.search_entry.get().strip()
        if username and username not in self.favorites:
            self.favorites.append(username)
            with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
                json.dump(self.favorites, f, indent=4)
            messagebox.showinfo("Успех", f"{username} добавлен в избранное")

    def show_favorites(self):
        self.results_list.delete(0, tk.END)
        self.results_list.insert(tk.END, "-- ИЗБРАННЫЕ ПОЛЬЗОВАТЕЛИ --")
        for user in self.favorites:
            self.results_list.insert(tk.END, user)

if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubFinder(root)
    root.mainloop()
