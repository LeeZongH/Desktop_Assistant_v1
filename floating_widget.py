# Zong-Hua Li 2026/06/20
import tkinter as tk
from tkinter import messagebox
import datetime
import platform

class FloatingWidget:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Assistant")
        
        self.os_system = platform.system()
        if self.os_system == "Windows":
            self.root.overrideredirect(True)
        elif self.os_system == "Linux":
            self.root.attributes('-type', 'splash')
            
        self.root.attributes("-topmost", True)
        self.root.geometry("250x350+100+100")
        self.root.configure(bg="#2E3440")

        self.is_minimized = False
        self.rest_interval = 0
        self.alarm_time = ""

        self.setup_ui()
        self.setup_drag()
        self.check_time()

    def setup_ui(self):
        self.title_bar = tk.Frame(self.root, bg="#4C566A", relief="raised", bd=0)
        self.title_bar.pack(expand=0, fill="x")
        
        tk.Label(self.title_bar, text="Desktop Assistant", bg="#4C566A", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        
        close_btn = tk.Button(self.title_bar, text="X", bg="#BF616A", fg="white", bd=0, command=self.root.destroy, width=2)
        close_btn.pack(side="right", padx=2, pady=2)

        self.min_btn = tk.Button(self.title_bar, text="—", bg="#EBCB8B", fg="black", bd=0, command=self.toggle_minimize, width=2)
        self.min_btn.pack(side="right", padx=2, pady=2)

        self.content_frame = tk.Frame(self.root, bg="#2E3440")
        self.content_frame.pack(fill="both", expand=True)

        tk.Label(self.content_frame, text="Temporary notes:", bg="#2E3440", fg="#D8DEE9").pack(anchor="w", padx=5, pady=(5,0))
        self.text_pad = tk.Text(self.content_frame, height=6, bg="#3B4252", fg="#ECEFF4", insertbackground="white", bd=0)
        self.text_pad.pack(fill="x", padx=5, pady=2)
        
        self.text_pad.bind("<Button-1>", lambda e: self.text_pad.focus_force())

        alarm_frame = tk.Frame(self.content_frame, bg="#2E3440")
        alarm_frame.pack(fill="x", padx=5, pady=5)
        tk.Label(alarm_frame, text="Reminder (HH:MM):", bg="#2E3440", fg="#D8DEE9").pack(side="left")
        self.alarm_entry = tk.Entry(alarm_frame, width=6, bg="#3B4252", fg="#ECEFF4", bd=0)
        self.alarm_entry.pack(side="left", padx=5)
        tk.Button(alarm_frame, text="Set", bg="#5E81AC", fg="white", bd=0, command=self.set_alarm).pack(side="left")
        
        self.alarm_entry.bind("<Button-1>", lambda e: self.alarm_entry.focus_force())

        rest_frame = tk.Frame(self.content_frame, bg="#2E3440")
        rest_frame.pack(fill="x", padx=5, pady=5)
        tk.Label(rest_frame, text="Interval (minutes):", bg="#2E3440", fg="#D8DEE9").pack(side="left")
        self.rest_entry = tk.Entry(rest_frame, width=5, bg="#3B4252", fg="#ECEFF4", bd=0)
        self.rest_entry.pack(side="left", padx=5)
        tk.Button(rest_frame, text="Start", bg="#A3BE8C", fg="black", bd=0, command=self.set_rest).pack(side="left")
        
        self.rest_entry.bind("<Button-1>", lambda e: self.rest_entry.focus_force())

    def toggle_minimize(self):
        if not self.is_minimized:
            self.content_frame.pack_forget()
            self.root.geometry("250x26")
            self.min_btn.config(text="□")
            self.is_minimized = True
        else:
            self.content_frame.pack(fill="both", expand=True)
            self.root.geometry("250x350")
            self.min_btn.config(text="—")
            self.is_minimized = False

    def setup_drag(self):
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def set_alarm(self):
        self.alarm_time = self.alarm_entry.get().strip()
        messagebox.showinfo("設定成功", f"將於 {self.alarm_time} 提醒您！")

    def set_rest(self):
        try:
            minutes = int(self.rest_entry.get().strip())
            if minutes <= 0:
                messagebox.showerror("錯誤", "時間必須大於 0 分鐘！")
                return
            self.rest_interval = minutes * 60 * 1000 # 轉換為毫秒
            self.root.after(self.rest_interval, self.trigger_rest)
            messagebox.showinfo("設定成功", f"每 {minutes} 分鐘提醒您休息！")
        except ValueError:
            messagebox.showerror("錯誤", "請輸入有效的數字")

    def trigger_rest(self):
        messagebox.showwarning("休息時間", "工作辛苦了！站起來走走，喝杯水吧！")
        if self.rest_interval > 0:
            self.root.after(self.rest_interval, self.trigger_rest)

    def check_time(self):
        if self.alarm_time:
            current_time = datetime.datetime.now().strftime("%H:%M")
            if current_time == self.alarm_time:
                self.alarm_time = ""
                self.alarm_entry.delete(0, tk.END)
                
                if self.is_minimized:
                    self.toggle_minimize()
                
                messagebox.showinfo("時間到！", "您設定的提醒時間到了！")

        self.root.after(1000, self.check_time)

if __name__ == "__main__":
    root = tk.Tk()
    app = FloatingWidget(root)
    root.mainloop()