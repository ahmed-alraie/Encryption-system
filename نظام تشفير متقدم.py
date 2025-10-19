# مشروع نظام التشفير المتقدم
# Advanced Encryption System Project

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import base64
import random
import string

class AdvancedEncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("نظام التشفير المتقدم")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        self.encryption_key = ""
        self.setup_ui()
    
    def setup_ui(self):
        """إنشاء واجهة المستخدم"""
        # العنوان الرئيسي
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(main_frame, text="نظام التشفير المتقدم", 
                              font=("Arial", 18, "bold"), fg="darkblue")
        title_label.pack(pady=10)
        
        # إطار المفتاح
        key_frame = ttk.LabelFrame(main_frame, text="إدارة مفتاح التشفير", padding="10")
        key_frame.pack(fill=tk.X, pady=10)
        
        # حقل إدخال المفتاح
        ttk.Label(key_frame, text="مفتاح التشفير:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.key_entry = ttk.Entry(key_frame, width=40, show="*")
        self.key_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # أزرار المفتاح
        key_buttons_frame = ttk.Frame(key_frame)
        key_buttons_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Button(key_buttons_frame, text="تعيين المفتاح", 
                  command=self.set_key).pack(side=tk.LEFT, padx=5)
        ttk.Button(key_buttons_frame, text="إنشاء مفتاح عشوائي", 
                  command=self.generate_key).pack(side=tk.LEFT, padx=5)
        ttk.Button(key_buttons_frame, text="إظهار/إخفاء المفتاح", 
                  command=self.toggle_key_visibility).pack(side=tk.LEFT, padx=5)
        
        # إطار النص الأصلي
        input_frame = ttk.LabelFrame(main_frame, text="النص الأصلي", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.input_text = scrolledtext.ScrolledText(input_frame, height=8, width=80)
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        # إطار أزرار العمليات
        operations_frame = ttk.Frame(main_frame)
        operations_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(operations_frame, text="تشفير النص", 
                  command=self.encrypt_text).pack(side=tk.LEFT, padx=10)
        ttk.Button(operations_frame, text="فك تشفير النص", 
                  command=self.decrypt_text).pack(side=tk.LEFT, padx=10)
        ttk.Button(operations_frame, text="مسح الكل", 
                  command=self.clear_all).pack(side=tk.LEFT, padx=10)
        
        # إطار النص المشفر
        output_frame = ttk.LabelFrame(main_frame, text="النص المشفر / النص بعد فك التشفير", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=8, width=80)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # إطار النسخ
        copy_frame = ttk.Frame(main_frame)
        copy_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(copy_frame, text="نسخ النص المشفر", 
                  command=self.copy_encrypted).pack(side=tk.LEFT, padx=5)
        
        # حالة المفتاح
        self.key_status = tk.Label(main_frame, text="لم يتم تعيين مفتاح", fg="red")
        self.key_status.pack(side=tk.BOTTOM, pady=5)
    
    def set_key(self):
        """تعيين مفتاح التشفير"""
        key = self.key_entry.get().strip()
        if not key:
            messagebox.showwarning("تحذير", "يرجى إدخال مفتاح التشفير")
            return
        
        self.encryption_key = key
        self.key_status.config(text=f"تم تعيين المفتاح ({len(key)} حرف)", fg="green")
        messagebox.showinfo("نجاح", "تم تعيين مفتاح التشفير بنجاح")
    
    def generate_key(self):
        """إنشاء مفتاح عشوائي"""
        key_length = 12
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        new_key = ''.join(random.choice(characters) for _ in range(key_length))
        
        self.key_entry.delete(0, tk.END)
        self.key_entry.insert(0, new_key)
        self.encryption_key = new_key
        self.key_status.config(text=f"تم إنشاء مفتاح جديد ({key_length} حرف)", fg="green")
        messagebox.showinfo("نجاح", f"تم إنشاء مفتاح جديد: {new_key}")
    
    def toggle_key_visibility(self):
        """تبديل إظهار/إخفاء المفتاح"""
        current_show = self.key_entry.cget('show')
        if current_show == '*':
            self.key_entry.config(show='')
        else:
            self.key_entry.config(show='*')
    
    def encrypt_text(self):
        """تشفير النص"""
        if not self.encryption_key:
            messagebox.showerror("خطأ", "يرجى تعيين مفتاح التشفير أولاً")
            return
        
        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("تحذير", "يرجى إدخال نص للتشفير")
            return
        
        try:
            # إضافة المفتاح للنص
            combined = self.encryption_key + text
            
            # تحويل إلى bytes ثم تشفير base64
            encoded_bytes = base64.b64encode(combined.encode('utf-8'))
            encrypted_text = encoded_bytes.decode('utf-8')
            
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", encrypted_text)
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء التشفير: {str(e)}")
    
    def decrypt_text(self):
        """فك تشفير النص"""
        if not self.encryption_key:
            messagebox.showerror("خطأ", "يرجى تعيين مفتاح التشفير أولاً")
            return
        
        encrypted_text = self.input_text.get("1.0", tk.END).strip()
        if not encrypted_text:
            messagebox.showwarning("تحذير", "يرجى إدخال نص مشفر لفك التشفير")
            return
        
        try:
            # فك تشفير base64
            decoded_bytes = base64.b64decode(encrypted_text.encode('utf-8'))
            decoded_text = decoded_bytes.decode('utf-8')
            
            # إزالة المفتاح من النص
            if decoded_text.startswith(self.encryption_key):
                original_text = decoded_text[len(self.encryption_key):]
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert("1.0", original_text)
            else:
                messagebox.showerror("خطأ", "المفتاح غير صحيح أو النص تالف")
                
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء فك التشفير: {str(e)}")
    
    def clear_all(self):
        """مسح جميع الحقول"""
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
        self.key_entry.delete(0, tk.END)
        self.encryption_key = ""
        self.key_status.config(text="لم يتم تعيين مفتاح", fg="red")
    
    def copy_encrypted(self):
        """نسخ النص المشفر إلى الحافظة"""
        encrypted = self.output_text.get("1.0", tk.END).strip()
        if encrypted:
            self.root.clipboard_clear()
            self.root.clipboard_append(encrypted)
            messagebox.showinfo("نجاح", "تم نسخ النص المشفر إلى الحافظة")
        else:
            messagebox.showwarning("تحذير", "لا يوجد نص مشفر للنسخ")

def main():
    root = tk.Tk()
    app = AdvancedEncryptionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()