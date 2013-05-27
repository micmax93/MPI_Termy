class AccessManager():  #klasa odpowiedzialna za rozgłaszanie informacji o zasobach i zbieranie potwierdzeń
    gender = None
    req_id = None
    req_state = 'outside'
    state = 'idle'
    monitor = Monitor()  #monitor definiujący reguły dostępu do zasobów
    queue_free_func = empty_func  #procedura wywoływana po uzyskaniu dostępu do sekcji krytycznej
    access_func = empty_func  #procedura wywoływana po uzyskaniu zasobu
    get_in_delay = 0  #opóźnienie wywołania funkcji access_func
    exit_func = empty_func #procedura wywoływana po zwolnieniu zasobu
    get_out_delay = 0  #opóźnienie wywołania funkcji exit_func

    def __init__(self, name, gender, monitor):
        self.name = name
        self.confirmations_num = 0
        self.confirmations_tab = [False] * mpi_count()
        self.gender = gender
        self.monitor = monitor

    def get_in(self):
        #próba uzyskania zasobu
        (entry, id) = self.monitor.get_access(self.gender)
        self.req_state = 'entering'
        if entry:
            self.req_id = id
            self.send_request()
        else:
            self.state = 'requesting'

    def get_out(self):
        #zwolnienie zasobu
        self.req_state = 'exiting'
        self.send_request()

    def send_request(self):
        #wysłanie żadania/informacji o aktualnie wykonanej operacji
        self.state = 'waiting'
        self.confirmations_num = 0
        self.confirmations_tab = [False] * mpi_count()
        mpi_bcast('request')

    def send_confirmation(self, target):
        #wysłanie potwierdzenia
        mpi_send(target, 'allowed')

    def critical_section(self):
        #kod wykonywany w momencie uzyskania kompletu potwierdzeń
        if self.req_state == 'entering':
            self.monitor.get_in(self.req_id, self.gender)
            self.req_state = 'inside'
            self.queue_free_func()
            exec_later(self.get_in_delay, self.access_func)

        elif self.req_state == 'exiting':
            self.monitor.get_out(self.req_id)
            self.req_state = 'outside'
            exec_later(self.get_out_delay, self.exit_func)


    def on_confirmation(self, sender):
        #zdarzenie otrzymania potwierdzenia
        self.confirmations_num += 1
        self.confirmations_tab[sender] = True
        if self.confirmations_num == mpi_count() - 1:
            self.state = 'active'
            self.critical_section()
            self.state = 'idle'

    def on_request(self, sender, data):
        #zdarzenie otrzymania informacji o zmianie w zasobie
        self.send_confirmation(sender)
        op = data['state']
        if op == 'entering':
            self.monitor.get_in(data['id'], data['gender'])
        elif op == 'exiting':
            self.monitor.get_out(data['id'])
            if self.state == 'requesting':
                self.get_in()
