class AccessAlgo:  # Algorytm uszeregowania dostępu do sekcji krytycznej
    my_state = 'idle'
    confirmations_num = 0
    confirmations_tab[K] = [False]
    waiting_set = []

    def send_request():
        #wysłanie żądania dostępu do sekcji krytycznej
        my_state = 'waiting'
        confirmations_num = 0
        confirmations_tab = [False]
        bcast('request')

    def send_confirmation(target):
        #wysłanie zezwolenia na wejście do sekcji krytycznej
        send(target, ['allowed', my_id])

    def exit_critical():
        #procedura opuszczenia sekcji krytycznej
        my_state = 'idle'
        for e in waiting_set:
            send_confirmation(e)
        waiting_set.clear()

    def on_confirmation(sender):
        #zdarzenie otrzymania potwierdzenia
        confirmations_num += 1
        confirmations_tab[sender] = True
        if confirmations_num == K - 1:
            my_state = 'active'
            critical_section()

    def on_request(sender, data):

        #zdarzenie otrzymania żądania dostępu)
        if my_state == 'idle' or (my_state == 'waiting' and sender < my_id):
            send_confirmation(sender)
        else:
            waiting_set.append(sender)