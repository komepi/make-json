"""辞書型を整形する

"""
import ast
from make_json.config import (
    TRUE_DICT,
    FALSE_DICT,
    NULL_DICT,
    TRUE_JSON,
    FALSE_JSON,
    NULL_JSON)

JSON2DICT = 1
DICT2JSON = 2

class ShapingDict:
    """辞書型を整形

    python, jsonの辞書型を文字列として受け取り、それをpython, jsonの
    辞書型に整形した文字列を返す。
    
    Attributes:
        indent (int): スペースによるインデント数
    """


    indent=2


    def __init__(self, indent: int, mode: int):
        """初期化

        Args:
            indent (int): スペースによるインデント数
            mode (int): python->jsonかjson->pythonかを指定.JSON2DICTかDICT2JSONをわたす。
        """
        self.indent = indent
        self.mode = mode
        
        if mode == JSON2DICT:
            self.exchange_config = {
                "true":{"to":TRUE_DICT, "from": TRUE_JSON},
                "false":{"to":FALSE_DICT, "from":FALSE_JSON},
                "null":{"to":NULL_DICT, "from": NULL_JSON}
            }
        elif mode == DICT2JSON:
            self.exchange_config = {
                "true":{"to":TRUE_JSON, "from": TRUE_DICT},
                "false":{"to":FALSE_JSON, "from":FALSE_DICT},
                "null":{"to":NULL_JSON, "from": NULL_DICT}
            }


    def dict2json(self, data: str):
        """受け取った文字列を整形済みの文字列にする

        Args:
            data (str): 整形対象の文字列

        Raises:
            Exception: pythonの文字列に変形できない場合発生

        Returns:
            str: 整形済み文字列
        """
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


    def dicts(self, data: dict, result: str, indent=0):
        """辞書型を整形
        辞書型を受け取り、整形する。
        
        Args:
            data (dict): 整形対象データ
            result (str): 現在整形済みの文字列
            indent (int, optional): 対象辞書型が存在するインデント.
                                    Defaults to 0.

        Returns:
            str: 現在整形済みの文字列

        Examples:
            dataとして{"key1":"value1", "key2":"value2"}を受け取るとする。
            以下のように整形される。
            '{
                "key1": "value1",
                "key2": "value2"
            }'
        """
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


    def lists(self, data: list, result: str, indent=0):
        """リスト型を整形
        リスト型を受け取り、整形する。

        Args:
            data (list): 整形対象データ
            result (str): 現在整形済みの文字列
            indent (int, optional): 対象辞書型が存在するインデント. Defaults to 0.

        Returns:
            str: 現在整形済みの文字列

        Examples:
            dataとして["value1", "value2"]を受け取るとする。
            
            以下のように整形される。
            
            '[
                "value1",
                "value2"
            ]'
        """
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


    def exchange(self, data: str):
        """jsonとpythonでの違いの修正
        Trueとtrue, Falseとfalse, Noneとnullを変換する。
        それ以外はそのまま返す。

        Args:
            data (str): 変換対象の文字列

        Returns:
            str: 変換後の文字列
        """
        def _exchange(data, config):
            if data == config["from"]:
                return config["to"]
            else: # data == config["to"]:
                return data
        if data in list(self.exchange_config["true"].values()):
            data = _exchange(data, self.exchange_config["true"])
        elif data in list(self.exchange_config["false"].values()):
            data = _exchange(data, self.exchange_config["false"])
        elif data in list(self.exchange_config["null"].values()):
            data = _exchange(data, self.exchange_config["null"])
        else:
            return '"{}"'.format(data)
        return data
        #if self.mode == DICT2JSON:
        #    str_t1 = "True"
        #    str_f1 = "False"
        #    str_n1 = "None"
        #    str_t2 = "true"
        #    str_f2 = "false"
        #    str_n2 = "null"
        #elif self.mode == JSON2DICT:
        #    str_t1 = "true"
        #    str_f1 = "false"
        #    str_n1 = "null"
        #    str_t2 = "True"
        #    str_f2 = "False"
        #    str_n2 = "None"
        #else:
        #    return '"{}"'.format(data)
        #if data == str_t1:
        #    data = str_t2
        #elif data == str_f1:
        #    data = str_f2
        #elif data == str_n1:
        #    data = str_n2
        #else:
        #    data = '"{}"'.format(data)
        #return data
