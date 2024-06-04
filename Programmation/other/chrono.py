class ChronoApp:
    """
    class utiliser pour les partie seul et avec le portail (Solo, Portail), elle sert a faire l'element chronomettre quand ou joue a deux
    """
    
    def __init__(self, main, master, label, time):
        self.main = main
        self.master = master
        self.label = label
        self.time_left = time
        self.timer_id = None
        self.update_timer()

    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        return f"{mins:02}:{secs:02}"

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.label.config(text=self.format_time(self.time_left))
            self.timer_id = self.main.after(1000, self.update_timer)
        else:
            self.stop_timer()
            if self.master.callback:
                self.master.callback()
    
    def stop_timer(self):
        if self.timer_id:
            self.main.after_cancel(self.timer_id)