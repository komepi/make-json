"""辞書型を整形する

"""
import ast
from collections import OrderedDict
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


    def __init__(self, indent: int, mode: int, is_shaping=True,
                 is_ordereddict_to_dict=True):
        """初期化

        Args:
            indent (int): スペースによるインデント数
            mode (int): python->jsonかjson->pythonかを指定.JSON2DICTかDICT2JSONをわたす。
        """
        self.indent = indent
        self.mode = mode
        self.is_shaping=is_shaping
        self.is_ordereddict_to_dict=is_ordereddict_to_dict
        if self.is_shaping:
            self.newline_str="\n"
        else:
            self.newline_str=""
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

    def _convert_ordereddict2dict(self,item: object):
        """OrderedDictを含むオブジェクトを辞書型に変換

        :param item: OrderedDictを含む変換対象
        :type item: object
        :return: 変換後
        :rtype: dict, list
        """
        if isinstance(item, list):
            return [self._convert_ordereddict2dict(elem) for elem in item]
        elif isinstance(item, tuple):
            return tuple(self._convert_ordereddict2dict(elem) for elem in item)
        elif isinstance(item, OrderedDict):
            return {key: self._convert_ordereddict2dict(value) for key, value in item.items()}
        elif isinstance(item, dict):
            return {key: self._convert_ordereddict2dict(value) for key, value in item.items()}
        else:
            return item

    def convert(self, data: str):
        """受け取った文字列を整形済みの文字列にする

        Args:
            data (str): 整形対象の文字列

        Raises:x
            Exception: pythonの文字列に変形できない場合発生

        Returns:
            str: 整形済み文字列
        """
        try:
            if "OrderedDict" in data:
                data = eval(data)
                if not self.is_ordereddict_to_dict:
                    data = self._convert_ordereddict2dict(data)
            else:
                data = ast.literal_eval(data)
            if not type(data) in [dict, list, OrderedDict]:
                raise Exception
        except:
            raise Exception('辞書型に形式があっていない')
        result = ''
        if isinstance(data,list):
            result = self.lists(data,result)
        elif isinstance(data,OrderedDict):
            result = self.ordereddicts(data,result)
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
        result+='{'+self.newline_str
        indent +=1
        for i, key in enumerate(data):
            value=data.get(key)
            result+='{indent}"{v}": '.format(indent=" "*indent*self.indent if self.is_shaping else "",v=key)
            if isinstance(value,list):
                result=self.lists(value,result,indent)
            elif isinstance(value, OrderedDict):
                result = self.ordereddicts(value,result,indent)
            elif isinstance(value, dict):
                result = self.dicts(value,result,indent)
            else:
                result+=self.exchange(value)
            result+=','+self.newline_str if i < lens-1 else self.newline_str
        indent-=1
        result+=' '*indent*self.indent if self.is_shaping else ""
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
        result+='['+self.newline_str
        indent+=1
        for i, value in enumerate(data):
            result+=' '*indent*self.indent if self.is_shaping else ""
            if isinstance(value,list):
                result = self.lists(value,result,indent)
            elif isinstance(value,OrderedDict):
                result = self.ordereddicts(value,result,indent)
            elif isinstance(value,dict):
                result = self.dicts(value,result,indent)
            else:
                result+=self.exchange(value)
            result+=','+self.newline_str if i <lens-1 else self.newline_str
        indent-=1
        result+=' '*indent*self.indent if self.is_shaping else ''
        result+=']'
        return result

    def ordereddicts(self, data, result, indent=0):
        lens = len(data)
        result += 'OrderedDict(['+self.newline_str
        indent+=1
        for i, key in enumerate(data):
            value = data.get(key)
            result += '{indent}("{v}", '.format(indent=" "*indent*self.indent if self.is_shaping else "", v=key)
            if isinstance(value, list):
                result=self.lists(value,result,indent)
            elif isinstance(value,OrderedDict):
                result=self.ordereddicts(value,result,indent)
            elif isinstance(value, dict):
                result=self.dicts(value,result,indent)
            else:
                result+=self.exchange(value)
            result += '),'+self.newline_str if i < lens-1 else ')'+self.newline_str
        indent-=1
        result+=' '*indent*self.indent if self.is_shaping else ""
        result+='])'
        
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
        _data = str(data)
        if _data in list(self.exchange_config["true"].values()):
            data = _exchange(_data, self.exchange_config["true"])
        elif _data in list(self.exchange_config["false"].values()):
            data = _exchange(_data, self.exchange_config["false"])
        elif _data in list(self.exchange_config["null"].values()):
            data = _exchange(_data, self.exchange_config["null"])
        else:
            if isinstance(data,str):
                return '"{}"'.format(_data)
            elif isinstance(data,int) or isinstance(data,float):
                return '{}'.format(_data)
        return data
