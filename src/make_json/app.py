import ast
JSON2DICT = 1
DICT2JSON = 2
class ShapingDict:

    indent=2
    def __init__(self, indent, mode):
        self.indent = indent
        self.mode = mode
    
    def dict2json(self, data):
        try:
            data = ast.literal_eval(data)
            if not type(data) in [dict, list]:
                raise Exception
        except:
            raise Exception('辞書型に形式があっていない')
        result = ''
        if isinstance(data,list):
            result = self.lists(data,result)
        elif isinstance(data,dict):
            result = self.dicts(data,result)
        return result

    def dicts(self, data, result, indent=0):
        lens =len(data)
        result+='{\n'
        indent +=1
        for i, key in enumerate(data):
            value=data.get(key)
            result+='{indent}"{v}": '.format(indent=" "*indent*self.indent,v=key)
            if isinstance(value,list):
                result=self.lists(value,result,indent)
            elif isinstance(value, dict):
                result = self.dicts(value,result,indent)
            else:
                result+=self.exchange(str(value))
            result+=',\n' if i < lens-1 else '\n'
        indent-=1
        result+=' '*indent*self.indent
        result+='}'

        return result

    def lists(self, data, result, indent=0):
        lens = len(data)
        result+='[\n'
        indent+=1
        for i, value in enumerate(data):
            result+=' '*indent*self.indent
            if isinstance(value,list):
                result = self.lists(value,result,indent)
            elif isinstance(value,dict):
                result = self.dicts(value,result,indent)
            else:
                result+=self.exchange(str(value))
            result+=',\n' if i <lens-1 else '\n'
        indent-=1
        result+=' '*indent*self.indent
        result+=']'
        return result

    def exchange(self, data):
        if self.mode == DICT2JSON:
            str_t1 = "True"
            str_f1 = "False"
            str_n1 = "None"
            str_t2 = "true"
            str_f2 = "false"
            str_n2 = "null"
        elif self.mode == JSON2DICT:
            str_t1 = "true"
            str_f1 = "false"
            str_n1 = "null"
            str_t2 = "True"
            str_f2 = "False"
            str_n2 = "None"
        else:
            return '"{}"'.format(data)
        if data == str_t1:
            data = str_t2
        elif data == str_f1:
            data = str_f2
        elif data == str_n1:
            data = str_n2
        else:
            data = '"{}"'.format(data)
        return data