if __name__ == '__main__':

    gender = get_rand_gender()  # Przypisanie płci do procesu
    lockers = AccessController('lockers', gender, LockersMonitor())  # Kolejka odpowiedzialna za szatnie
    showers = AccessController('showers', gender, ShowerMonitor())  # Kolejka odpowiedzialna za natrysk

    # Po uzyskaniu dostępu do szatni, proces dokona próby wejścia pod natrysk
    lockers.set_access_func(LOCKER_DELAY, showers.enter)

    # Po wejściu pod natrysk i odczekaniu, proces wyjdzie z pod natrysku
    showers.set_access_func(SHOWER_DELAY, showers.exit)

    # Po wyjściu z pod natrysku proces wykonuje timeout, który odzwierciedla czas spędzony na basenie
    # Po wyjściu z basenu następuje wywołanie wyjścia z szatni
    showers.set_exit_func(POOL_DELAY, lockers.exit)

    # Po wyjściu z szatni proces informuje o wykonaniu zadania
    lockers.set_exit_func(0, job_done)
