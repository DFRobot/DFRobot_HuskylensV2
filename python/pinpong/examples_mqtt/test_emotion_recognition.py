"""
二哈识图V2 MQTT协议表情识别测试
需要实际的MQTT broker和二哈识图V2设备
"""

import sys
import time
import argparse
from dfrobot_huskylensv2_mqtt import (
    DFRobot_HuskylensV2,
    ALGORITHM_EMOTION_RECOGNITION
)

# 从主库导入默认配置
from dfrobot_huskylensv2_mqtt import (
    BROKER, PORT, TOPIC_CMD, TOPIC_RESP, 
    USERNAME, PASSWORD, TIMEOUT
)
USE_CONFIG_FILE = True


def print_separator():
    """打印分隔线"""
    print("=" * 60)


def test_connection(huskylens):
    """测试连接"""
    print_separator()
    print("测试1: 连接MQTT broker")
    print_separator()
    
    print(f"正在连接到 MQTT broker: {huskylens.broker_host}:{huskylens.broker_port}")
    connected = huskylens.connect()
    
    if connected:
        print("✓ 连接成功")
        return True
    else:
        print("✗ 连接失败")
        return False


def test_get_algorithm_list(huskylens):
    """测试获取算法列表"""
    print_separator()
    print("测试2: 获取算法列表")
    print_separator()
    
    print("正在获取算法列表...")
    algorithms = huskylens.getAlgorithmList()
    
    if algorithms is None:
        print("✗ 获取算法列表失败")
        return False
    
    print(f"✓ 成功获取算法列表，共 {len(algorithms)} 个算法:")
    print()
    for algo in algorithms:
        algo_id = algo.get('id', 'N/A')
        name_cn = algo.get('name_cn', 'N/A')
        name_en = algo.get('name_en', 'N/A')
        print(f"  ID: {algo_id:2d} | {name_cn:20s} | {name_en}")
    
    return True


def test_switch_algorithm(huskylens, algo_id, wait_time=5.0):
    """测试切换算法"""
    print_separator()
    print(f"测试3: 切换算法 (ID: {algo_id})")
    print_separator()
    
    print(f"正在切换到算法 ID: {algo_id}...")
    result = huskylens.switchAlgorithm(algo_id)
    
    if result:
        print(f"✓ 成功切换到算法 ID: {algo_id}")
        # 等待真实的切换进程完成
        if wait_time > 0:
            print(f"  等待 {wait_time} 秒，确保切换完成...")
            time.sleep(wait_time)
            print(f"  (已等待 {wait_time} 秒)")
        return True
    else:
        print(f"✗ 切换算法失败 (ID: {algo_id})")
        return False


def test_get_result(huskylens, algo_id):
    """测试获取识别结果"""
    print_separator()
    print(f"测试4: 获取识别结果 (算法 ID: {algo_id})")
    print_separator()
    
    print("正在获取识别结果...")
    count = huskylens.getResult(algo_id)
    
    if count is not None:
        print(f"✓ 成功获取识别结果，共 {count} 个结果")
        print("(结果已缓存，可通过其他API获取)")
        return True
    else:
        print("✗ 获取识别结果失败")
        return False


def test_available(huskylens, algo_id):
    """测试检查结果是否可用"""
    print_separator()
    print(f"测试5: 检查结果是否可用 (算法 ID: {algo_id})")
    print_separator()
    
    print("正在检查结果...")
    available = huskylens.available(algo_id)
    
    if available:
        print("✓ 结果可用")
        return True
    else:
        print("✗ 结果不可用")
        return False


def test_get_all_results(huskylens, algo_id):
    """测试获取并打印所有识别结果"""
    print_separator()
    print(f"测试6: 获取所有识别结果 (算法 ID: {algo_id})")
    print_separator()
    
    print("正在获取所有识别结果...")
    # 先调用 getResult 获取并缓存结果
    count = huskylens.getResult(algo_id)
    
    if count is not None and count > 0:
        print(f"✓ 找到 {count} 个识别结果")
        print()
        
        # 通过 getCachedResultByIndex 获取每个结果
        for index in range(count):
            block = huskylens.getCachedResultByIndex(algo_id, index)
            if block:
                print(f"结果 #{index + 1}:")
                print("-" * 60)
                # 排除 'used' 字段，不显示在输出中
                display_block = {k: v for k, v in block.items() if k != 'used'}
                sorted_keys = sorted(display_block.keys())
                for key in sorted_keys:
                    value = display_block[key]
                    if isinstance(value, list):
                        print(f"  {key:20s}: {value}")
                    else:
                        print(f"  {key:20s}: {value}")
                print("-" * 60)
                if index < count - 1:
                    print()
        return True
    elif count == 0:
        print("✗ 未找到识别结果")
        return False
    else:
        print("✗ 获取识别结果失败")
        return False


