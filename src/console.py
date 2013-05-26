import time
#def display_queue():
 #   print("                       .----.")
 #   print(" ~O   O  ~O   O  ~O    |   ||")
 #   print(" /|\ /|\ /|\ /|\ /|\   |   ||")
 #   print(" / \ / \ / \ / \ / \  ||  |||")
 #   print(" ----------------------------")

#                       _o_        _o_
#                       /_\         |
#                        X         / \
#+=================+----------+----------+
#|        Waiting: |          |          |
#|-----------------|----------|----------|
#| Locker room #1: |          |          |
#|-----------------|----------|----------|
#| Locker room #2: |          |          |
#|-----------------|----------|----------|
#| Locker room #3: |          |          |
#|-----------------|----------|----------|
#|        Showers: |          |          |
#|-----------------|----------|----------|
#|  Swimming pool: |          |          |
#+=================+==========+==========+

#display_queue()

class Console:
    def format_field_pro(self, val):
        return "    " + '{:6s}'.format(str(val)) + ""

    # def format_field_easy(self, val):
    #     return " " + '{:3s}'.format(str(val)) + " "

    break_line = "|-----------------|----------|----------|"

    def display_global_state_pro(self):
        print("                       _o_        _o_    ")
        print("                       /_\         |     ")
        print("                        X         / \    ")
        print("+=================+----------+----------+")
        print("|        Waiting: |" + self.format_field_pro(15) + "|" + self.format_field_pro(15) + "|")
        print(self.break_line)
        print("| Locker room #1: |" + self.format_field_pro(15) + "|" + self.format_field_pro(15) + "|")
        print(self.break_line)
        print("| Locker room #2: |" + self.format_field_pro(15) + "|" + self.format_field_pro(15) + "|")
        print(self.break_line)
        print("| Locker room #3: |" + self.format_field_pro(15) + "|" + self.format_field_pro(15) + "|")
        print(self.break_line)
        print("|        Showers: |" + self.format_field_pro(15) + "|" + self.format_field_pro(15) + "|")
        print(self.break_line)
        print("|  Swimming pool: |" + self.format_field_pro(15) + "|" + self.format_field_pro(15) + "|")
        print("+=================+==========+==========+")

    # def display_global_state_easy(self):


#
# times = 8  # 24
# # print('\n' * times)
# display_global_state()
# time.sleep(5)
# print('\n' * times)
# display_global_state()