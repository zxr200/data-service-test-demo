# 专业测试演示项目

## 项目简介

本项目展示了如何为python业务代码构建完整的测试，使用pytest框架实现

## 主要技术

-**pytest框架**：编写并运行测试

-**参数化测试**：`@pytest.mark.parametrize`覆盖多种测试场景

-**Mock技术**：`unittest.mock`隔离外部依赖，保证稳定性和速度

-**Fixture管理**:`pytest.fixture`提高代码复用性

## 项目结构

-`data_service.py`:业务逻辑，即数据验证与处理

-`test_data_service.py`:测试

-`requirements.txt`:项目依赖

-`README.md`:项目说明