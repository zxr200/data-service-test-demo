import requests            #http请求库，向后端API发送数据

class DataService:
    #validate_dataset()检查数据的有效性
    def validate_dataset(self,dataset): #传入要检查的数据集dataset
        #dataset是一个字典，包括名称name，数据行数rows，数据来源source

        #检查名称
        if not dataset.get('name'):
            return False,"数据集名称不能为空"

        if len(dataset.get('name',''))<2:  #.get('name','')如果name的值不存在就返回空字符串
            return False,"数据集名称至少为2个字符"

        #检查行数
        rows=dataset.get('rows')
        if rows is None:
            return False,"数据行数不能为空"

        if not isinstance(rows,int):   #isinstance()用来类型检查
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


    #process_dataset()将有效的数据发送到服务器
    def process_dataset(self,dataset):

        #先调用validate_dataset()检查数据是否合格，如果验证失败，要返回错误信息
        is_valid,message=self.validate_dataset(dataset)
        if not is_valid:
            return False,message

        try:
            # 发送数据到服务器
            response=requests.post( #用post()发送数据到指定网址
                'https://api.data-service.com/analyze',
                json=dataset, #数据以JASON格式发送
                timeout=5  #设置5秒超时，5秒内没响应就会报错
            )

            #处理响应结果
            if response.status_code==200:  #status_code是固有属性
                return True,"数据处理成功"
            else:
                return False,(f"数据处理失败，状态码：{response.status_code}")

        #异常处理
        except requests.exceptions.Timeout:
            return False,"数据处理超时"
        except Exception as e:
            return False,f"数据处理异常，{str(e)}"
