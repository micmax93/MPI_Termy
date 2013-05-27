class AccessQueue:  # Kolejka oparta o algorytm Lamporta
    state = 'idle'
    confirmations_num = 0
    confirmations_tab = [False] * mpi_count()
    waiting_set = []


    def send_request(self):
        #wysłanie żądania dostępu do sekcji krytycznej
        self.state = 'waiting'
        self.confirmations_num = 0
        self.confirmations_tab = [False] * mpi_count()
        mpi_bcast('request')

    def send_confirmation(self, target):
        #wysłanie zezwolenia na wejście do sekcji krytycznej
        mpi_send(target, 'allowed')

    def exit_critical(self):
        #procedura opuszczenia sekcji krytycznej
        self.state = 'idle'
        for e in self.waiting_set:
            self.send_confirmation(e)
        self.waiting_set.clear()

    def on_confirmation(self, sender):
        #zdarzenie otrzymania potwierdzenia
        self.confirmations_num += 1
        self.confirmations_tab[sender] = True
        if self.confirmations_num == mpi_count() - 1:
            self.state = 'active'
            self.critical_section()

    def on_request(self, sender, data):

        #zdarzenie otrzymania żądania dostępu)
        if self.state == 'idle':
            self.send_confirmation(sender)

        elif self.state == 'waiting' and sender < mpi_rank() and not self.confirmations_tab[sender]:
            self.send_confirmation(sender)

        else:
            self.waiting_set.append(sender)