# 数据服务测试演示项目

## 项目简介

本项目展示了如何为python业务代码构建完整的测试，测试使用pytest框架实现

## 主要技术

-**pytest框架**：编写并运行测试

-**Fixture**：`pytest.fixture`提供可以重用的测试资源，保证测试的独立性

-**参数化测试**：`@pytest.mark.parametrize`覆盖多种测试场景

-**Mock技术**：`unittest.mock`隔离外部依赖，保证稳定性和速度


## 项目结构

-`data_service.py`:业务逻辑，包括对数据有效性的验证和数据处理

-`test_data_service.py`:对业务逻辑的测试

-`requirements.txt`:列出了项目运行所需要的所有第三方库

-`README.md`:项目说明文档

## 业务逻辑

**1.数据有效性的验证(`validate_dataset`)：**

-数据集名称：不能为空且至少2个字符

-数据行数：不能为空且是整数，范围是大于0，小于1000000

-数据源：不能为空

**2.数据处理(`process_dataset`)：**

-验证数据的有效性：调用`validate_dataset()`

-把有效的数据发送到服务器：`requests.post()`

-处理响应结果：检查`response.status_code`

-处理异常情况：检查异常类型

## 测试体系

### 1.Fixture

-使用Fixture，一个是`data_service`，一个是`valid_dataset`

-`data_service`提供测试对象实例

-`valid_dataset`提供正确有效的测试数据

-如果没有Fixture，就需要在每个测试中写创建测试对象实例和定义有效测试数据的代码，这样代码重复还容易出错

-而Pytest运行测试时，每个测试都会获得新的Fixture实例，这样测试独立，互不干扰

### 2.参数化测试

-**数据验证测试**：使用参数化测试一次性验证`validate_dataset()`的所有验证规则，覆盖了所有可能的场景，共7个测试用例，如果不使用参数化测试，那么就需要编写7个单独的测试函数。而这样提高了测试覆盖率，也避免了代码重复

-**API响应测试**：使用参数化测试验证外部API的响应处理，包括2种API响应状态码，也就是2个测试用例

### 3.Mock

-用Mock来隔离`process_dataset`中的`requests.post`这个网络请求，因为`requests.post()`是外部依赖，它依赖网络连接和远程服务器的状态，可能会导致测试速度慢、测试结果不稳定，而进行测试只是为了验证业务逻辑，所以用Mock替换掉它

**正常响应测试：**

-在测试中模拟网络请求，返回响应结果：

-`@patch('data_service.requests.post')`将真实的`requests.post`替换为`mock_post` 

-`test_process_dataset_with_mock(self,mock_post,...):`让`mock_post`返回假的响应，来模拟API的正常响应，测试响应成功或失败的处理

**异常情况测试：**

-在测试中模拟网络请求超时的异常情况：

-`@patch('data_service.requests.post')`将真实的`requests.post`替换为`mock_post`

-`test_process_dataset_timeout(self,mock_post,...):`让`mock_post`抛出超时异常，测试异常情况的处理

**行为验证：**`test_process_dataset_with_mock`中的`mock_post.assert_called_once_with`验证业务代码用正确的参数调用外部API

## 运行

`pytest -v`

## 测试结果

![测试结果](result.png)

