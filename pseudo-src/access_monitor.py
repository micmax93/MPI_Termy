class Monitor:  # Interfejs ogólnego monitora zasobów.

    def get_in(self, num, gender):
        # Uzyskanie zasobu o numerze "num" przez proces płci "gender".
        pass

    def get_out(self, num):
        # Zwolnienie jednostki zasobu o numerze "num"
        pass

    def get_access(self, gender):
        # Sprawdzenie czy dla danej płci znajduje się dostępny zasób.
        pass