class AccessController:
    """
    Klasa odpowiedzialna za spójną kontrolę dostępu i operacji na zasobie
    Itegruje ze sobą kolejkę dostępu z managerem zasobu
    kolejka - odpowiada za to żeby dostęp do krytycznej częsci zasobu był sekwencyjny i sprawiedliwy
    manager - odpowiada za to aby zasób był użytkowany zgodnie z określonymi regułami
    """
    def __init__(self, name, gender, monitor):
        #utworzenie kolejki i managera
        self.queue = AccessQueue(name)
        self.manager = AccessManager(name, gender, monitor)

        #powiązanie sekcji krytycznej kolejki z żądaniem uzyskania zasobu
        self.queue.get_access_func = self.manager.get_in

        #zwolnienie sekcji krytycznej po uzyskaniu zasobu
        self.manager.queue_free_func = self.queue.exit_critical


    def set_access_func(self, delay, func):
        #ustawia funkcję wywoływaną po uzyskaniu zasobu

    def set_exit_func(self, delay, func):
        #ustawia funkcję wywoływaną po zwolnieniu zasobu

    def enter(self):
        #zgłoszenie zamiaru uzyskania zasobu
        self.queue.send_update()

    def exit(self):
        #zwolnienie zasobu
        self.manager.get_out()

    def on_confirmation(self, sender, data):
        #zdarzenie otrzymania potwierdzenia

    def on_request(self, sender, data):
        #zdarzenie otrzymania żądania