def test_get_cached_center_result(huskylens, algo_id):
    """测试获取中心结果"""
    print_separator()
    print(f"测试7: 获取中心结果 (算法 ID: {algo_id})")
    print_separator()
    
    print("正在获取中心结果...")
    result = huskylens.getCachedCenterResult(algo_id)
    
    if result:
        print("✓ 成功获取中心结果")
        print()
        print("中心结果详情:")
        print("-" * 60)
        # 排除 'used' 字段，不显示在输出中
        display_result = {k: v for k, v in result.items() if k != 'used'}
        sorted_keys = sorted(display_result.keys())
        for key in sorted_keys:
            value = display_result[key]
            if isinstance(value, list):
                print(f"  {key:20s}: {value}")
            else:
                print(f"  {key:20s}: {value}")
        print("-" * 60)
        return True
    else:
        print("✗ 未找到中心结果")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='二哈识图V2 MQTT表情识别测试')
    parser.add_argument('--host', type=str, default=BROKER,
                        help=f'MQTT broker地址 (默认: {BROKER})')
    parser.add_argument('--port', type=int, default=PORT,
                        help=f'MQTT broker端口 (默认: {PORT})')
    parser.add_argument('--command-topic', type=str, default=TOPIC_CMD,
                        help=f'命令主题 (默认: {TOPIC_CMD})')
    parser.add_argument('--response-topic', type=str, default=TOPIC_RESP,
                        help=f'响应主题 (默认: {TOPIC_RESP})')
    parser.add_argument('--username', type=str, default=USERNAME,
                        help='MQTT用户名 (可选)')
    parser.add_argument('--password', type=str, default=PASSWORD,
                        help='MQTT密码 (可选)')
    parser.add_argument('--timeout', type=float, default=TIMEOUT,
                        help=f'命令超时时间（秒）(默认: {TIMEOUT})')
    parser.add_argument('--algorithm', type=int, default=ALGORITHM_EMOTION_RECOGNITION,
                        help=f'要测试的算法ID (默认: {ALGORITHM_EMOTION_RECOGNITION} - 表情识别)')
    parser.add_argument('--skip-result-tests', action='store_true',
                        help='跳过结果相关的测试')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("二哈识图V2 MQTT协议表情识别测试")
    print("=" * 60)
    print()
    print("✓ 使用默认配置")
    print()
    print("配置信息:")
    print(f"  MQTT Broker: {args.host}:{args.port}")
    print(f"  命令主题: {args.command_topic}")
    print(f"  响应主题: {args.response_topic}")
    if args.username:
        print(f"  用户名: {args.username}")
    print(f"  超时时间: {args.timeout}秒")
    print(f"  测试算法ID: {args.algorithm} (表情识别)")
    print()
    
    huskylens = DFRobot_HuskylensV2(
        broker_host=args.host,
        broker_port=args.port,
        command_topic=args.command_topic,
        response_topic=args.response_topic,
        username=args.username,
        password=args.password,
        timeout=args.timeout
    )
    
    test_results = []
    
    try:
        if not test_connection(huskylens):
            print("\n连接失败，无法继续测试")
            return 1
        test_results.append(("连接", True))
        time.sleep(1)
        
        if test_get_algorithm_list(huskylens):
            test_results.append(("获取算法列表", True))
        else:
            test_results.append(("获取算法列表", False))
        time.sleep(1)
        
        if test_switch_algorithm(huskylens, args.algorithm):
            test_results.append(("切换算法", True))
        else:
            test_results.append(("切换算法", False))
        
        if not args.skip_result_tests:
            if test_get_result(huskylens, args.algorithm):
                test_results.append(("获取识别结果", True))
            else:
                test_results.append(("获取识别结果", False))
            time.sleep(1)
            
            if test_available(huskylens, args.algorithm):
                test_results.append(("检查结果可用性", True))
            else:
                test_results.append(("检查结果可用性", False))
            time.sleep(1)
            
            # 测试6: 获取所有识别结果
            if test_get_all_results(huskylens, args.algorithm):
                test_results.append(("获取所有识别结果", True))
            else:
                test_results.append(("获取所有识别结果", False))
            time.sleep(1)
            
            # 测试7: 获取中心结果
            if test_get_cached_center_result(huskylens, args.algorithm):
                test_results.append(("获取中心结果", True))
            else:
                test_results.append(("获取中心结果", False))
        
        print_separator()
        print("测试总结")
        print_separator()
        passed = sum(1 for _, result in test_results if result)
        total = len(test_results)
        print(f"总计: {total} 个测试")
        print(f"通过: {passed} 个")
        print(f"失败: {total - passed} 个")
        print()
        for test_name, result in test_results:
            status = "✓" if result else "✗"
            print(f"  {status} {test_name}")
        
        return 0 if passed == total else 1
        
    except KeyboardInterrupt:
        print("\n\n测试被用户中断")
        return 1
    except Exception as e:
        print(f"\n\n测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        print_separator()
        print("断开MQTT连接...")
        huskylens.disconnect()
        print("已断开连接")


if __name__ == '__main__':
    sys.exit(main())
