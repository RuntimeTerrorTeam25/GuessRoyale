import wx
import random
import time

from config import DIFFICULTY_LEVELS, WORD_LISTS
from game.core import GameState
from game.leaderboard import add_score
from game.leaderboard import load_leaderboard


class GuessRoyaleFrame(wx.Frame):
    
    def __init__(self):
        super().__init__(
            None,
            title="GuessRoyale – GUI",
            size=(750, 380),
            style=wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX
        )
        self.Centre()

        self.state: GameState | None = None
        self.target = None
        self.secret = None
        self.attempts_left = 0

        self.word_len = 0
        self.max_attempts = 0
        self.current_row = 0
        self.grid_labels: list[list[wx.StaticText]] = []

        panel = wx.Panel(self)
        self.panel = panel
        root = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(panel, label="GuessRoyale")
        f = title.GetFont(); f.PointSize += 8; f = f.Bold(); title.SetFont(f)
        root.Add(title, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)

        cfg = wx.BoxSizer(wx.HORIZONTAL)
        cfg.Add(wx.StaticText(panel, label="Name:"), 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        self.name_txt = wx.TextCtrl(panel); cfg.Add(self.name_txt, 1, wx.RIGHT, 10)

        self.rb_num = wx.RadioButton(panel, label="Number", style=wx.RB_GROUP)
        self.rb_word = wx.RadioButton(panel, label="Word")
        cfg.Add(self.rb_num, 0, wx.RIGHT, 5); cfg.Add(self.rb_word, 0, wx.RIGHT, 15)

        cfg.Add(wx.StaticText(panel, label="Difficulty:"), 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        diff_labels = [f"{k} - {v['name']}" for k, v in DIFFICULTY_LEVELS.items()]
        self.diff_choice = wx.ComboBox(panel, choices=diff_labels, style=wx.CB_READONLY)
        self.diff_choice.SetSelection(0)
        cfg.Add(self.diff_choice, 0, wx.RIGHT, 10)

        self.start_btn = wx.Button(panel, label="Start")
        self.exit_btn = wx.Button(panel, label="Exit")
        cfg.Add(self.start_btn, 0, wx.RIGHT, 5); cfg.Add(self.exit_btn, 0)
        root.Add(cfg, 0, wx.EXPAND | wx.ALL, 8)

        root.Add(wx.StaticLine(panel), 0, wx.EXPAND | wx.ALL, 5)

        self.status_lbl = wx.StaticText(panel, label="Status: Not playing")
        root.Add(self.status_lbl, 0, wx.ALL | wx.EXPAND, 4)


        # Leaderboard (Home Screen)
        self.lb_title = wx.StaticText(panel, label="Leaderboard")
        lb_font = self.lb_title.GetFont()
        lb_font.SetWeight(wx.FONTWEIGHT_BOLD)
        self.lb_title.SetFont(lb_font)

        self.leaderboard = wx.ListCtrl(
            panel,
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )

        self.leaderboard.InsertColumn(0, "Name")
        self.leaderboard.InsertColumn(1, "Mode")
        self.leaderboard.InsertColumn(2, "Difficulty")
        self.leaderboard.InsertColumn(3, "Score")

        root.Add(self.lb_title, 0, wx.LEFT | wx.TOP, 8)
        root.Add(self.leaderboard, 1, wx.EXPAND | wx.ALL, 8)


        self.mode_sizer = wx.BoxSizer(wx.VERTICAL)

        


        # Number mode UI
        self.num_panel = wx.Panel(panel)
        num_s = wx.BoxSizer(wx.VERTICAL)
        self.num_info = wx.StaticText(self.num_panel, label="Number mode instructions.")
        self.num_feedback = wx.StaticText(self.num_panel, label="")
        num_in_row = wx.BoxSizer(wx.HORIZONTAL)
        self.num_input = wx.TextCtrl(self.num_panel, style=wx.TE_PROCESS_ENTER)
        self.num_submit = wx.Button(self.num_panel, label="Submit")
        num_in_row.Add(self.num_input, 1, wx.RIGHT, 8); num_in_row.Add(self.num_submit, 0)
        num_s.Add(self.num_info, 0, wx.ALL | wx.EXPAND, 6)
        num_s.Add(self.num_feedback, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 6)
        num_s.Add(num_in_row, 0, wx.ALL | wx.EXPAND, 6)
        self.num_panel.SetSizer(num_s)

        # Word mode UI
        self.word_panel = wx.Panel(panel)
        word_s = wx.BoxSizer(wx.VERTICAL)
        self.word_info = wx.StaticText(self.word_panel, label="Word mode instructions.")
        word_s.Add(self.word_info, 0, wx.ALL | wx.EXPAND, 6)
        self.grid_container = wx.Panel(self.word_panel)
        self.grid_container.SetBackgroundColour(wx.Colour(240, 240, 240))
        self.grid_sizer = wx.GridSizer(rows=1, cols=1, vgap=4, hgap=4)
        self.grid_container.SetSizer(self.grid_sizer)
        word_s.Add(self.grid_container, 1, wx.ALL | wx.EXPAND, 6)
        word_in_row = wx.BoxSizer(wx.HORIZONTAL)
        self.word_input = wx.TextCtrl(self.word_panel, style=wx.TE_PROCESS_ENTER)
        self.word_submit = wx.Button(self.word_panel, label="Guess")
        word_in_row.Add(self.word_input, 1, wx.RIGHT, 8); word_in_row.Add(self.word_submit, 0)
        word_s.Add(word_in_row, 0, wx.ALL | wx.EXPAND, 6)
        self.word_feedback = wx.StaticText(self.word_panel, label="")
        word_s.Add(self.word_feedback, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 6)
        self.word_panel.SetSizer(word_s)

        self.mode_sizer.Add(self.num_panel, 0, wx.EXPAND)
        self.mode_sizer.Add(self.word_panel, 1, wx.EXPAND)
        root.Add(self.mode_sizer, 1, wx.EXPAND | wx.ALL, 4)

        panel.SetSizer(root)


        self.Bind(wx.EVT_SIZE, self.on_resize)
        self.start_btn.Bind(wx.EVT_BUTTON, self.on_start)
        self.exit_btn.Bind(wx.EVT_BUTTON, lambda e: self.Close())
        self.num_submit.Bind(wx.EVT_BUTTON, self.on_num_submit)
        self.num_input.Bind(wx.EVT_TEXT_ENTER, self.on_num_submit)
        self.word_submit.Bind(wx.EVT_BUTTON, self.on_word_submit)
        self.word_input.Bind(wx.EVT_TEXT_ENTER, self.on_word_submit)

        self.show_number_mode(False); self.show_word_mode(False)
        self.disable_inputs()
        self.load_leaderboard_table()

    def load_leaderboard_table(self):
            self.leaderboard.DeleteAllItems()
            data = load_leaderboard()
            data = sorted(data, key=lambda x: x["score"], reverse=True)

            for row in data:
                idx = self.leaderboard.InsertItem(
                    self.leaderboard.GetItemCount(), row["player"]
                )
                self.leaderboard.SetItem(idx, 1, row["mode"])
                self.leaderboard.SetItem(idx, 2, row["difficulty"])
                self.leaderboard.SetItem(idx, 3, str(row["score"]))

            for col in range(4):
                self.leaderboard.SetColumnWidth(
                    col, wx.LIST_AUTOSIZE_USEHEADER
                )

            total_width = self.leaderboard.GetClientSize().width
            col_width = total_width // 4

            for col in range(4):
                self.leaderboard.SetColumnWidth(col, col_width) 

    def on_resize(self, event):
        if self.leaderboard.IsShown():
            total_width = self.leaderboard.GetClientSize().width
            col_width = total_width // 4
            for col in range(4):
                self.leaderboard.SetColumnWidth(col, col_width)
        event.Skip()

    # sizing / helpers

    def resize_for_number_mode(self):
        self.SetSize((750, 380)); self.Centre(); self.panel.Layout()

    def resize_for_word_mode(self):
        self.SetSize((900, 600)); self.Centre(); self.panel.Layout()

    def show_number_mode(self, show: bool):
        self.num_panel.Show(show)

    def show_word_mode(self, show: bool):
        self.word_panel.Show(show)

    def update_status(self):
        if not self.state:
            self.status_lbl.SetLabel("Status: Not playing")
        else:
            s = self.state
            self.status_lbl.SetLabel(
                f"Player: {s.player_name}   Mode: {s.mode}   "
                f"Diff: {s.difficulty_name}   Lives: {s.lives}   Score: {s.score}"
            )
        self.panel.Layout()

    def disable_inputs(self):
        for w in (self.num_input, self.num_submit, self.word_input, self.word_submit):
            w.Enable(False)

    def enable_inputs_for_mode(self):
        if not self.state: 
            return
        is_num = self.state.mode == "Number"
        self.num_input.Enable(is_num); self.num_submit.Enable(is_num)
        self.word_input.Enable(not is_num); self.word_submit.Enable(not is_num)

    # start
    
    def on_start(self, event):

        self.lb_title.Hide()
        self.leaderboard.Hide()

        name = self.name_txt.GetValue().strip() or "Anonymous"
        diff_key = self.diff_choice.GetStringSelection().split(" - ")[0]
        mode = "Number" if self.rb_num.GetValue() else "Word"

        self.state = GameState(name, mode, diff_key)
        self.target = self.secret = None
        self.attempts_left = 0
        self.num_feedback.SetLabel(""); self.word_feedback.SetLabel("")
        self.disable_inputs()

        if mode == "Number":
            self.resize_for_number_mode()
            self.show_number_mode(True); self.show_word_mode(False)
            self.start_number_round()
        else:
            self.resize_for_word_mode()
            self.show_number_mode(False); self.show_word_mode(True)
            self.start_word_game()

        self.enable_inputs_for_mode()
        self.update_status()

    # number mode

    def start_number_round(self):
        d = self.state.difficulty
        self.attempts_left = d["max_attempts"]
        self.target = random.randint(d["min"], d["max"])
        self.num_info.SetLabel(
            f"Guess a number between {d['min']} and {d['max']} "
            f"(Attempts: {self.attempts_left})."
        )
        self.num_feedback.SetLabel("")
        self.num_input.SetValue(""); self.num_input.SetFocus()

    def on_num_submit(self, event):
        if not self.state or self.state.mode != "Number":
            return
        guess_str = self.num_input.GetValue().strip()
        if not guess_str:
            self.num_feedback.SetLabel("Enter a number."); return
        self.num_input.SetValue("")
        try:
            g = int(guess_str)
        except ValueError:
            self.num_feedback.SetLabel("Enter a valid integer."); return

        self.attempts_left -= 1

        if g == self.target:
            pts = max(self.attempts_left + 1, 1) * 10
            self.state.score += pts
            self.update_status()
            res = self.ask_continue(f"Correct!\nYou earned {pts} points.\n"
                                    f"Total score: {self.state.score}")
            if res == wx.ID_YES:
                self.start_number_round()
            else:
                self.game_over()
            return

        self.num_feedback.SetLabel("Too low." if g < self.target else "Too high.")
        if self.attempts_left <= 0:
            self.handle_round_failed()
        else:
            self.num_info.SetLabel(f"Attempts left: {self.attempts_left}. Try again.")
        self.update_status()

    # word mode

    def start_word_game(self):
        words = WORD_LISTS[self.state.difficulty_key]
        self.secret = random.choice(words).lower()
        d = self.state.difficulty
        self.max_attempts = d["max_attempts"]
        self.attempts_left = self.max_attempts
        self.word_len = len(self.secret)
        self.current_row = 0
        self.word_info.SetLabel(
            "Guess the secret word.\n"
            f"Hint: len={self.word_len}, first='{self.secret[0]}', "
            f"last='{self.secret[-1]}' (Attempts: {self.max_attempts})."
        )
        self.word_feedback.SetLabel("")
        self.word_input.SetValue(""); self.word_input.SetFocus()
        self.build_word_grid()

    def build_word_grid(self):
        for row in self.grid_labels:
            for cell in row:
                cell.Destroy()
        self.grid_labels = []
        self.grid_sizer.Clear()
        self.grid_sizer = wx.GridSizer(rows=self.max_attempts, cols=self.word_len, vgap=4, hgap=4)
        self.grid_container.SetSizer(self.grid_sizer)

        for _ in range(self.max_attempts):
            row_labels = []
            for _ in range(self.word_len):
                btn = wx.Button(
                    self.grid_container,
                    label="",
                    style=wx.BU_EXACTFIT | wx.BORDER_NONE,

                )

                btn.SetBackgroundColour(wx.Colour(200, 200, 200))
                btn.SetForegroundColour(wx.BLACK)
                btn.SetOwnBackgroundColour(wx.Colour(200, 200, 200))
                btn.SetOwnForegroundColour(wx.BLACK)

                btn.SetMinSize((45, 45))
                btn.Bind(wx.EVT_BUTTON, lambda e: None)  # ignore clicks
                

                font = btn.GetFont()
                font.SetPointSize(font.GetPointSize() + 4)
                font.SetWeight(wx.FONTWEIGHT_BOLD)
                btn.SetFont(font)
                self.grid_sizer.Add(btn, 0, wx.EXPAND)
                row_labels.append(btn)

            self.grid_labels.append(row_labels)

        self.grid_container.Layout(); self.panel.Layout()

    def on_word_submit(self, event):
        if not self.state or self.state.mode != "Word" or self.current_row >= self.max_attempts:
            return
        guess = self.word_input.GetValue().strip().lower()
        if not guess:
            self.word_feedback.SetLabel("Enter a word."); return
        if len(guess) != self.word_len:
            self.word_feedback.SetLabel(f"Enter a {self.word_len}-letter word."); return
        self.word_input.SetValue("")
        self.evaluate_word_guess(guess)

    def evaluate_word_guess(self, guess: str):
        self.attempts_left -= 1
        secret = self.secret
        row_labels = self.grid_labels[self.current_row]

        remaining = {}
        for i, ch in enumerate(secret):
            if guess[i] != ch:
                remaining[ch] = remaining.get(ch, 0) + 1

        red = wx.Colour(180, 30, 30)
        green = wx.Colour(0, 135, 90)
        yellow = wx.Colour(200, 160, 0)

        colours = [red] * self.word_len

        for i, ch in enumerate(guess):
            row_labels[i].SetLabel(ch.upper())
            if ch == secret[i]:
                colours[i] = green

        for i, ch in enumerate(guess):
            if colours[i] == green:
                continue
            if remaining.get(ch, 0) > 0:
                colours[i] = yellow
                remaining[ch] -= 1

        for i in range(self.word_len):
            row_labels[i].SetBackgroundColour(colours[i])
            row_labels[i].SetForegroundColour(wx.WHITE)  # ALWAYS white text
            row_labels[i].Refresh()


        self.grid_container.Layout(); self.panel.Layout()

        if guess == secret:
            pts = max(self.attempts_left + 1, 1) * 15
            self.state.score += pts
            self.update_status()
            res = self.ask_continue(
                f"Correct! The word was '{secret}'.\n"
                f"You earned {pts} points.\nTotal score: {self.state.score}"
            )
            if res == wx.ID_YES:
                self.start_word_game()
            else:
                self.game_over()
            return

        if self.attempts_left <= 0:
            self.handle_round_failed()
        else:
            self.current_row += 1
            self.word_feedback.SetLabel(
                f"Wrong guess. Attempts left: {self.attempts_left}."
            )
        self.update_status()

    # shared

    def ask_continue(self, msg: str) -> int:
        dlg = wx.MessageDialog(
            self, msg + "\n\nContinue?", "Round Complete",
            wx.YES_NO | wx.ICON_INFORMATION
        )
        res = dlg.ShowModal()
        dlg.Destroy()
        return res

    def handle_round_failed(self):
        self.state.lives -= 1
        self.update_status()
        if self.state.lives > 0:
            wx.MessageBox(
                f"Out of attempts.\nLives left: {self.state.lives}",
                "Round Failed", wx.OK | wx.ICON_INFORMATION
            )
            if self.state.mode == "Number":
                self.start_number_round()
            else:
                self.start_word_game()
        else:
            revived = self.revival_minigame()
            if revived:
                self.state.lives = 1
                self.update_status()
                wx.MessageBox(
                    "Revived with 1 life!", "Revival",
                    wx.OK | wx.ICON_INFORMATION
                )
                if self.state.mode == "Number":
                    self.start_number_round()
                else:
                    self.start_word_game()
            else:
                self.game_over()

    # revival hub

    def revival_minigame(self) -> bool:
        challenges = [
            self.rv_memory_flash,
            self.rv_direction_reflex,
            self.rv_fast_typing,
            self.rv_quick_math,
        ]
        chosen = random.choice(challenges)
        name = chosen.__name__.replace("rv_", "").replace("_", " ").title()
        dlg = wx.MessageDialog(
            self,
            f"You are out of lives.\n\nRevival Arena has chosen:\n\n{name}\n\n"
            "Win this challenge to revive with 1 life.",
            "Revival Arena", wx.OK | wx.ICON_INFORMATION
        )
        dlg.ShowModal(); dlg.Destroy()
        return chosen()

    def rv_memory_flash(self) -> bool:
        seq = "".join(str(random.randint(0, 9)) for _ in range(5))
        dlg = wx.MessageDialog(
            self,
            f"MEMORY FLASH\n\nMemorize this 5-digit sequence:\n\n{seq}\n\n"
            "Press OK when you are ready to type it.",
            "Memory Flash", wx.OK | wx.ICON_INFORMATION
        )
        dlg.ShowModal(); dlg.Destroy()
        ask = wx.TextEntryDialog(self, "Enter the sequence exactly as shown:", "Memory Flash – Recall")
        ans = ask.GetValue().strip().replace(" ", "") if ask.ShowModal() == wx.ID_OK else ""
        ask.Destroy()
        if ans == seq:
            wx.MessageBox("Perfect recall. You revive!", "Revival Success", wx.OK | wx.ICON_INFORMATION)
            return True
        wx.MessageBox(f"Wrong. Correct sequence was: {seq}", "Revival Failed", wx.OK | wx.ICON_ERROR)
        return False

    def rv_direction_reflex(self) -> bool:
        directions = {"L": "LEFT", "R": "RIGHT", "U": "UP", "D": "DOWN"}
        rounds, time_limit = 5, 1.5
        for i in range(rounds):
            key, label = random.choice(list(directions.items()))
            msg = (
                f"DIRECTION REFLEX (Round {i+1}/{rounds})\n\n"
                f"Type the FIRST LETTER of:\n\n{label}\n\n"
                f"You must respond within {time_limit} seconds."
            )
            start = time.time()
            dlg = wx.TextEntryDialog(self, msg, "Direction Reflex")
            ans = dlg.GetValue().strip().upper() if dlg.ShowModal() == wx.ID_OK else ""
            dlg.Destroy()
            delta = time.time() - start
            if delta > time_limit:
                wx.MessageBox(f"Too slow! ({delta:.2f}s)", "Reflex Failed", wx.OK | wx.ICON_ERROR)
                return False
            if ans != key:
                wx.MessageBox(f"Wrong direction. Expected '{key}'.", "Reflex Failed", wx.OK | wx.ICON_ERROR)
                return False
        wx.MessageBox("Reflexes on point. You revive!", "Revival Success", wx.OK | wx.ICON_INFORMATION)
        return True

    def rv_fast_typing(self) -> bool:
        words = ["royale", "python", "reflex", "memory", "ninja", "system"]
        word = random.choice(words); time_limit = 4
        msg = (
            "FAST TYPING\n\n"
            f"Type this word exactly within {time_limit} seconds:\n\n{word}"
        )
        start = time.time()
        dlg = wx.TextEntryDialog(self, msg, "Fast Typing")
        ans = dlg.GetValue().strip() if dlg.ShowModal() == wx.ID_OK else ""
        dlg.Destroy()
        delta = time.time() - start
        if delta > time_limit:
            wx.MessageBox(f"Too slow! ({delta:.2f}s)", "Typing Failed", wx.OK | wx.ICON_ERROR)
            return False
        if ans == word:
            wx.MessageBox("Typing accurate and fast. You revive!", "Revival Success", wx.OK | wx.ICON_INFORMATION)
            return True
        wx.MessageBox(f"Incorrect typing.\nExpected: {word}", "Typing Failed", wx.OK | wx.ICON_ERROR)
        return False

    def rv_quick_math(self) -> bool:
        a = random.randint(5, 15)
        b = random.randint(2, 12)
        op = random.choice(["+", "-", "*"])
        ans = a + b if op == "+" else a - b if op == "-" else a * b
        limit = 7
        msg = (
            "QUICK MATH\n\nSolve this within the time limit to revive:\n\n"
            f"{a} {op} {b} = ?\n\nTime limit: {limit} seconds."
        )
        start = time.time()
        dlg = wx.TextEntryDialog(self, msg, "Quick Math")
        val = dlg.GetValue().strip() if dlg.ShowModal() == wx.ID_OK else ""
        dlg.Destroy()
        delta = time.time() - start
        if delta > limit:
            wx.MessageBox(f"Too slow ({delta:.2f}s).", "Math Failed", wx.OK | wx.ICON_ERROR)
            return False
        try:
            if int(val) == ans:
                wx.MessageBox("Correct! You revive with 1 life.", "Revival Success", wx.OK | wx.ICON_INFORMATION)
                return True
        except ValueError:
            pass
        wx.MessageBox(f"Wrong answer. Correct = {ans}", "Math Failed", wx.OK | wx.ICON_ERROR)
        return False

    def game_over(self):
        score = self.state.score if self.state else 0

        dlg = wx.MessageDialog(
            self,
            f"Game Over.\nFinal score: {score}\n\nSave to leaderboard?",
            "Game Over",
            wx.YES_NO | wx.ICON_QUESTION,
        )
        res = dlg.ShowModal()
        dlg.Destroy()

        if res == wx.ID_YES and self.state is not None:
            add_score(self.state)

        # SHOW leaderboard again on home screen
        self.lb_title.Show()
        self.leaderboard.Show()
        self.load_leaderboard_table()

        # reset game state
        self.state = None
        self.target = None
        self.secret = None
        self.attempts_left = 0
        self.word_len = 0
        self.max_attempts = 0
        self.current_row = 0

        self.disable_inputs()
        self.show_number_mode(False)
        self.show_word_mode(False)
        self.status_lbl.SetLabel("Status: Not playing")
        self.panel.Layout()



class GuessRoyaleApp(wx.App):
    def OnInit(self):
        frame = GuessRoyaleFrame()
        frame.Show()
        self.SetTopWindow(frame)
        return True


if __name__ == "__main__":
    app = GuessRoyaleApp(False)
    app.MainLoop()
