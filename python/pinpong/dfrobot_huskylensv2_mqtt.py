"""
二哈识图V2 MQTT协议驱动库
基于HuskylensV2_Protocol_MQTT协议实现
"""

import json
import uuid
import threading
import time
from typing import Dict, List, Optional, Any
try:
    import paho.mqtt.client as mqtt
except ImportError:
    raise ImportError("请安装 paho-mqtt 库: pip install paho-mqtt")


# 算法常量定义
ALGORITHM_FACE_RECOGNITION = 1
ALGORITHM_OBJECT_RECOGNITION = 2
ALGORITHM_OBJECT_TRACKING = 3
ALGORITHM_COLOR_RECOGNITION = 4
ALGORITHM_OBJECT_CLASSIFICATION = 5
ALGORITHM_SELF_LEARNING_CLASSIFICATION = 6
ALGORITHM_SEGMENT = 7
ALGORITHM_HAND_RECOGNITION = 8
ALGORITHM_POSE_RECOGNITION = 9
ALGORITHM_LICENSE_RECOGNITION = 10
ALGORITHM_OCR_RECOGNITION = 11
ALGORITHM_LINE_TRACKING = 12
ALGORITHM_EMOTION_RECOGNITION = 13
ALGORITHM_GAZE_RECOGNITION = 14
ALGORITHM_FACE_ORIENTATION = 15
ALGORITHM_TAG_RECOGNITION = 16
ALGORITHM_BARCODE_RECOGNITION = 17
ALGORITHM_QRCODE_RECOGNITION = 18
ALGORITHM_FALLDOWN_RECOGNITION = 19


# MQTT默认配置常量
# 这些常量可以在导入时使用，也可以作为 DFRobot_HuskylensV2 的默认参数
DEFAULT_BROKER_HOST = "127.0.0.1"
DEFAULT_BROKER_PORT = 1883
DEFAULT_COMMAND_TOPIC = "usr/cmd"
DEFAULT_RESPONSE_TOPIC = "usr/response"
DEFAULT_USERNAME = "huskylens"
DEFAULT_PASSWORD = "dfrobot"
DEFAULT_TIMEOUT = 5.0

# 为了向后兼容，提供别名
BROKER = DEFAULT_BROKER_HOST
PORT = DEFAULT_BROKER_PORT
TOPIC_CMD = DEFAULT_COMMAND_TOPIC
TOPIC_RESP = DEFAULT_RESPONSE_TOPIC
USERNAME = DEFAULT_USERNAME
PASSWORD = DEFAULT_PASSWORD
TIMEOUT = DEFAULT_TIMEOUT


