"""
模型上下文协议（MCP）示例代码
演示如何创建 MCP 服务器和客户端
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
import json
from llm_config import create_llm


@dataclass
class MCPResource:
    """MCP 资源 - 静态数据"""
    uri: str
    name: str
    description: str
    mime_type: str
    data: Any


@dataclass
class MCPTool:
    """MCP 工具 - 可执行函数"""
    name: str
    description: str
    parameters: Dict[str, Any]
    function: callable


@dataclass
class MCPrompt:
    """MCP 提示 - 交互模板"""
    name: str
    description: str
    template: str


class MCPServer(ABC):
    """MCP 服务器抽象基类"""

    def __init__(self, server_name: str):
        self.server_name = server_name
        self.resources: List[MCPResource] = []
        self.tools: Dict[str, MCPTool] = {}
        self.prompts: List[MCPrompt] = []

    @abstractmethod
    def register_resources(self):
        """注册资源"""
        pass

    @abstractmethod
    def register_tools(self):
        """注册工具"""
        pass

    def register_prompt(self, name: str, description: str, template: str):
        """注册提示"""
        prompt = MCPrompt(name, description, template)
        self.prompts.append(prompt)

    def get_resource(self, uri: str) -> Optional[MCPResource]:
        """获取资源"""
        for resource in self.resources:
            if resource.uri == uri:
                return resource
        return None

    def list_resources(self) -> List[Dict]:
        """列出所有资源"""
        return [
            {
                'uri': r.uri,
                'name': r.name,
                'description': r.description,
                'mime_type': r.mime_type
            }
            for r in self.resources
        ]

    def list_tools(self) -> List[Dict]:
        """列出所有工具"""
        return [
            {
                'name': t.name,
                'description': t.description,
                'parameters': t.parameters
            }
            for t in self.tools.values()
        ]

    def execute_tool(self, tool_name: str, arguments: Dict) -> Any:
        """执行工具"""
        if tool_name not in self.tools:
            raise ValueError(f"工具 '{tool_name}' 不存在")

        tool = self.tools[tool_name]
        return tool.function(**arguments)

    def list_prompts(self) -> List[Dict]:
        """列出所有提示"""
        return [
            {
                'name': p.name,
                'description': p.description
            }
            for p in self.prompts
        ]


class FileSystemMCPServer(MCPServer):
    """文件系统 MCP 服务器示例"""

    def __init__(self, root_directory: str = "/tmp/mcp_files"):
        super().__init__("filesystem_server")
        self.root_directory = root_directory
        self.register_resources()
        self.register_tools()

    def register_resources(self):
        """注册文件系统资源"""
        # 模拟注册一些资源
        self.resources.append(
            MCPResource(
                uri="file:///documents/readme.md",
                name="README",
                description="项目说明文档",
                mime_type="text/markdown",
                data="# 项目说明\n\n这是一个使用 MCP 的项目。"
            )
        )

    def register_tools(self):
        """注册文件系统工具"""

        def list_directory(path: str = ".") -> List[str]:
            """列出目录内容"""
            # 简化实现，返回模拟数据
            files = [
                "document1.txt",
                "document2.md",
                "data.csv",
                "config.json"
            ]
            print(f"  列出目录: {path}")
            return files

        def read_file(filepath: str) -> str:
            """读取文件内容"""
            print(f"  读取文件: {filepath}")
            # 简化实现
            return f"这是 {filepath} 的内容"

        def write_file(filepath: str, content: str) -> bool:
            """写入文件内容"""
            print(f"  写入文件: {filepath}")
            # 简化实现
            return True

        def create_directory(directory: str) -> bool:
            """创建目录"""
            print(f"  创建目录: {directory}")
            # 简化实现
            return True

        # 注册工具
        self.tools["list_directory"] = MCPTool(
            name="list_directory",
            description="列出指定目录中的文件和子目录",
            parameters={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "要列出的目录路径"
                    }
                }
            },
            function=list_directory
        )

        self.tools["read_file"] = MCPTool(
            name="read_file",
            description="读取文件内容",
            parameters={
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "要读取的文件路径"
                    }
                }
            },
            function=read_file
        )

        self.tools["write_file"] = MCPTool(
            name="write_file_file",
            description="写入内容到文件",
            parameters={
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "要写入的文件路径"
                    },
                    "content": {
                        "type": "string",
                        "description": "要写入的内容"
                    }
                }
            },
            function=write_file
        )

        self.tools["create_directory"] = MCPTool(
            name="create_directory",
            description="创建新目录",
            parameters={
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "要创建的目录路径"
                    }
                }
            },
            function=create_directory
        )


class DatabaseMCPServer(MCPServer):
    """数据库 MCP 服务器示例"""

    def __init__(self):
        super().__init__("database_server")
        self.mock_data = {
            "users": [
                {"id": 1, "name": "张三", "email": "zhangsan@example.com"},
                {"id": 2, "name": "李四", "email": "lisi@example.com"},
                {"id": 3, "name": "王五", "email": "wangwu@example.com"}
            ]
        }
        self.register_resources()
        self.register_tools()

    def register_resources(self):
        """注册数据库资源"""
        pass  # 数据库资源通常通过工具访问

    def register_tools(self):
        """注册数据库工具"""

        def query_database(query: str) -> List[Dict]:
            """执行数据库查询"""
            print(f"  执行查询: {query[:50]}...")
            # 简化实现
            return self.mock_data["users"]

        def get_user_by_id(user_id: int) -> Optional[Dict]:
            """根据ID获取用户"""
            print(f"  查询用户ID: {user_id}")
            for user in self.mock_data["users"]:
                if user["id"] == user_id:
                    return user
            return None

        def insert_user(name: str, email: str) -> Dict:
            """插入新用户"""
            print(f"  插入用户: {name}")
            new_id = len(self.mock_data["users"]) + 1
            new_user = {"id": new_id, "name": name, "email": email}
            self.mock_data["users"].append(new_user)
            return new_user

        def update_user(user_id: int, **kwargs) -> bool:
            """更新用户信息"""
            print(f"  更新用户ID: {user_id}")
            for user in self.mock_data["users"]:
                if user["id"] == user_id:
                    user.update(kwargs)
                    return True
            return False

        # 注册工具
        self.tools["query_database"] = MCPTool(
            name="query_database",
            description="执行SQL查询",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "SQL查询语句"
                    }
                }
            },
            function=query_database
        )

        self.tools["get_user_by_id"] = MCPTool(
            name="get_user_by_id",
            description="根据ID获取用户",
            parameters={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "用户ID"
                    }
                }
            },
            function=get_user_by_id
        )

        self.tools["insert_user"] = MCPTool(
            name="insert_user",
            description="插入新用户",
            parameters={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "用户姓名"
                    },
                    "email": {
                        "type": "string",
                        "description": "用户邮箱"
                    }
                }
            },
            function=insert_user
        )

        self.tools["update_user"] = MCPTool(
            name="update_user",
            description="更新用户信息",
            parameters={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "用户ID"
                    },
                    "name": {
                        "type": "string",
                        "description": "新用户姓名"
                    },
                    "email": {
                        "type": "string",
                        "description": "新用户邮箱"
                    }
                }
            },
            function=update_user
        )


class MCPClient:
    """MCP 客户端"""

    def __init__(self, name: str):
        self.name = name
        self.connected_servers: Dict[str, MCPServer] = {}

    def connect_to_server(self, server: MCPServer):
        """连接到 MCP 服务器"""
        print(f"\n{self.name} 连接到服务器: {server.server_name}")
        self.connected_servers[server.server_name] = server

        # 发现服务器能力
        print(f"  发现 {len(server.list_resources())} 个资源")
        print(f"  发现 {len(server.list_tools())} 个工具")
        print(f"  发现 {len(server.list_prompts())} 个提示")

    def discover_tools(self, server_name: str) -> List[Dict]:
        """发现服务器上的工具"""
        if server_name not in self.connected_servers:
            raise ValueError(f"未连接到服务器: {server_name}")

        server = self.connected_servers[server_name]
        return server.list_tools()

    def call_tool(self, server_name: str, tool_name: str, arguments: Dict) -> Any:
        """调用服务器上的工具"""
        if server_name not in self.connected_servers:
            raise ValueError(f"未连接到服务器: {server_name}")

        print(f"\n{self.name} 调用工具: {server_name}.{tool_name}")
        print(f"  参数: {arguments}")

        server = self.connected_servers[server_name]
        result = server.execute_tool(tool_name, arguments)

        print(f"  结果: {result}")
        return result

    def get_resource(self, server_name: str, uri: str) -> Optional[MCPResource]:
        """获取服务器上的资源"""
        if server_name not in self.connected_servers:
            raise ValueError(f"未连接到服务器: {server_name}")

        server = self.connected_servers[server_name]
        return server.get_resource(uri)


class MCPAgent:
    """使用 MCP 的智能体"""

    def __init__(self, name: str, llm):
        self.name = name
        self.llm = llm
        self.mcp_client = MCPClient(f"{name}_client")

    def connect_mcp_server(self, server: MCPServer):
        """连接 MCP 服务器"""
        self.mcp_client.connect_to_server(server)

    def process_request(self, user_request: str) -> str:
        """处理用户请求"""
        print(f"\n{'='*60}")
        print(f"智能体 {self.name} 处理请求: {user_request}")
        print(f"{'='*60}\n")

        # 分析请求并决定使用哪个工具
        analysis = self._analyze_request(user_request)
        print(f"分析结果: {analysis}")

        # 执行工具调用
        if analysis['action'] == 'list_files':
            server_name = analysis['server']
            files = self.mcp_client.call_tool(
                server_name,
                "list_directory",
                {"path": analysis.get('path', '.')}
            )
            return f"找到 {len(files)} 个文件: {files}"

        elif analysis['action'] == 'read_file':
            server_name = analysis['server']
            content = self.mcp_client.call_tool(
                server_name,
                "read_file",
                {"filepath": analysis['filepath']}
            )
            return content

        elif analysis['action'] == 'query_database':
            server_name = analysis['server']
            results = self.mcp_client.call_tool(
                server_name,
                "query_database",
                {"query": analysis['query']}
            )
            return f"查询返回 {len(results)} 条结果"

        else:
            return "无法理解请求"

    def _analyze_request(self, request: str) -> Dict:
        """分析请求（简化版本）"""
        request_lower = request.lower()

        if "文件" in request_lower and ("列表" in request_lower or "列出" in request_lower):
            return {
                'action': 'list_files',
                'server': 'filesystem_server',
                'path': '.'
            }
        elif "读取" in request_lower and "文件" in request_lower:
            return {
                'action': 'read_file',
                'server': 'filesystem_server',
                'filepath': 'document1.txt'
            }
        elif "查询" in request_lower and "数据库" in request_lower:
            return {
                'action': 'query_database',
                'server': 'database_server',
                'query': 'SELECT * FROM users'
            }
        else:
            return {'action': 'unknown'}


def demonstrate_mcp_filesystem():
    """演示文件系统 MCP 服务器"""
    print("=== 文件系统 MCP 服务器演示 ===")

    # 创建文件系统服务器
    fs_server = FileSystemMCPServer()

    # 创建客户端
    client = MCPClient("测试客户端")

    # 连接服务器
    client.connect_to_server(fs_server)

    # 列出可用工具
    print(f"\n可用工具:")
    for tool in client.discover_tools("filesystem_server"):
        print(f"  - {tool['name']}: {tool['description']}")

    # 调用工具
    print("\n调用 list_directory 工具:")
    files = client.call_tool("filesystem_server", "list_directory", {"path": "."})

    print("\n调用 read_file 工具:")
    content = client.call_tool("filesystem_server", "read_file", {"filepath": "document1.txt"})


def demonstrate_mcp_database():
    """演示数据库 MCP 服务器"""
    print("\n" + "="*60)
    print("=== 数据库 MCP 服务器演示 ===")

    # 创建数据库服务器
    db_server = DatabaseMCPServer()

    # 创建客户端
    client = MCPClient("测试客户端")

    # 连接服务器
    client.connect_to_server(db_server)

    # 列出可用工具
    print(f"\n可用工具:")
    for tool in client.discover_tools("database_server"):
        print(f"  - {tool['name']}: {tool['description']}")

    # 调用工具
    print("\n调用 query_database 工具:")
    users = client.call_tool("database_server", "query_database", {"query": "SELECT * FROM users"})

    print("\n调用 get_user_by_id 工具:")
    user = client.call_tool("database_server", "get_user_by_id", {"user_id": 1})

    print("\n调用 insert_user 工具:")
    new_user = client.call_tool("database_server", "insert_user", {
        "name": "赵六",
        "email": "zhaoliu@example.com"
    })


def demonstrate_mcp_agent():
    """演示使用 MCP 的智能体"""
    print("\n" + "="*60)
    print("=== MCP 智能体演示 ===")

    # 创建 LLM
    llm = create_llm(temperature=0.3)

    # 创建智能体
    agent = MCPAgent("文件助手", llm)

    # 连接 MCP 服务器
    fs_server = FileSystemMCPServer()
    db_server = DatabaseMCPServer()

    agent.connect_mcp_server(fs_server)
    agent.connect_mcp_server(db_server)

    # 处理请求
    requests = [
        "列出当前目录的文件",
        "读取 document1.txt 文件",
        "查询数据库中的所有用户"
    ]

    for request in requests:
        response = agent.process_request(request)
        print(f"\n响应: {response}\n")


if __name__ == "__main__":
    try:
        demonstrate_mcp_filesystem()
        demonstrate_mcp_database()
        demonstrate_mcp_agent()

        print("\n" + "="*60)
        print("MCP 演示完成！")
        print("="*60)

    except Exception as e:
        print(f"错误: {e}")
        print("请确保已正确设置 OPENAI_API_KEY 环境变量")
