import tkinter as tk
from tkinter import messagebox
import re
import string
import math

# Core logic: Analyze password strength
def analyze_password(password):
    score = 0
    recommendations = []

    length = len(password)
    has_upper = bool(re.search(r"[A-Z]", password))
    has_lower = bool(re.search(r"[a-z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_special = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))

    if length >= 12:
        score += 2
    elif length >= 8:
        score += 1
    else:
        recommendations.append("Use at least 12 characters.")

    if has_upper: score += 1
    else: recommendations.append("Add uppercase letters.")

    if has_lower: score += 1
    else: recommendations.append("Add lowercase letters.")

    if has_digit: score += 1
    else: recommendations.append("Add numbers.")

    if has_special: score += 1
    else: recommendations.append("Use special characters (e.g. !, @, #).")

    entropy = calculate_entropy(password)
    if entropy >= 60:
        score += 1
    else:
        recommendations.append("Increase character variety to improve entropy.")

    if score >= 7:
        strength = "Strong"
    elif score >= 4:
        strength = "Moderate"
    else:
        strength = "Weak"

    return strength, recommendations

# Helper function to calculate entropy
def calculate_entropy(password):
    charset = 0
    if re.search(r"[a-z]", password): charset += 26
    if re.search(r"[A-Z]", password): charset += 26
    if re.search(r"\d", password): charset += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): charset += len(string.punctuation)

    if charset == 0:
        return 0

    entropy = len(password) * math.log2(charset)
    return round(entropy, 2)

# GUI application
class PasswordAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Analyzer")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.label = tk.Label(root, text="Enter your password:", font=("Arial", 12))
        self.label.pack(pady=10)

        self.entry = tk.Entry(root, width=30, font=("Arial", 12))
        self.entry.pack(pady=5)

        self.button = tk.Button(root, text="Analyze", command=self.check_password, font=("Arial", 12))
        self.button.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
        self.result_label.pack(pady=10)

        self.tips_label = tk.Label(root, text="", font=("Arial", 10), wraplength=350, justify="left")
        self.tips_label.pack()

    def check_password(self):
        password = self.entry.get()
        if not password:
            messagebox.showwarning("Input Required", "Please enter a password.")
            return

        strength, tips = analyze_password(password)
        self.result_label.config(text=f"Strength: {strength}")

        if tips:
            formatted_tips = "\n- " + "\n- ".join(tips)
            self.tips_label.config(text=f"Suggestions:{formatted_tips}")
        else:
            self.tips_label.config(text="Your password looks good!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordAnalyzerApp(root)
    root.mainloop()
