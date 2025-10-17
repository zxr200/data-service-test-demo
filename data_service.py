import requests            #http请求库，向后端API发送数据

class DataService:
    def validate_dataset(self,dataset):

        #检查名称
        if not dataset.get('name'):
            return False,"数据集名称不能为空"

        if len(dataset.get('name',''))<2:
            return False,"数据集名称至少为2个字符"

        #检查行数
        rows=dataset.get('rows')
        if rows is None:
            return False,"数据行数不能为空"

        if not isinstance(rows,int):
            return False,"数据行数必须为整数"

        if rows <=0:
            return False,"数据行数必须大于0"

        if rows >1000000:
            return False,"数据行数不能大于1000000"

        #检查数据源
        source=dataset.get('source')
        if not source:
            return False,"数据源不能为空"

        #上述检查全都通过 返回成功的元组
        return True,"数据集验证成功"

    def process_dataset(self,dataset):
        is_valid,message=self.validate_dataset(dataset)
        if not is_valid:
            return False,message

        try:
            response=requests.post(
                'https://api.data-service.com/analyze',
                json=dataset,
                timeout=5
            )
            if response.status_code==200:
                return True,"数据处理成功"
            else:
                return False,(f"数据处理失败，状态码：{response.status_code}")
        except requests.exceptions.Timeout:
            return False,"数据处理超时"
        except Exception as e:
            return False,f"数据处理异常，{str(e)}"
