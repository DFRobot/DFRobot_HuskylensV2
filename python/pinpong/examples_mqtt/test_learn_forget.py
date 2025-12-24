"""
二哈识图V2 MQTT协议学习与忘记功能测试
测试learn、learnBlock、forget相关的方法
需要实际的MQTT broker和二哈识图V2设备
"""

import sys
import time
import argparse
from dfrobot_huskylensv2_mqtt import (
    DFRobot_HuskylensV2,
    ALGORITHM_FACE_RECOGNITION
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


def test_switch_algorithm(huskylens, algo_id, wait_time=5.0):
    """测试切换算法"""
    print_separator()
    print(f"测试2: 切换算法 (ID: {algo_id})")
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


def test_learn(huskylens, algo_id):
    """测试学习当前目标"""
    print_separator()
    print(f"测试3: 学习当前目标 (算法 ID: {algo_id})")
    print_separator()
    
    print("正在学习当前目标...")
    print("(请确保设备前有可识别的目标)")
    learned_id = huskylens.learn(algo_id)
    
    if learned_id is not None:
        print(f"✓ 学习成功，学习到的ID: {learned_id}")
        return True, learned_id
    else:
        print("✗ 学习失败")
        print("  (可能原因: 没有可识别的目标，或学习过程出错)")
        return False, None


def test_learn_block(huskylens, algo_id, x, y, width, height):
    """测试学习指定区域"""
    print_separator()
    print(f"测试4: 学习指定区域 (算法 ID: {algo_id})")
    print_separator()
    
    print(f"正在学习指定区域 (x={x}, y={y}, width={width}, height={height})...")
    learned_id = huskylens.learnBlock(algo_id, x, y, width, height)
    
    if learned_id is not None:
        print(f"✓ 学习成功，学习到的ID: {learned_id}")
        return True, learned_id
    else:
        print("✗ 学习失败")
        print("  (可能原因: 指定区域没有可识别的目标，或学习过程出错)")
        return False, None


def test_forget(huskylens, algo_id):
    """测试忘记已学习的内容"""
    print_separator()
    print(f"测试5: 忘记已学习的内容 (算法 ID: {algo_id})")
    print_separator()
    
    print("正在忘记已学习的内容...")
    result = huskylens.forget(algo_id)
    
    if result:
        print("✓ 忘记成功")
        return True
    else:
        print("✗ 忘记失败")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='二哈识图V2 MQTT学习与忘记功能测试')
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
    parser.add_argument('--algorithm', type=int, default=ALGORITHM_FACE_RECOGNITION,
                        help=f'要测试的算法ID (默认: {ALGORITHM_FACE_RECOGNITION} - 人脸识别)')
    parser.add_argument('--skip-learn', action='store_true',
                        help='跳过学习测试')
    parser.add_argument('--skip-learn-block', action='store_true',
                        help='跳过学习区域测试')
    parser.add_argument('--skip-forget', action='store_true',
                        help='跳过忘记测试')
    parser.add_argument('--learn-block-x', type=int, default=0,
                        help='学习区域的X坐标 (默认: 0)')
    parser.add_argument('--learn-block-y', type=int, default=0,
                        help='学习区域的Y坐标 (默认: 0)')
    parser.add_argument('--learn-block-width', type=int, default=320,
                        help='学习区域的宽度 (默认: 320)')
    parser.add_argument('--learn-block-height', type=int, default=240,
                        help='学习区域的高度 (默认: 240)')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("二哈识图V2 MQTT协议学习与忘记功能测试")
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
    print(f"  测试算法ID: {args.algorithm} (人脸识别)")
    print()
    print("注意:")
    print("  - 此测试会先切换到人脸识别算法，等待5秒")
    print("  - 学习功能需要设备前有可识别的目标")
    print("  - 学习区域测试需要指定正确的坐标和尺寸")
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
    learned_id = None
    
    try:
        # 测试1: 连接
        if not test_connection(huskylens):
            print("\n连接失败，无法继续测试")
            return 1
        test_results.append(("连接", True))
        time.sleep(1)
        
        # 测试2: 切换到人脸识别算法（必须，学习功能需要先切换算法）
        if not test_switch_algorithm(huskylens, args.algorithm):
            print("\n切换算法失败，无法继续测试")
            return 1
        test_results.append(("切换算法", True))
        # 注意：test_switch_algorithm内部已等待5秒
        
        # 测试3: 学习当前目标
        if not args.skip_learn:
            success, learned_id = test_learn(huskylens, args.algorithm)
            test_results.append(("学习当前目标", success))
            time.sleep(1)
        else:
            print_separator()
            print("跳过学习当前目标测试")
            print_separator()

        huskylens.drawRect([0,255,0], 2, args.learn_block_x, args.learn_block_y, args.learn_block_width, args.learn_block_height)
        print("请将要学习的物体放在Rect中，等待10秒")
        time.sleep(10)
        # 测试4: 学习指定区域
        if not args.skip_learn_block:
            success, block_id = test_learn_block(
                huskylens, args.algorithm,
                args.learn_block_x, args.learn_block_y,
                args.learn_block_width, args.learn_block_height
            )
            test_results.append(("学习指定区域", success))
            if block_id is not None:
                learned_id = block_id
            time.sleep(1)
        else:
            print_separator()
            print("跳过学习指定区域测试")
            print_separator()
        time.sleep(5)
        huskylens.clearRect()
        # 测试5: 忘记已学习的内容
        if not args.skip_forget:
            if test_forget(huskylens, args.algorithm):
                test_results.append(("忘记已学习内容", True))
            else:
                test_results.append(("忘记已学习内容", False))
        else:
            print_separator()
            print("跳过忘记测试")
            print_separator()
        
        # 打印测试总结
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
        
        if learned_id is not None:
            print()
            print(f"学习到的ID: {learned_id}")
        
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
        # 断开连接
        print_separator()
        print("断开MQTT连接...")
        huskylens.disconnect()
        print("已断开连接")


if __name__ == '__main__':
    sys.exit(main())

