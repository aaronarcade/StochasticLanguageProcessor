#Aaron Brown
import sys, io
from time import sleep

class SourceModel:

     def __init__(self, name, text_stream):
        self.name = name
        self.text_stream = text_stream
        print("Training " + self.name[:-7] + " model ", end="")
        text_stream.seek(0)
        self.stochastic = [[0] * 26 for i in range(0,26)]
        letter_1 = text_stream.read(1)
        letter_2 = text_stream.read(1)
        norm_vec = []

        while letter_2 != "":
            self.stochastic[ord(letter_1)-97][ord(letter_2)-97] += 1
            letter_1 = letter_2
            letter_2 = text_stream.read(1)

        for state_1 in range(len(self.stochastic)):
            norm_vec.append(sum(self.stochastic[state_1]))
            for state_2 in range(len(self.stochastic[state_1])):
                if self.stochastic[state_1][state_2] != 0:
                    self.stochastic[state_1][state_2] = float(self.stochastic[state_1][state_2]/norm_vec[state_1])
                else:
                    self.stochastic[state_1][state_2] = 0.01
        for c in "...":
            print(c, end="")
            sys.stdout.flush()
            sleep(0.2)
        print(" done.")

     def probability(self, text_stream):
         text_stream.seek(0)
         prob = 1
         letter_1 = text_stream.read(1)
         letter_2 = text_stream.read(1)

         while letter_2 != "":
            prob*=self.stochastic[ord(letter_1)-97][ord(letter_2)-97]
            letter_1 = letter_2
            letter_2 = text_stream.read(1)
         text_stream.close()
         return prob


     def __repr__(self):
        state_string = "\t"
        for letter in range(0,26):
             state_string+= chr(letter+97) + "\t"
        state_string += "\n"
        for state_1 in range(26):
            state_string += chr(state_1+97) + "\t"
            for state_2 in self.stochastic[state_1]:
                state_string += format(state_2, '.2f') + "\t"
            state_string += "\n"
        return state_string

if __name__=="__main__":

    fin = sys.argv[-1]
    langs = sys.argv[1:-1]

    def make_string(t):
        if t[-5:] == ".test" or t[-7:] == ".corpus":
            test_file = open(t, "rt").read().lower()
            return("".join([l for l in test_file if l.isalpha()]))
        else:
            return("".join([l for l in t.lower() if l.isalpha()]))
        test_file.close()

    matricies = [(SourceModel(lang,io.StringIO(make_string(lang)))) for lang in langs]

    if fin[-5:] == ".test":
        print("Analyzing file", fin)
    else:
        print("Analyzing string", fin)

    probs = [matrix.probability(io.StringIO(make_string(fin))) for matrix in matricies]
    prob_norm = sum(probs)
    lang_norm = [(langs[tup],probs[tup]/prob_norm) for tup in range(len(langs))]
    order_lang = sorted(lang_norm, key = lambda x:x[1], reverse=True)

    for order in order_lang:
        print("Relative pobability that test string is " + str(order[0]) + "\t: " + format((order[1]), '.9f'))
