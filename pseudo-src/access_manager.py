class AccessManager():  #klasa odpowiedzialna za rozgłaszanie informacji o zasobach i zbieranie potwierdzeń
    my_state = 'idle'
    my_type = None
    req_id = None
    req_state = 'outside'


    def mk_msg(cmd):  #generowanie treści komunikatu
        rank = my_id
        data = {'cmd': cmd, 'rank': rank}
        if cmd == 'update':
            data['id'] = req_id
            data['type'] = my_type
            data['state'] = req_state
        return data
    
    def send_update():  #wysłanie informacji o aktualnie wykonanej operacji
        data = mk_msg('update')
        bcast(data)
        my_state = 'active'

    def get_in():  #próba uzyskania zasobu
        entry = monitor.try_get_access(my_type)
        req_state = 'entering'
        if entry:
            req_id = monitor.id
            send_update()
            monitor.get_in(req_id, my_type)
            req_state = 'inside'
            free_critical()
            my_state = 'idle'
        else:
            my_state = 'requesting'

    def get_out():  #zwolnienie zasobu
        req_state = 'exiting'
        send_update()
        monitor.get_out(req_id)
        req_state = 'outside'
        my_state = 'idle'

    def on_update(sender, data):  #zdarzenie otrzymania informacji o zmianie w zasobie
        op = data['state']
        if op == 'entering':
            monitor.get_in(data['id'], data['type'])
        elif op == 'exiting':
            monitor.get_out(data['id'])
            if my_state == 'requesting':
                get_in()
