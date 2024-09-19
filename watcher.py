import tkinter as tk
from tkinter import scrolledtext, messagebox
import openai
import subprocess
import sys
import time
import re  # Regex kutubxonasini import qilish

# OpenAI API kalitini o'rnatish
openai.api_key = "sk-z1CQz307MliZm1AsomzCD3kUxhqJYd1v0Fvzoe_S-qT3BlbkFJxOcLyWcZXyJW_suM-k_7OqivsZyJIRW9ND_NdxB4wA"

def generate_code(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Foydalanuvchi so'ragan buyruq asosida faqat to'liq va sintaksis jihatidan to'g'ri Python kodini yozing. Hech qanday izoh, markdown formatlari yoki matn yozmang, faqat toza kod yozing."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message['content'].strip()
    except openai.error.APIConnectionError as e:
        messagebox.showerror("Xato", f"OpenAI API bilan aloqa qilishda xato yuz berdi: {e}")
        print("Biroz kutib, yana sinab ko'riladi...")
        time.sleep(5)  # 5 soniya kutib, yana urinish
        return generate_code(prompt)
    except Exception as e:
        messagebox.showerror("Xato", f"Xato yuz berdi: {e}")
        return None

def write_target_script(code):
    if code:  # Kodning mavjudligini tekshirish
        with open('target_script.py', 'w') as f:
            f.write(code)

def install_module(module_name):
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", module_name], check=True)
        messagebox.showinfo("Ma'lumot", f"'{module_name}' moduli muvaffaqiyatli o'rnatildi.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Xato", f"Modulni o'rnatishda xato yuz berdi: {e}")

def run_target_script():
    try:
        subprocess.run([sys.executable, 'target_script.py'], check=True)
        messagebox.showinfo("Ma'lumot", "target_script.py muvaffaqiyatli ishga tushirildi.")
    except subprocess.CalledProcessError as e:
        stderr_output = e.stderr.decode() if e.stderr else "Aniqlanmagan xato yuz berdi."
        display_advice_from_gpt(stderr_output)

def display_advice_from_gpt(error_message):
    advice = generate_code(f"Kodda xato bor. Bu xato: {error_message}. Uni qanday tuzatish mumkin?")
    if advice:
        # Terminalda bajarilishi kerak bo'lgan buyruqlarni ajratish
        terminal_commands = re.findall(r'(pip install [\w\-]+)', advice)  # Faqat pip install buyruqlarini ajratib olish
        
        output_text.delete(1.0, tk.END)  # O'ng panelni tozalash
        if terminal_commands:
            for command in terminal_commands:
                output_text.insert(tk.END, command + "\n")
        else:
            output_text.insert(tk.END, "Terminalda bajarilishi kerak bo'lgan buyruq topilmadi.\n")

def on_send_command():
    command = input_text.get("1.0", tk.END).strip()
    if command:
        code = generate_code(command)
        if code:
            write_target_script(code)
            messagebox.showinfo("Ma'lumot", "Yangi kod target_script.py fayliga yozildi.")

def on_run_file():
    run_target_script()

# Tkinter interfeysi
root = tk.Tk()
root.title("GPT-4 Buyruq va Faylni Boshqarish")

# Buyruq kiritish maydoni (chap tomon)
input_text = scrolledtext.ScrolledText(root, height=10, width=50)
input_text.grid(row=0, column=0, padx=10, pady=10)

# Buyruqni yuborish tugmasi
send_button = tk.Button(root, text="Buyruqni yuborish", command=on_send_command)
send_button.grid(row=1, column=0, padx=10, pady=10)

# Faylni yurgazish tugmasi
run_button = tk.Button(root, text="Faylni yurgazish", command=on_run_file)
run_button.grid(row=2, column=0, padx=10, pady=10)

# Xato va tavsiyalar uchun maydon (o'ng tomon)
output_text = scrolledtext.ScrolledText(root, height=10, width=50)
output_text.grid(row=0, column=1, rowspan=3, padx=10, pady=10)

# Dastur oynasini ko'rsatish
root.mainloop()
