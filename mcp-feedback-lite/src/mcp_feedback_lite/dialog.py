import sys
import tkinter as tk
from tkinter import scrolledtext

if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

COLORS = {
    "bg": "#1e1e2e",
    "surface": "#313244",
    "border": "#45475a",
    "text": "#cdd6f4",
    "subtext": "#a6adc8",
    "accent": "#89b4fa",
    "green": "#a6e3a1",
    "red": "#f38ba8",
    "yellow": "#f9e2af",
}

FONT = "Segoe UI" if sys.platform == "win32" else "Helvetica"


class FeedbackDialog:
    def __init__(self, summary: str, project_directory: str, timeout: int = 600):
        self.summary = summary
        self.project_directory = project_directory
        self.timeout = timeout
        self.feedback = ""
        self._timeout_id = None
        self._remaining = timeout

    def show(self) -> str:
        self.root = tk.Tk()
        self.root.title("MCP Feedback")
        self.root.configure(bg=COLORS["bg"])
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        w, h = 720, 580
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.minsize(520, 420)
        self.root.attributes("-topmost", True)

        self._build_ui()
        self._start_timer()
        self.input_text.focus_set()

        self.root.mainloop()
        return self.feedback

    # ── UI construction ──────────────────────────────────────────

    def _build_ui(self):
        main = tk.Frame(self.root, bg=COLORS["bg"], padx=16, pady=12)
        main.pack(fill=tk.BOTH, expand=True)

        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(2, weight=3)   # summary area  60%
        main.grid_rowconfigure(5, weight=2)   # input area    40%

        row = 0

        # ── header ──
        header = tk.Frame(main, bg=COLORS["bg"])
        header.grid(row=row, column=0, sticky="ew", pady=(0, 10))
        tk.Label(
            header, text=self.project_directory,
            bg=COLORS["bg"], fg=COLORS["subtext"],
            font=(FONT, 9), anchor="w",
        ).pack(side=tk.LEFT)
        self.timer_label = tk.Label(
            header, bg=COLORS["bg"], fg=COLORS["yellow"], font=(FONT, 9),
        )
        self.timer_label.pack(side=tk.RIGHT)
        row += 1

        # ── summary label ──
        tk.Label(
            main, text="  AI 工作摘要",
            bg=COLORS["bg"], fg=COLORS["accent"],
            font=(FONT, 11, "bold"), anchor="w",
        ).grid(row=row, column=0, sticky="w", pady=(0, 4))
        row += 1

        # ── summary text (read-only) ──
        sf = tk.Frame(main, bg=COLORS["border"])
        sf.grid(row=row, column=0, sticky="nsew", pady=(0, 14))
        sf.grid_rowconfigure(0, weight=1)
        sf.grid_columnconfigure(0, weight=1)

        self.summary_text = scrolledtext.ScrolledText(
            sf, wrap=tk.WORD,
            bg=COLORS["surface"], fg=COLORS["text"],
            font=(FONT, 10),
            insertbackground=COLORS["text"],
            selectbackground=COLORS["accent"],
            borderwidth=0, highlightthickness=0,
            padx=10, pady=8,
        )
        self.summary_text.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        self.summary_text.insert("1.0", self.summary)
        self.summary_text.configure(state=tk.DISABLED)
        row += 1

        # ── separator ──
        tk.Frame(main, bg=COLORS["border"], height=1).grid(
            row=row, column=0, sticky="ew", pady=(0, 14),
        )
        row += 1

        # ── input label ──
        tk.Label(
            main, text="  请输入下一步指令",
            bg=COLORS["bg"], fg=COLORS["green"],
            font=(FONT, 11, "bold"), anchor="w",
        ).grid(row=row, column=0, sticky="w", pady=(0, 4))
        row += 1

        # ── input text (editable) ──
        inf = tk.Frame(main, bg=COLORS["border"])
        inf.grid(row=row, column=0, sticky="nsew", pady=(0, 8))
        inf.grid_rowconfigure(0, weight=1)
        inf.grid_columnconfigure(0, weight=1)

        self.input_text = scrolledtext.ScrolledText(
            inf, wrap=tk.WORD,
            bg=COLORS["surface"], fg=COLORS["text"],
            font=(FONT, 10),
            insertbackground=COLORS["text"],
            selectbackground=COLORS["accent"],
            borderwidth=0, highlightthickness=0,
            padx=10, pady=8,
        )
        self.input_text.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        self.input_text.bind("<Control-Return>", self._on_submit)
        self.input_text.bind("<Escape>", lambda _: self._on_close())
        row += 1

        # ── hint ──
        tk.Label(
            main, text="Ctrl+Enter 提交  |  空白提交 = 退出会话  |  Esc 关闭",
            bg=COLORS["bg"], fg=COLORS["subtext"], font=(FONT, 9),
        ).grid(row=row, column=0, sticky="w", pady=(0, 10))
        row += 1

        # ── buttons ──
        btn_frame = tk.Frame(main, bg=COLORS["bg"])
        btn_frame.grid(row=row, column=0, sticky="e")

        submit_btn = tk.Button(
            btn_frame, text="  提交反馈",
            command=lambda: self._on_submit(None),
            bg=COLORS["accent"], fg="#1e1e2e",
            activebackground="#b4d0fb", activeforeground="#1e1e2e",
            font=(FONT, 10, "bold"), relief=tk.FLAT,
            padx=20, pady=6, cursor="hand2",
        )
        submit_btn.pack(side=tk.RIGHT, padx=(8, 0))

        exit_btn = tk.Button(
            btn_frame, text="退出",
            command=self._on_close,
            bg=COLORS["border"], fg=COLORS["text"],
            activebackground=COLORS["red"], activeforeground="#1e1e2e",
            font=(FONT, 10), relief=tk.FLAT,
            padx=20, pady=6, cursor="hand2",
        )
        exit_btn.pack(side=tk.RIGHT)

    # ── event handlers ───────────────────────────────────────────

    def _on_submit(self, event):
        self.feedback = self.input_text.get("1.0", tk.END).strip()
        self._cancel_timer()
        self.root.destroy()
        return "break"

    def _on_close(self):
        self.feedback = ""
        self._cancel_timer()
        self.root.destroy()

    # ── timeout timer ────────────────────────────────────────────

    def _cancel_timer(self):
        if self._timeout_id:
            self.root.after_cancel(self._timeout_id)
            self._timeout_id = None

    def _start_timer(self):
        self._tick()

    def _tick(self):
        if self._remaining <= 0:
            self._on_close()
            return
        m, s = divmod(self._remaining, 60)
        self.timer_label.configure(text=f"{m:02d}:{s:02d}")
        self._remaining -= 1
        self._timeout_id = self.root.after(1000, self._tick)


def show_feedback_dialog(
    summary: str, project_directory: str, timeout: int = 600,
) -> str:
    dialog = FeedbackDialog(summary, project_directory, timeout)
    return dialog.show()
