from cmd import Cmd
import data_processing.configuration as config
import classification.random_forest as rdf

class ForestPromt(Cmd):
    prompt = '>> '

    def do_exit(self, inp):
        return True
    do_EOF = do_exit

    def do_printconf(self, inp):
        print(config.load_config())
    
    def do_editconf(self, inp):
        inp = inp.split()
        if inp[0] in ['cores_to_use',"number_of_trees","factor"]:
            config.change_config(inp[0],int(inp[1]))
        elif inp[0] == "dataset":
            config.change_config(inp[0],inp[1])
        else:
            print("Config doesn't exits.")

    def do_rdf(self, inp):
        rdf.build_forest()

if __name__ == '__main__':
    promt = ForestPromt()
    promt.cmdloop()
