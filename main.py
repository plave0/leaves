from cmd import Cmd
import os
from pathlib import Path
import data_processing.configuration as config
import data_processing.recorder as r
import classification.random_forest as rdf

class ForestPromt(Cmd):
    prompt = '>> '

    def do_exit(self, inp):
        return True
    do_EOF = do_exit

    def do_printconf(self, inp):
        print(config.load_config())

    def do_printres(self, inp):
        res = r.load_res()
        print(res)

    def do_forests(self, inp):
        path = Path('data/forests')
        for filename in sorted(os.listdir(path)):
            print (filename)
    
    def do_editconf(self, inp):
        inp = inp.split()
        if inp[0] in ['cores_to_use',"number_of_trees","factor"]:
            config.change_config(inp[0],int(inp[1]))
        elif inp[0] == "dataset":
            config.change_config(inp[0],inp[1])
        else:
            print("Config doesn't exits.")

    def do_rdf(self, inp):
        rdf.build_forest(inp)

    def do_createconfig(self, inp):
        config.create_config_file()
    
    def do_createres(self, inp):
        r.create_res_file()
    
    def do_clear(self, inp):
       clear = lambda: os.system('clear')
       clear()

if __name__ == '__main__':  
    promt = ForestPromt()
    promt.cmdloop()