class DFRobot_HuskylensV2:
    """
    二哈识图V2 MQTT协议驱动类
    """
    
    def __init__(self, broker_host: str = DEFAULT_BROKER_HOST, broker_port: int = DEFAULT_BROKER_PORT,
                 command_topic: str = DEFAULT_COMMAND_TOPIC,
                 response_topic: str = DEFAULT_RESPONSE_TOPIC,
                 client_id: Optional[str] = None,
                 username: Optional[str] = DEFAULT_USERNAME,
                 password: Optional[str] = DEFAULT_PASSWORD,
                 timeout: float = DEFAULT_TIMEOUT):
        """
        初始化二哈识图V2 MQTT客户端
        
        @param broker_host: MQTT broker地址
        @param broker_port: MQTT broker端口
        @param command_topic: 命令发布主题
        @param response_topic: 响应订阅主题
        @param client_id: MQTT客户端ID，如果为None则自动生成
        @param username: MQTT用户名（可选）
        @param password: MQTT密码（可选）
        @param timeout: 命令超时时间（秒）
        """
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.command_topic = command_topic
        self.response_topic = response_topic
        self.timeout = timeout
        
        # 生成客户端ID
        if client_id is None:
            client_id = f"huskylens_client_{uuid.uuid4().hex[:8]}"
        
        # 创建MQTT客户端
        self.client = mqtt.Client(client_id=client_id)
        if username and password:
            self.client.username_pw_set(username, password)
        
        # 响应存储字典，key为correlation_id
        self.responses: Dict[str, Dict] = {}
        self.response_lock = threading.Lock()
        self.response_events: Dict[str, threading.Event] = {}
        
        # 当前结果缓存
        self.result_cache: Dict[int, Dict] = {}
        self.result_cache_lock = threading.Lock()
        
        # 设置回调函数
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
        
        # 连接状态
        self.connected = False
        self.connection_lock = threading.Lock()
        
    def _on_connect(self, client, userdata, flags, rc):
        """MQTT连接回调"""
        if rc == 0:
            self.connected = True
            # 订阅响应主题
            client.subscribe(self.response_topic)
            print(f"已连接到MQTT broker，订阅主题: {self.response_topic}")
        else:
            self.connected = False
            print(f"MQTT连接失败，错误代码: {rc}")
    
    def _on_message(self, client, userdata, msg):
        """MQTT消息接收回调"""
        try:
            payload = json.loads(msg.payload.decode('utf-8'))
            correlation_id = payload.get('correlation_id')
            
            if correlation_id:
                with self.response_lock:
                    self.responses[correlation_id] = payload
                    # 触发等待的事件
                    if correlation_id in self.response_events:
                        self.response_events[correlation_id].set()
                
                # 如果是get_result响应，更新结果缓存
                if payload.get('cmd') == 'get_result' and payload.get('ret') == 'success':
                    result_data = payload.get('results', [])
                    if result_data:
                        try:
                            # 如果result_data是字符串，先解析
                            if isinstance(result_data, str):
                                result_data = json.loads(result_data)
                            
                            # 将results列表转换为按算法ID组织的字典格式
                            result_dict = {}
                            
                            if isinstance(result_data, list):
                                # 按算法ID分组
                                for result_item in result_data:
                                    if isinstance(result_item, dict):
                                        algo_id = result_item.get('algorithm')
                                        if algo_id is not None:
                                            if algo_id not in result_dict:
                                                result_dict[algo_id] = {'blocks': []}
                                            # 规范化结果项（转换坐标字段格式）
                                            normalized_item = self._normalize_result_item(result_item)
                                            # 添加 'used' 标记，用于 popCachedResult
                                            normalized_item['used'] = False
                                            result_dict[algo_id]['blocks'].append(normalized_item)
                            elif isinstance(result_data, dict):
                                # 如果已经是字典格式，直接使用
                                result_dict = result_data
                            
                            with self.result_cache_lock:
                                self.result_cache = result_dict
                        except (json.JSONDecodeError, TypeError):
                            pass
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"解析MQTT消息失败: {e}")
    
    def _on_disconnect(self, client, userdata, rc):
        """MQTT断开连接回调"""
        self.connected = False
        if rc != 0:
            print(f"MQTT意外断开连接，错误代码: {rc}")
    
    def connect(self):
        """连接到MQTT broker"""
        try:
            self.client.connect(self.broker_host, self.broker_port, 60)
            self.client.loop_start()
            # 等待连接建立
            for _ in range(50):  # 最多等待5秒
                if self.connected:
                    return True
                time.sleep(0.1)
            return False
        except Exception as e:
            print(f"连接MQTT broker失败: {e}")
            return False
    
    def disconnect(self):
        """断开MQTT连接"""
        self.client.loop_stop()
        self.client.disconnect()
        self.connected = False
    
    def _send_command(self, command: Dict[str, Any]) -> Optional[Dict]:
        """
        发送MQTT命令并等待响应
        
        @param command: 命令字典
        @return: 响应字典，如果超时或失败则返回None
        """
        if not self.connected:
            if not self.connect():
                return None
        
        # 生成correlation_id
        correlation_id = str(uuid.uuid4())
        command['correlation_id'] = correlation_id
        
        # 创建事件用于等待响应
        event = threading.Event()
        with self.response_lock:
            self.response_events[correlation_id] = event
        
        try:
            # 发布命令
            payload = json.dumps(command, ensure_ascii=False)
            result = self.client.publish(self.command_topic, payload, qos=1)
            
            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                print(f"发布命令失败，错误代码: {result.rc}")
                return None
            
            # 等待响应
            if event.wait(timeout=self.timeout):
                with self.response_lock:
                    response = self.responses.pop(correlation_id, None)
                    self.response_events.pop(correlation_id, None)
                    return response
            else:
                print(f"等待响应超时: {correlation_id}")
                with self.response_lock:
                    self.response_events.pop(correlation_id, None)
                return None
        except Exception as e:
            print(f"发送命令失败: {e}")
            with self.response_lock:
                self.response_events.pop(correlation_id, None)
            return None
    
    def getAlgorithmList(self) -> Optional[List[Dict]]:
        """
        获取二哈识图V2支持的算法列表
        
        @return: 算法列表，格式为 [{"id": 1, "name_en": "", "name_cn": "", ...}, ...]
                 如果失败或没有algorithms字段则返回None
        """
        command = {"cmd": "algorithm_list"}
        response = self._send_command(command)
        
        if response and response.get('ret') == 'success':
            # 检查是否有algorithms字段
            if 'algorithms' in response:
                algorithms = response.get('algorithms')
                if isinstance(algorithms, list):
                    return algorithms
        return None
    
    def switchAlgorithm(self, algo: int) -> bool:
        """
        切换二哈识图V2的内置算法
        
        @param algo: 二哈识图V2内置算法
        @return: 成功返回True，失败返回False
        
        注意：此方法不包含等待时间参数，如需等待时间，请在调用此方法的测试代码中实现
        """
        command = {
            "cmd": "switch_algorithm",
            "algorithm": algo
        }
        response = self._send_command(command)
        
        if response and response.get('ret') == 'success':
            return True
        return False
    
    def _normalize_result_item(self, item: Dict) -> Dict:
        """
        规范化结果项，将数组格式的坐标字段转换为分离的x, y字段
        例如: leye: [373, 86] -> leye_x: 373, leye_y: 86
        
        @param item: 原始结果项
        @return: 规范化后的结果项
        """
        normalized = item.copy()
        
        # 需要转换的字段列表（数组格式 -> x, y格式）
        coordinate_fields = [
            'leye', 'reye', 'lmouth', 'rmouth', 'nose',
            'wrist', 'thumb_cmc', 'thumb_mcp', 'thumb_ip', 'thumb_tip',
            'index_finger_mcp', 'index_finger_pip', 'index_finger_dip', 'index_finger_tip',
            'middle_finger_mcp', 'middle_finger_pip', 'middle_finger_dip', 'middle_finger_tip',
            'ring_finger_mcp', 'ring_finger_pip', 'ring_finger_dip', 'ring_finger_tip',
            'pinky_finger_mcp', 'pinky_finger_pip', 'pinky_finger_dip', 'pinky_finger_tip',
            'lear', 'rear', 'lshoulder', 'rshoulder', 'lelbow', 'relbow',
            'lwrist', 'rwrist', 'lhip', 'rhip', 'lknee', 'rknee', 'lankle', 'rankle'
        ]
        
        for field in coordinate_fields:
            if field in normalized:
                value = normalized[field]
                if isinstance(value, list) and len(value) >= 2:
                    # 转换为 x, y 格式
                    normalized[f'{field}_x'] = value[0]
                    normalized[f'{field}_y'] = value[1]
                    # 保留原始字段（可选，如果需要的话）
                    # normalized[field] = value
        
        return normalized
    
    def getResult(self, algo: int) -> Optional[int]:
        """
        获取二哈识图V2的识别结果并缓存
        
        @param algo: 二哈识图内置算法
        @return: 识别到的结果数量，如果失败则返回None
        
        注意：此方法不包含等待时间参数，如需等待时间，请在调用此方法的测试代码中实现
        """
        command = {"cmd": "get_result"}
        response = self._send_command(command)
        
        if response and response.get('ret') == 'success':
            # 获取results字段（可能是列表或字符串）
            result_data = response.get('results', [])
            
            if result_data:
                try:
                    # 如果result_data是字符串，先解析
                    if isinstance(result_data, str):
                        result_data = json.loads(result_data)
                    
                    # 将results列表转换为按算法ID组织的字典格式
                    # 实际格式: results = [{'algorithm': 1, 'id': 1, 'xCenter': 526, ...}, ...]
                    # 目标格式: {algo_id: {'blocks': [...]}}
                    result_dict = {}
                    
                    if isinstance(result_data, list):
                        # 按算法ID分组
                        for result_item in result_data:
                            if isinstance(result_item, dict):
                                algo_id = result_item.get('algorithm')
                                if algo_id is not None:
                                    if algo_id not in result_dict:
                                        result_dict[algo_id] = {'blocks': []}
                                    # 规范化结果项（转换坐标字段格式）
                                    normalized_item = self._normalize_result_item(result_item)
                                    # 添加 'used' 标记，用于 popCachedResult
                                    normalized_item['used'] = False
                                    result_dict[algo_id]['blocks'].append(normalized_item)
                    elif isinstance(result_data, dict):
                        # 如果已经是字典格式，直接使用
                        result_dict = result_data
                    
                    # 更新缓存
                    with self.result_cache_lock:
                        self.result_cache = result_dict
                    
                    # 返回指定算法的结果数量
                    if algo in result_dict:
                        algo_result = result_dict[algo]
                        blocks = algo_result.get('blocks', [])
                        if isinstance(blocks, list):
                            return len(blocks)
                    return 0
                except (json.JSONDecodeError, TypeError) as e:
                    print(f"解析结果失败: {e}")
                    return None
        return None
    
    def available(self, algo: int) -> bool:
        """
        如果此算法的结果存在于当前缓存中
        
        @param algo: 二哈识图内置算法
        @return: True/False
        """
        with self.result_cache_lock:
            if algo in self.result_cache:
                algo_result = self.result_cache[algo]
                # 检查是否有blocks且blocks不为空
                if isinstance(algo_result, dict):
                    blocks = algo_result.get('blocks', [])
                    if isinstance(blocks, list) and len(blocks) > 0:
                        return True
            return False
    
    def getCachedCenterResult(self, algo: int) -> Optional[Dict]:
        """
        获取二哈识图V2中最接近摄像头中心的结果信息
        
        @param algo: 二哈识图内置算法
        @return: 最接近中心的结果block，如果不存在则返回None
        """
        with self.result_cache_lock:
            if algo not in self.result_cache:
                return None
            
            algo_result = self.result_cache[algo]
            if not isinstance(algo_result, dict):
                return None
            
            blocks = algo_result.get('blocks', [])
            if not isinstance(blocks, list) or len(blocks) == 0:
                return None
            
            # 摄像头中心坐标（默认320x240分辨率，中心为160,120）
            # 如果结果中有分辨率信息，可以使用实际分辨率
            center_x, center_y = 160, 120
            
            # 找到最接近中心的block
            min_distance = float('inf')
            closest_block = None
            
            for block in blocks:
                if not isinstance(block, dict):
                    continue
                
                # 获取中心坐标
                x_center = block.get('xCenter', 0)
                y_center = block.get('yCenter', 0)
                
                # 计算到中心的距离
                distance = ((x_center - center_x) ** 2 + (y_center - center_y) ** 2) ** 0.5
                
                if distance < min_distance:
                    min_distance = distance
                    closest_block = block
            
            return closest_block
    
    def getCachedResultByIndex(self, algo: int, index: int) -> Optional[Dict]:
        """
        获取二哈识图V2中指定索引的结果信息
        
        @param algo: 二哈识图内置算法
        @param index: 结果索引号（从0开始）
        @return: 指定索引的结果，如果不存在则返回None
        """
        with self.result_cache_lock:
            if algo not in self.result_cache:
                return None
            
            algo_result = self.result_cache[algo]
            if not isinstance(algo_result, dict):
                return None
            
            blocks = algo_result.get('blocks', [])
            if not isinstance(blocks, list):
                return None
            
            if 0 <= index < len(blocks):
                return blocks[index]
            return None
    
    def getCachedResultByID(self, algo: int, ID: int) -> Optional[Dict]:
        """
        获取二哈识图V2中指定ID的结果信息
        
        @param algo: 二哈识图内置算法
        @param ID: 指定ID
        @return: 指定ID的结果，如果存在多个则返回第一个，如果不存在则返回None
        """
        with self.result_cache_lock:
            if algo not in self.result_cache:
                return None
            
            algo_result = self.result_cache[algo]
            if not isinstance(algo_result, dict):
                return None
            
            blocks = algo_result.get('blocks', [])
            if not isinstance(blocks, list):
                return None
            
            # 查找匹配ID的block
            for block in blocks:
                if isinstance(block, dict) and block.get('ID') == ID:
                    return block
            
            return None
    
    def getCachedIndexResultByID(self, algo: int, ID: int, index: int) -> Optional[Dict]:
        """
        获取二哈识图V2中指定ID和索引的结果信息
        
        @param algo: 二哈识图内置算法
        @param ID: 指定ID
        @param index: 结果索引号（同一ID的第n个结果）
        @return: 指定ID和索引的结果，如果不存在则返回None
        """
        with self.result_cache_lock:
            if algo not in self.result_cache:
                return None
            
            algo_result = self.result_cache[algo]
            if not isinstance(algo_result, dict):
                return None
            
            blocks = algo_result.get('blocks', [])
            if not isinstance(blocks, list):
                return None
            
            # 查找匹配ID的blocks
            matching_blocks = []
            for block in blocks:
                if isinstance(block, dict) and block.get('ID') == ID:
                    matching_blocks.append(block)
            
            # 返回指定索引的结果
            if 0 <= index < len(matching_blocks):
                return matching_blocks[index]
            
            return None
    
    def popCachedResult(self, algo: int) -> Optional[Dict]:
        """
        从缓存中弹出一个未使用的结果（类似队列的pop操作）
        
        @param algo: 二哈识图内置算法
        @return: 一个未使用的结果block，如果所有结果都已使用或没有结果则返回None
        """
        with self.result_cache_lock:
            if algo not in self.result_cache:
                return None
            
            algo_result = self.result_cache[algo]
            if not isinstance(algo_result, dict):
                return None
            
            blocks = algo_result.get('blocks', [])
            if not isinstance(blocks, list):
                return None
            
            # 查找第一个未使用的结果（通过检查是否有 'used' 标记）
            # 如果没有 'used' 标记，则认为未使用
            for block in blocks:
                if isinstance(block, dict):
                    # 如果block没有'used'标记，或者'used'为False，则返回它
                    if 'used' not in block or not block.get('used', False):
                        # 标记为已使用
                        block['used'] = True
                        return block
            
            return None
    
    def getResultByID(self, algo: int, ID: int) -> Optional[Dict]:
        """
        从设备获取指定ID的结果（先获取最新结果，然后返回指定ID的结果）
        
        @param algo: 二哈识图内置算法
        @param ID: 指定ID
        @return: 指定ID的结果，如果不存在则返回None
        """
        # 先获取最新结果
        self.getResult(algo)
        # 然后从缓存中获取指定ID的结果
        return self.getCachedResultByID(algo, ID)
    
    def getCachedResultNum(self, algo: int) -> int:
        """
        获取缓存中的结果总数
        
        @param algo: 二哈识图内置算法
        @return: 缓存中的结果总数，如果没有缓存则返回0
        """
        with self.result_cache_lock:
            if algo not in self.result_cache:
                return 0
            
            algo_result = self.result_cache[algo]
            if not isinstance(algo_result, dict):
                return 0
            
            blocks = algo_result.get('blocks', [])
            if isinstance(blocks, list):
                return len(blocks)
            return 0
    
    def getCachedResultLearnedNum(self, algo: int) -> int:
        """
        获取缓存中已学习的结果数量（ID != 0）
        
        @param algo: 二哈识图内置算法
        @return: 已学习的结果数量，如果没有缓存则返回0
        """
        count = 0
        with self.result_cache_lock:
            if algo not in self.result_cache:
                return 0
            
            algo_result = self.result_cache[algo]
            if not isinstance(algo_result, dict):
                return 0
            
            blocks = algo_result.get('blocks', [])
            if isinstance(blocks, list):
                for block in blocks:
                    if isinstance(block, dict):
                        block_id = block.get('ID', 0)
                        if block_id != 0:
                            count += 1
        return count
    
    def getCachedResultNumByID(self, algo: int, ID: int) -> int:
        """
        获取缓存中指定ID的结果数量
        
        @param algo: 二哈识图内置算法
        @param ID: 指定ID
        @return: 指定ID的结果数量，如果没有缓存则返回0
        """
        count = 0
        with self.result_cache_lock:
            if algo not in self.result_cache:
                return 0
            
            algo_result = self.result_cache[algo]
            if not isinstance(algo_result, dict):
                return 0
            
            blocks = algo_result.get('blocks', [])
            if isinstance(blocks, list):
                for block in blocks:
                    if isinstance(block, dict) and block.get('ID') == ID:
                        count += 1
        return count
    
    def getCachedResultMaxID(self, algo: int) -> Optional[int]:
        """
        获取缓存中的最大ID
        
        @param algo: 二哈识图内置算法
        @return: 缓存中的最大ID，如果没有缓存或没有结果则返回None
        """
        max_id = None
        with self.result_cache_lock:
            if algo not in self.result_cache:
                return None
            
            algo_result = self.result_cache[algo]
            if not isinstance(algo_result, dict):
                return None
            
            blocks = algo_result.get('blocks', [])
            if isinstance(blocks, list) and len(blocks) > 0:
                for block in blocks:
                    if isinstance(block, dict):
                        block_id = block.get('ID')
                        if block_id is not None:
                            if max_id is None or block_id > max_id:
                                max_id = block_id
        return max_id
    
    def learn(self, algo: int) -> Optional[int]:
        """
        学习当前目标
        
        @param algo: 二哈识图内置算法
        @return: 学习到的ID，如果失败则返回None
        """
        command = {
            "cmd": "learn",
            "algorithm": algo
        }
        response = self._send_command(command)
        
        if response and response.get('ret') == 'success':
            # 返回学习到的ID
            learned_id = response.get('id')
            return learned_id if learned_id is not None else None
        return None
    
    def learnBlock(self, algo: int, x: int, y: int, width: int, height: int) -> Optional[int]:
        """
        学习方框中的物体
        
        @param algo: 二哈识图内置算法
        @param x: 方框左上角X坐标
        @param y: 方框左上角Y坐标
        @param width: 方框宽度
        @param height: 方框高度
        @return: 学习到的ID，如果失败则返回None
        """
        command = {
            "cmd": "learn_block",
            "algorithm": algo,
            "x": x,
            "y": y,
            "width": width,
            "height": height
        }
        response = self._send_command(command)
        
        if response and response.get('ret') == 'success':
            # 返回学习到的ID
            learned_id = response.get('id')
            return learned_id if learned_id is not None else None
        return None
    
    def forget(self, algo: int) -> bool:
        """
        忘记已学习的内容
        
        @param algo: 二哈识图内置算法
        @return: 成功返回True，失败返回False
        """
        command = {
            "cmd": "forget",
            "algorithm": algo
        }
        response = self._send_command(command)
        
        return response is not None and response.get('ret') == 'success'
    
    def saveKnowledges(self, algo: int, knowledgeID: int) -> bool:
        """
        保存知识库
        
        @param algo: 二哈识图内置算法
        @param knowledgeID: 知识库ID
        @return: 成功返回True，失败返回False
        """
        command = {
            "cmd": "save_knowledges",
            "algorithm": algo,
            "knowledges_id": knowledgeID
        }
        response = self._send_command(command)
        
        return response is not None and response.get('ret') == 'success'
    
    def loadKnowledges(self, algo: int, knowledgeID: int) -> bool:
        """
        加载知识库
        
        @param algo: 二哈识图内置算法
        @param knowledgeID: 知识库ID
        @return: 成功返回True，失败返回False
        """
        command = {
            "cmd": "load_knowledges",
            "algorithm": algo,
            "knowledges_id": knowledgeID
        }
        response = self._send_command(command)
        
        return response is not None and response.get('ret') == 'success'
    
    def setNameByID(self, algo: int, ID: int, name: str) -> bool:
        """
        设置已学习对象的名称
        
        @param algo: 二哈识图内置算法
        @param ID: 对象ID
        @param name: 对象名称
        @return: 成功返回True，失败返回False
        """
        command = {
            "cmd": "set_name_by_id",
            "algorithm": algo,
            "ID": ID,
            "name": name
        }
        response = self._send_command(command)
        
        return response is not None and response.get('ret') == 'success'
    
    def getAlgorithmParams(self, algo: int, param_keys: Optional[List[str]] = None) -> Dict:
        """
        获取算法参数
        
        @param algo: 二哈识图内置算法
        @param param_keys: 要获取的参数键列表，如果为None则获取所有参数
        @return: 参数字典，格式为 {param_key: {type, value, ...}}
        """
        command = {
            "cmd": "get_algorithm_params",
            "algorithm": algo
        }
        response = self._send_command(command)
        
        if response and response.get('ret') == 'success':
            params = response.get('params', {})
            if param_keys is None:
                # 返回所有参数
                return params
            else:
                # 只返回指定的参数
                result = {}
                for key in param_keys:
                    if key in params:
                        result[key] = params[key]
                return result
        return {}
    
    def setAlgorithmParams(self, algo: int, params: Dict) -> bool:
        """
        设置算法参数
        
        @param algo: 二哈识图内置算法
        @param params: 参数字典，格式为 {param_key: value} 或 [{param_key: value}, ...]
        @return: 成功返回True，失败返回False
        """
        # 将参数字典转换为列表格式
        if isinstance(params, dict):
            param_list = [{k: v} for k, v in params.items()]
        elif isinstance(params, list):
            param_list = params
        else:
            return False
        
        command = {
            "cmd": "set_algorithm_params",
            "algorithm": algo,
            "params": param_list
        }
        response = self._send_command(command)
        
        return response is not None and response.get('ret') == 'success'
    
    def setMultiAlgorithm(self, algos: List[int]) -> bool:
        """
        设置多算法
        
        @param algos: 算法ID列表（2-3个算法）
        @return: 成功返回True，失败返回False
        """
        if len(algos) < 2 or len(algos) > 3:
            return False
        
        command = {
            "cmd": "set_multi_algorithm",
            "algorithms": algos
        }
        response = self._send_command(command)
        
        return response is not None and response.get('ret') == 'success'
    
    def setMultiAlgorithmRatio(self, ratios: List[int]) -> bool:
        """
        设置多算法算力分配
        
        @param ratios: 算力分配比例列表（2-3个比例）
        @return: 成功返回True，失败返回False
        """
        if len(ratios) < 2 or len(ratios) > 3:
            return False
        
        command = {
            "cmd": "set_multi_ratio",
            "ratios": ratios
        }
        response = self._send_command(command)
        
        return response is not None and response.get('ret') == 'success'
    
    def drawRect(self, color, lineWidth: int, x: int, y: int, width: int, height: int) -> bool:
        """
        绘制矩形
        
        @param color: 颜色，可以是RGB值列表 [R, G, B] 或整数颜色值 (如 0xFFFFFF)
        @param lineWidth: 线宽
        @param x: 左上角X坐标
        @param y: 左上角Y坐标
        @param width: 矩形宽度
        @param height: 矩形高度
        @return: 成功返回True，失败返回False
        """
        # 转换颜色格式：如果是整数，转换为RGB列表
        if isinstance(color, int):
            r = (color >> 16) & 0xFF
            g = (color >> 8) & 0xFF
            b = color & 0xFF
            color_list = [r, g, b]
        elif isinstance(color, (list, tuple)) and len(color) == 3:
            color_list = list(color)
        else:
            return False
        
        command = {
            "cmd": "draw_rect",
            "color": color_list,
            "line_width": lineWidth,
            "x": x,
            "y": y,
            "width": width,
            "height": height
        }
        response = self._send_command(command)
        
        return response is not None and response.get('ret') == 'success'
    
    def drawUniqueRect(self, color, lineWidth: int, x: int, y: int, width: int, height: int) -> bool:
        """
        绘制唯一矩形（覆盖之前的矩形）
        
        @param color: 颜色，可以是RGB值列表 [R, G, B] 或整数颜色值 (如 0xFFFFFF)
        @param lineWidth: 线宽
        @param x: 左上角X坐标
        @param y: 左上角Y坐标
        @param width: 矩形宽度
        @param height: 矩形高度
        @return: 成功返回True，失败返回False
        """
        # 转换颜色格式：如果是整数，转换为RGB列表
        if isinstance(color, int):
            r = (color >> 16) & 0xFF
            g = (color >> 8) & 0xFF
            b = color & 0xFF
            color_list = [r, g, b]
        elif isinstance(color, (list, tuple)) and len(color) == 3:
            color_list = list(color)
        else:
            return False
        
        command = {
            "cmd": "draw_unique_rect",
            "color": color_list,
            "line_width": lineWidth,
            "x": x,
            "y": y,
            "width": width,
            "height": height
        }
        response = self._send_command(command)
        
        return response is not None and response.get('ret') == 'success'
    
    def clearRect(self) -> bool:
        """
        清除矩形
        
        @return: 成功返回True，失败返回False
        """
        command = {
            "cmd": "clear_rect"
        }
        response = self._send_command(command)
        
        return response is not None and response.get('ret') == 'success'
    
    def drawText(self, color, fontSize: int, x: int, y: int, text: str) -> bool:
        """
        绘制文字
        
        @param color: 颜色，可以是RGB值列表 [R, G, B] 或整数颜色值 (如 0xFFFFFF)
        @param fontSize: 字体大小
        @param x: 文字X坐标
        @param y: 文字Y坐标
        @param text: 文字内容
        @return: 成功返回True，失败返回False
        """
        # 转换颜色格式：如果是整数，转换为RGB列表
        if isinstance(color, int):
            r = (color >> 16) & 0xFF
            g = (color >> 8) & 0xFF
            b = color & 0xFF
            color_list = [r, g, b]
        elif isinstance(color, (list, tuple)) and len(color) == 3:
            color_list = list(color)
        else:
            return False
        
        command = {
            "cmd": "draw_text",
            "color": color_list,
            "font_size": fontSize,
            "x": x,
            "y": y,
            "text": text
        }
        response = self._send_command(command)
        
        return response is not None and response.get('ret') == 'success'
    
    def clearText(self) -> bool:
        """
        清除文字
        
        @return: 成功返回True，失败返回False
        """
        command = {
            "cmd": "clear_text"
        }
        response = self._send_command(command)
        
        return response is not None and response.get('ret') == 'success'
    
    def takePhoto(self, resolution: str = "640x480") -> Optional[str]:
        """
        拍照
        
        @param resolution: 分辨率，支持 "640x480", "1280x720", "1920x1080"
        @return: 照片文件名，如果失败则返回None
        """
        if resolution not in ["640x480", "1280x720", "1920x1080"]:
            return None
        
        command = {
            "cmd": "take_photo",
            "resolution": resolution
        }
        response = self._send_command(command)
        
        if response and response.get('ret') == 'success':
            filename = response.get('filename')
            return filename if filename else None
        return None
    
    def takeScreenshot(self) -> Optional[str]:
        """
        截屏
        
        @return: 截图文件名，如果失败则返回None
        """
        command = {
            "cmd": "take_screenshot"
        }
        response = self._send_command(command)
        
        if response and response.get('ret') == 'success':
            filename = response.get('filename')
            return filename if filename else None
        return None
    
    def playMusic(self, filename: str, volume: int = 100) -> bool:
        """
        播放音乐
        
        @param filename: 音乐文件名
        @param volume: 音量（0-100），默认100
        @return: 成功返回True，失败返回False
        """
        command = {
            "cmd": "play_music",
            "filename": filename,
            "volume": volume
        }
        response = self._send_command(command)
        
        return response is not None and response.get('ret') == 'success'
    
    def startRecording(self, mediaType: int, duration: int, filename: str = "", resolution: str = "640x480") -> bool:
        """
        开始录音/录像
        
        @param mediaType: 媒体类型，1=音频，2=视频
        @param duration: 录制时长（秒）
        @param filename: 文件名（可选）
        @param resolution: 分辨率，仅用于视频，支持 "640x480", "1280x720", "1920x1080"
        @return: 成功返回True，失败返回False
        """
        if mediaType == 2:  # 视频
            if resolution not in ["640x480", "1280x720", "1920x1080"]:
                return False
            command = {
                "cmd": "start_record_video",
                "duration": duration,
                "resolution": resolution
            }
        else:  # 音频
            command = {
                "cmd": "start_record_audio",
                "duration": duration
            }
        
        if filename:
            command["filename"] = filename
        
        response = self._send_command(command)
        
        return response is not None and response.get('ret') == 'success'
    
    def stopRecording(self, mediaType: int) -> bool:
        """
        停止录音/录像
        
        @param mediaType: 媒体类型，1=音频，2=视频
        @return: 成功返回True，失败返回False
        """
        if mediaType == 2:  # 视频
            command = {
                "cmd": "stop_record_video"
            }
        else:  # 音频
            command = {
                "cmd": "stop_record_audio"
            }
        
        response = self._send_command(command)
        
        return response is not None and response.get('ret') == 'success'
    
    def __enter__(self):
        """上下文管理器入口"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.disconnect()

