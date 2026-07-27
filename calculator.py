import customtkinter as ctk
import math
import ast
import operator as op

# Konfigurasi Tema Utama
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class SafeEvaluator:
    """Evaluator ekspresi matematika berbasis AST tanpa eksekusi eval() yang berbahaya"""
    def __init__(self, is_deg=True):
        self.is_deg = is_deg
        self.operators = {
            ast.Add: op.add,
            ast.Sub: op.sub,
            ast.Mult: op.mul,
            ast.Div: op.truediv,
            ast.Pow: op.pow,
            ast.USub: op.neg,
            ast.UAdd: op.pos,
        }

    def eval(self, expr_str: str):
        clean_expr = (
            expr_str.replace("×", "*")
            .replace("÷", "/")
            .replace("^", "**")
            .replace("π", "math.pi")
            .replace("e", "math.e")
        )
        try:
            node = ast.parse(clean_expr, mode='eval')
            return self._eval_node(node.body)
        except ZeroDivisionError:
            raise ZeroDivisionError("Cannot divide by zero")
        except Exception:
            raise ValueError("Ekspresi Tidak Valid")

    def _eval_node(self, node):
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op_type = type(node.op)
            if op_type in self.operators:
                if op_type == ast.Div and right == 0:
                    raise ZeroDivisionError("Cannot divide by zero")
                return self.operators[op_type](left, right)
            raise ValueError("Operator Tidak Didukung")
        elif isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            op_type = type(node.op)
            if op_type in self.operators:
                return self.operators[op_type](operand)
            raise ValueError("Operator Unary Tidak Didukung")
        elif isinstance(node, ast.Call):
            func_name = node.func.id if isinstance(node.func, ast.Name) else None
            args = [self._eval_node(arg) for arg in node.args]
            return self._eval_func(func_name, args)
        elif isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name) and node.value.id == "math":
                return getattr(math, node.attr)
            raise ValueError("Atribut Tidak Diizinkan")
        elif isinstance(node, ast.Name):
            if node.id == "pi":
                return math.pi
            elif node.id == "e":
                return math.e
            raise ValueError(f"Variabel {node.id} Tidak Dikenal")
        else:
            raise ValueError("Sintaks Tidak Didukung")

    def _eval_func(self, name, args):
        if not args:
            raise ValueError("Argumen Fungsi Kosong")
        val = args[0]
        if name in ["sin", "cos", "tan"]:
            rad_val = math.radians(val) if self.is_deg else val
            if name == "sin": return math.sin(rad_val)
            if name == "cos": return math.cos(rad_val)
            if name == "tan": return math.tan(rad_val)
        elif name == "log":
            return math.log10(val)
        elif name == "ln":
            return math.log(val)
        elif name == "sqrt":
            if val < 0: raise ValueError("Domain Error")
            return math.sqrt(val)
        elif name == "fact":
            if val < 0 or not float(val).is_integer(): raise ValueError("Domain Error")
            return math.factorial(int(val))
        raise ValueError(f"Fungsi {name} Tidak Didukung")


class AdvancedCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Advanced Calculator")
        self.geometry("420x680")
        self.resizable(False, False)

        # Application State
        self.expression = ""
        self.memory = 0.0
        self.is_deg = True
        self.evaluator = SafeEvaluator(is_deg=self.is_deg)

        # Palette Palette
        self.BG_COLOR = "#181825"
        self.DISPLAY_BG = "#1E1E2E"
        self.BTN_NUM_BG = "#313244"
        self.BTN_NUM_HOVER = "#45475A"
        self.BTN_FUNC_BG = "#45475A"
        self.BTN_FUNC_HOVER = "#585B70"
        self.BTN_ACCENT_BG = "#89B4FA"
        self.BTN_ACCENT_HOVER = "#B4BEFE"
        self.BTN_OP_HOVER = "#EBA0AC"
        self.TEXT_MAIN = "#CDD6F4"
        self.TEXT_MUTED = "#A6ADC8"

        self.configure(fg_color=self.BG_COLOR)

        self._create_ui()
        self._bind_keyboard()

    def _create_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header Bar
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 5))

        self.deg_btn = ctk.CTkButton(
            top_bar, text="DEG", width=50, height=26, corner_radius=6,
            fg_color="#313244", text_color="#89B4FA", font=("Inter", 11, "bold"),
            command=self._toggle_deg_rad
        )
        self.deg_btn.pack(side="left")

        ctk.CTkLabel(
            top_bar, text="SCIENTIFIC", font=("Inter", 11, "bold"), text_color=self.TEXT_MUTED
        ).pack(side="right")

        # Display Frame (Dual Line)
        display_frame = ctk.CTkFrame(self, fg_color=self.DISPLAY_BG, corner_radius=12)
        display_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        display_frame.grid_columnconfigure(0, weight=1)

        self.sub_display = ctk.CTkLabel(
            display_frame, text="", font=("Inter", 13), text_color=self.TEXT_MUTED, anchor="e"
        )
        self.sub_display.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 0))

        self.main_display = ctk.CTkLabel(
            display_frame, text="0", font=("Inter", 32, "bold"), text_color=self.TEXT_MAIN, anchor="e"
        )
        self.main_display.grid(row=1, column=0, sticky="ew", padx=15, pady=(5, 15))

        # Memory Register Bar
        mem_bar = ctk.CTkFrame(self, fg_color="transparent")
        mem_bar.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 5))

        mem_btns = [("MC", self._mem_clear), ("MR", self._mem_recall), ("M+", self._mem_add), ("M-", self._mem_sub)]
        for label, cmd in mem_btns:
            ctk.CTkButton(
                mem_bar, text=label, width=45, height=24, corner_radius=6,
                fg_color="transparent", hover_color="#313244",
                text_color=self.TEXT_MUTED, font=("Inter", 11), command=cmd
            ).pack(side="left", expand=True)

        # Keypad Layout (Grid 5 Kolom)
        keypad = ctk.CTkFrame(self, fg_color="transparent")
        keypad.grid(row=3, column=0, sticky="nsew", padx=20, pady=(5, 20))

        for col in range(5):
            keypad.grid_columnconfigure(col, weight=1)

        buttons = [
            ("sin", 0, 0, "func", lambda: self._append_func("sin")),
            ("cos", 0, 1, "func", lambda: self._append_func("cos")),
            ("tan", 0, 2, "func", lambda: self._append_func("tan")),
            ("π", 0, 3, "func", lambda: self._append_symbol("π")),
            ("AC", 0, 4, "op", self._clear_all),

            ("log", 1, 0, "func", lambda: self._append_func("log")),
            ("ln", 1, 1, "func", lambda: self._append_func("ln")),
            ("√", 1, 2, "func", lambda: self._append_func("sqrt")),
            ("^", 1, 3, "func", lambda: self._append_symbol("^")),
            ("⌫", 1, 4, "op", self._backspace),

            ("(", 2, 0, "func", lambda: self._append_symbol("(")),
            (")", 2, 1, "func", lambda: self._append_symbol(")")),
            ("x!", 2, 2, "func", lambda: self._append_func("fact")),
            ("÷", 2, 3, "func", lambda: self._append_symbol("÷")),
            ("%", 2, 4, "func", self._percent),

            ("7", 3, 0, "num", lambda: self._append_symbol("7")),
            ("8", 3, 1, "num", lambda: self._append_symbol("8")),
            ("9", 3, 2, "num", lambda: self._append_symbol("9")),
            ("×", 3, 3, "func", lambda: self._append_symbol("×")),
            ("e", 3, 4, "func", lambda: self._append_symbol("e")),

            ("4", 4, 0, "num", lambda: self._append_symbol("4")),
            ("5", 4, 1, "num", lambda: self._append_symbol("5")),
            ("6", 4, 2, "num", lambda: self._append_symbol("6")),
            ("-", 4, 3, "func", lambda: self._append_symbol("-")),
            ("+/-", 4, 4, "func", self._toggle_sign),

            ("1", 5, 0, "num", lambda: self._append_symbol("1")),
            ("2", 5, 1, "num", lambda: self._append_symbol("2")),
            ("3", 5, 2, "num", lambda: self._append_symbol("3")),
            ("+", 5, 3, "func", lambda: self._append_symbol("+")),

            ("0", 6, 0, "num", lambda: self._append_symbol("0")),
            (".", 6, 2, "num", lambda: self._append_symbol(".")),
            ("=", 6, 3, "accent", self._calculate),
        ]

        for text, r, c, btype, cmd in buttons:
            kwargs = self._get_button_style(btype)
            c_span = 2 if text in ["0", "="] else 1
            if text == ".": c = 2
            elif text == "=": c = 3

            btn = ctk.CTkButton(keypad, text=text, command=cmd, **kwargs)
            btn.grid(row=r, column=c, columnspan=c_span, padx=3, pady=3, sticky="nsew")

    def _get_button_style(self, btype):
        base = {"height": 42, "corner_radius": 8, "font": ("Inter", 14, "bold")}
        if btype == "num":
            return {**base, "fg_color": self.BTN_NUM_BG, "hover_color": self.BTN_NUM_HOVER, "text_color": self.TEXT_MAIN}
        elif btype == "func":
            return {**base, "fg_color": self.BTN_FUNC_BG, "hover_color": self.BTN_FUNC_HOVER, "text_color": self.TEXT_MAIN}
        elif btype == "op":
            return {**base, "fg_color": "#45475A", "hover_color": self.BTN_OP_HOVER, "text_color": "#F38BA8"}
        elif btype == "accent":
            return {**base, "fg_color": self.BTN_ACCENT_BG, "hover_color": self.BTN_ACCENT_HOVER, "text_color": "#11111B"}

    def _append_symbol(self, sym):
        if self.main_display.cget("text") in ["Error", "Domain Error", "Cannot divide by zero"]:
            self.expression = ""
        self.expression += str(sym)
        self._update_display()

    def _append_func(self, func_name):
        if self.main_display.cget("text") in ["Error", "Domain Error", "Cannot divide by zero"]:
            self.expression = ""
        self.expression += f"{func_name}("
        self._update_display()

    def _clear_all(self):
        self.expression = ""
        self.sub_display.configure(text="")
        self.main_display.configure(text="0")

    def _backspace(self):
        if self.expression:
            self.expression = self.expression[:-1]
            self._update_display()

    def _toggle_sign(self):
        if self.expression:
            self.expression = self.expression[1:] if self.expression.startswith("-") else "-" + self.expression
            self._update_display()

    def _percent(self):
        try:
            val = float(self.expression) / 100.0
            self.expression = str(val)
            self._update_display()
        except Exception:
            pass

    def _toggle_deg_rad(self):
        self.is_deg = not self.is_deg
        self.evaluator.is_deg = self.is_deg
        self.deg_btn.configure(text="DEG" if self.is_deg else "RAD")

    def _update_display(self):
        self.main_display.configure(text=self.expression if self.expression else "0")

    def _calculate(self):
        if not self.expression: return
        try:
            res = self.evaluator.eval(self.expression)
            if isinstance(res, float):
                res = int(res) if res.is_integer() else round(res, 8)
            self.sub_display.configure(text=f"{self.expression} =")
            self.main_display.configure(text=str(res))
            self.expression = str(res)
        except ZeroDivisionError:
            self.main_display.configure(text="Cannot divide by zero")
            self.expression = ""
        except ValueError as e:
            self.main_display.configure(text=str(e))
            self.expression = ""

    def _mem_clear(self): self.memory = 0.0
    def _mem_recall(self): self._append_symbol(str(self.memory))
    def _mem_add(self):
        try: self.memory += float(self.main_display.cget("text"))
        except ValueError: pass
    def _mem_sub(self):
        try: self.memory -= float(self.main_display.cget("text"))
        except ValueError: pass

    def _bind_keyboard(self):
        self.bind("<Return>", lambda e: self._calculate())
        self.bind("<BackSpace>", lambda e: self._backspace())
        self.bind("<Escape>", lambda e: self._clear_all())
        for char in "0123456789.+-*/()":
            mapped = "×" if char == "*" else ("÷" if char == "/" else char)
            self.bind(char, lambda e, c=mapped: self._append_symbol(c))


if __name__ == "__main__":
    app = AdvancedCalculator()
    app.mainloop()