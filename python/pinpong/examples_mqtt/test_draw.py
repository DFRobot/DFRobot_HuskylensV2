"""
二哈识图V2 MQTT协议绘制功能测试
测试draw和clear相关的方法
需要实际的MQTT broker和二哈识图V2设备
"""

import sys
import time
import argparse
from dfrobot_huskylensv2_mqtt import (
    DFRobot_HuskylensV2,
    ALGORITHM_FACE_RECOGNITION
)

# 颜色常量定义
COLOR_RED = 0xFF0000      # 红色
COLOR_GREEN = 0x00FF00    # 绿色
COLOR_BLUE = 0x0000FF     # 蓝色
COLOR_WHITE = 0xFFFFFF    # 白色
COLOR_YELLOW = 0xFFFF00   # 黄色

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


def test_draw_rect(huskylens):
    """测试绘制矩形"""
    print_separator()
    print("测试3: 绘制矩形")
    print_separator()
    
    print("正在绘制红色矩形 (x=100, y=100, width=200, height=150, lineWidth=3)...")
    result = huskylens.drawRect(COLOR_RED, 3, 100, 100, 200, 150)
    
    if result:
        print("✓ 绘制矩形成功")
        print("  (使用整数颜色值: 0xFF0000)")
        return True
    else:
        print("✗ 绘制矩形失败")
        return False


def test_draw_rect_rgb(huskylens):
    """测试使用RGB列表绘制矩形"""
    print_separator()
    print("测试4: 使用RGB列表绘制矩形")
    print_separator()
    
    print("正在绘制绿色矩形 (x=150, y=150, width=180, height=120, lineWidth=2)...")
    result = huskylens.drawRect([0, 255, 0], 2, 150, 150, 180, 120)
    
    if result:
        print("✓ 绘制矩形成功")
        print("  (使用RGB列表: [0, 255, 0])")
        return True
    else:
        print("✗ 绘制矩形失败")
        return False


def test_draw_unique_rect(huskylens):
    """测试绘制唯一矩形"""
    print_separator()
    print("测试5: 绘制唯一矩形")
    print_separator()
    
    print("正在绘制蓝色唯一矩形 (x=200, y=200, width=160, height=100, lineWidth=4)...")
    result = huskylens.drawUniqueRect(COLOR_BLUE, 4, 200, 200, 160, 100)
    
    if result:
        print("✓ 绘制唯一矩形成功")
        print("  (唯一矩形会覆盖之前的矩形)")
        return True
    else:
        print("✗ 绘制唯一矩形失败")
        return False


def test_draw_text(huskylens):
    """测试绘制文字"""
    print_separator()
    print("测试6: 绘制文字")
    print_separator()
    
    print("正在绘制文字 (位置: x=50, y=50, 字体大小: 20)...")
    result = huskylens.drawText(COLOR_YELLOW, 20, 50, 50, "Hello Huskylens!")
    
    if result:
        print("✓ 绘制文字成功")
        print("  (使用黄色文字: 0xFFFF00)")
        return True
    else:
        print("✗ 绘制文字失败")
        return False


def test_draw_text_rgb(huskylens):
    """测试使用RGB列表绘制文字"""
    print_separator()
    print("测试7: 使用RGB列表绘制文字")
    print_separator()
    
    print("正在绘制文字 (位置: x=50, y=80, 字体大小: 20)...")
    result = huskylens.drawText([255, 255, 255], 20, 50, 80, "MQTT Test")
    
    if result:
        print("✓ 绘制文字成功")
        print("  (使用RGB列表: [255, 255, 255] - 白色)")
        return True
    else:
        print("✗ 绘制文字失败")
        return False


def test_clear_rect(huskylens):
    """测试清除矩形"""
    print_separator()
    print("测试8: 清除矩形")
    print_separator()
    
    print("正在清除矩形...")
    result = huskylens.clearRect()
    
    if result:
        print("✓ 清除矩形成功")
        return True
    else:
        print("✗ 清除矩形失败")
        return False


def test_clear_text(huskylens):
    """测试清除文字"""
    print_separator()
    print("测试9: 清除文字")
    print_separator()
    
    print("正在清除文字...")
    result = huskylens.clearText()
    
    if result:
        print("✓ 清除文字成功")
        return True
    else:
        print("✗ 清除文字失败")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='二哈识图V2 MQTT绘制功能测试')
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
                        help=f'用于切换的算法ID (默认: {ALGORITHM_FACE_RECOGNITION})')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("二哈识图V2 MQTT协议绘制功能测试")
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
    print(f"  用于切换的算法ID: {args.algorithm}")
    print()
    print("注意:")
    print("  - 此测试会尝试在设备屏幕上绘制矩形和文字")
    print("  - 请确保设备已连接并处于可绘制状态")
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
        # 测试1: 连接
        if not test_connection(huskylens):
            print("\n连接失败，无法继续测试")
            return 1
        test_results.append(("连接", True))
        time.sleep(1)
        
        # 测试2: 切换到人脸识别算法（必须，draw功能需要先切换算法）
        if not test_switch_algorithm(huskylens, args.algorithm):
            print("\n切换算法失败，无法继续绘制测试")
            return 1
        test_results.append(("切换算法", True))
        # 注意：test_switch_algorithm内部已等待5秒
        
        # 测试3: 绘制矩形（整数颜色值）
        if test_draw_rect(huskylens):
            test_results.append(("绘制矩形(整数颜色)", True))
        else:
            test_results.append(("绘制矩形(整数颜色)", False))
        time.sleep(1)
        
        # 测试4: 绘制矩形（RGB列表）
        if test_draw_rect_rgb(huskylens):
            test_results.append(("绘制矩形(RGB列表)", True))
        else:
            test_results.append(("绘制矩形(RGB列表)", False))
        time.sleep(1)
        
        # 测试5: 绘制唯一矩形
        if test_draw_unique_rect(huskylens):
            test_results.append(("绘制唯一矩形", True))
        else:
            test_results.append(("绘制唯一矩形", False))
        time.sleep(1)
        
        # 测试6: 绘制文字（整数颜色值）
        if test_draw_text(huskylens):
            test_results.append(("绘制文字(整数颜色)", True))
        else:
            test_results.append(("绘制文字(整数颜色)", False))
        time.sleep(1)
        
        # 测试7: 绘制文字（RGB列表）
        if test_draw_text_rgb(huskylens):
            test_results.append(("绘制文字(RGB列表)", True))
        else:
            test_results.append(("绘制文字(RGB列表)", False))
        time.sleep(1)
        
        # 测试8: 清除矩形
        if test_clear_rect(huskylens):
            test_results.append(("清除矩形", True))
        else:
            test_results.append(("清除矩形", False))
        time.sleep(1)
        
        # 测试9: 清除文字
        if test_clear_text(huskylens):
            test_results.append(("清除文字", True))
        else:
            test_results.append(("清除文字", False))
        
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

