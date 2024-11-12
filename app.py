import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

class PatternMaker:
    def __init__(self, root):
        self.root = root
        self.root.title("برنامج رسم باترونات الخياطة")
        
        # إعداد المتغيرات
        self.fabric_width = None
        self.fabric_folded = None
        self.scale_factor = 1.0  # نسبة التكبير والتصغير الافتراضية

        # قم بإنشاء شريط القوائم واستدعاء الوظائف
        self.create_menu()

        # إطار يحتوي على اللوحة وشريط التمرير
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # لوحة الرسم
        self.canvas = tk.Canvas(main_frame, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # مسطرة أفقية
        self.horizontal_ruler = tk.Canvas(main_frame, height=20, bg="lightgray")
        self.horizontal_ruler.pack(fill=tk.X, side=tk.TOP)

        # مسطرة عمودية
        self.vertical_ruler = tk.Canvas(main_frame, width=20, bg="lightgray")
        self.vertical_ruler.pack(fill=tk.Y, side=tk.LEFT)

        # شريط التمرير للتكبير والتصغير
        self.zoom_scale = tk.Scale(root, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, label="تكبير/تصغير")
        self.zoom_scale.set(self.scale_factor)
        self.zoom_scale.pack(fill=tk.X)
        self.zoom_scale.bind("<Motion>", self.update_zoom)

    def create_menu(self):
        menu_bar = tk.Menu(self.root)

        # قائمة ملف
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="جديد", command=self.new_pattern)
        file_menu.add_command(label="فتح", command=self.open_file)
        file_menu.add_command(label="حفظ", command=self.save_file)
        file_menu.add_command(label="حفظ باسم", command=self.save_file_as)
        menu_bar.add_cascade(label="ملف", menu=file_menu)

        # قائمة اجزاء
        parts_menu = tk.Menu(menu_bar, tearoff=0)
        parts_menu.add_command(label="جزء جديد", command=self.new_part)
        parts_menu.add_command(label="استدعاء جزء", command=self.load_part)
        parts_menu.add_command(label="تعديل جزء", command=self.edit_part)
        menu_bar.add_cascade(label="اجزاء", menu=parts_menu)

        # قائمة أدوات
        tools_menu = tk.Menu(menu_bar, tearoff=0)
        tools_menu.add_command(label="ترتيب تلقائي", command=self.auto_arrange)
        menu_bar.add_cascade(label="أدوات", menu=tools_menu)

        # إضافة شريط القوائم إلى النافذة الرئيسية
        self.root.config(menu=menu_bar)

    def new_pattern(self):
        # نافذة إدخال العرض وخيار القماش
        width = simpledialog.askinteger("العرض", "أدخل عرض القماش (سم):")
        if width is not None:
            folded = messagebox.askyesno("خيار القماش", "هل القماش مثني؟")

            # حفظ البيانات والرسم
            self.fabric_width = width
            self.fabric_folded = folded
            self.canvas.delete("all")
            self.update_rulers()
            self.draw_pattern()
        else:
            messagebox.showerror("خطأ", "يجب إدخال العرض بشكل صحيح.")

    def draw_pattern(self):
        # رسم خط يمثل عرض القماش
        scaled_width = self.fabric_width * self.scale_factor
        if self.fabric_width:
            if self.fabric_folded:
                scaled_width /= 2
            # رسم خط أفقي يمثل عرض القماش
            self.canvas.create_line(10, 50, 10 + scaled_width, 50, fill="black", width=2)
            self.canvas.create_text(10 + scaled_width / 2, 60, text="قماش مثني" if self.fabric_folded else "قماش مدة واحدة", fill="blue")

    def update_rulers(self):
        # تحديث المسطرة الأفقية
        self.horizontal_ruler.delete("all")
        ruler_width = self.fabric_width * (0.5 if self.fabric_folded else 1) * self.scale_factor
        for i in range(0, int(ruler_width), 10):
            x = i + 20
            self.horizontal_ruler.create_line(x, 0, x, 10)
            if i % 50 == 0:
                self.horizontal_ruler.create_text(x, 15, text=str(i), anchor="n")

        # تحديث المسطرة العمودية
        self.vertical_ruler.delete("all")
        for i in range(0, 500, 10):  # نضع قياسات وهمية للطول
            y = i + 20
            self.vertical_ruler.create_line(10, y, 20, y)
            if i % 50 == 0:
                self.vertical_ruler.create_text(5, y, text=str(i), anchor="e")

    def update_zoom(self, event=None):
        # تحديث نسبة التكبير/التصغير
        self.scale_factor = self.zoom_scale.get()
        self.canvas.delete("all")
        self.update_rulers()
        self.draw_pattern()

    def open_file(self):
        file_path = filedialog.askopenfilename(title="فتح ملف")
        if file_path:
            # هنا يمكن إضافة كود لتحميل الملف
            messagebox.showinfo("فتح", f"تم فتح الملف: {file_path}")

    def save_file(self):
        # هنا يمكن إضافة كود لحفظ الملف
        messagebox.showinfo("حفظ", "تم حفظ الملف بنجاح.")

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(title="حفظ الملف باسم")
        if file_path:
            # هنا يمكن إضافة كود لحفظ الملف باسم جديد
            messagebox.showinfo("حفظ باسم", f"تم حفظ الملف باسم: {file_path}")

    def new_part(self):
        # نافذة صغيرة لإدخال بيانات الجزء الجديد
        part_name = simpledialog.askstring("جزء جديد", "أدخل اسم الجزء:")
        if part_name:
            messagebox.showinfo("جزء جديد", f"تم إنشاء جزء جديد باسم: {part_name}")

    def load_part(self):
        # هنا يمكن إضافة كود لاستدعاء جزء معين
        messagebox.showinfo("استدعاء جزء", "تم استدعاء جزء.")

    def edit_part(self):
        # هنا يمكن إضافة كود لتعديل جزء معين
        messagebox.showinfo("تعديل جزء", "تم تعديل الجزء.")

    def auto_arrange(self):
        # هنا يمكن إضافة كود لترتيب الأجزاء تلقائياً
        messagebox.showinfo("ترتيب تلقائي", "تم ترتيب الأجزاء تلقائياً.")

# تشغيل البرنامج
if __name__ == "__main__":
    root = tk.Tk()
    app = PatternMaker(root)
    root.geometry("800x600")
    root.mainloop()
