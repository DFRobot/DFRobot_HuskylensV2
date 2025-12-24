"""
二哈识图V2 MQTT协议人脸识别演示程序
持续获取并打印所有人脸信息，按Ctrl+C退出
"""

import sys
import time
import signal
from dfrobot_huskylensv2_mqtt import (
    DFRobot_HuskylensV2,
    ALGORITHM_FACE_RECOGNITION
)

# 从主库导入默认配置
from dfrobot_huskylensv2_mqtt import (
    BROKER, PORT, TOPIC_CMD, TOPIC_RESP, 
    USERNAME, PASSWORD, TIMEOUT
)

# 全局变量，用于优雅退出
running = True


def signal_handler(sig, frame):
    """处理Ctrl+C信号"""
    global running
    print("\n\n收到退出信号，正在退出...")
    running = False


def print_separator():
    """打印分隔线"""
    print("=" * 60)


def print_face_info(face, index):
    """打印人脸信息"""
    print(f"\n人脸 #{index + 1}:")
    print("-" * 60)
    # 排除 'used' 字段，不显示在输出中
    display_face = {k: v for k, v in face.items() if k != 'used'}
    sorted_keys = sorted(display_face.keys())
    for key in sorted_keys:
        value = display_face[key]
        if isinstance(value, list):
            print(f"  {key:20s}: {value}")
        else:
            print(f"  {key:20s}: {value}")
    print("-" * 60)


def main():
    """主函数"""
    global running
    
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    
    print("=" * 60)
    print("二哈识图V2 MQTT协议人脸识别演示程序")
    print("=" * 60)
    print()
    print("配置信息:")
    print(f"  MQTT Broker: {BROKER}:{PORT}")
    print(f"  命令主题: {TOPIC_CMD}")
    print(f"  响应主题: {TOPIC_RESP}")
    if USERNAME:
        print(f"  用户名: {USERNAME}")
    print(f"  算法: 人脸识别 (ID: {ALGORITHM_FACE_RECOGNITION})")
    print()
    print("提示:")
    print("  - 程序将持续获取人脸信息并打印")
    print("  - 每2秒更新一次")
    print("  - 按 Ctrl+C 退出程序")
    print()
    
    # 创建Huskylens实例
    huskylens = DFRobot_HuskylensV2(
        broker_host=BROKER,
        broker_port=PORT,
        command_topic=TOPIC_CMD,
        response_topic=TOPIC_RESP,
        username=USERNAME,
        password=PASSWORD,
        timeout=TIMEOUT
    )
    
    try:
        # 连接MQTT broker
        print_separator()
        print("正在连接到MQTT broker...")
        if not huskylens.connect():
            print("✗ 连接失败，无法继续")
            return 1
        print("✓ 连接成功")
        time.sleep(1)
        
        # 切换到人脸识别算法
        print_separator()
        print(f"正在切换到人脸识别算法 (ID: {ALGORITHM_FACE_RECOGNITION})...")
        if not huskylens.switchAlgorithm(ALGORITHM_FACE_RECOGNITION):
            print("✗ 切换算法失败，无法继续")
            return 1
        print("✓ 切换成功")
        print("  等待5秒，确保切换完成...")
        time.sleep(5)
        print("  准备就绪")
        print()
        
        # 主循环：持续获取人脸信息
        iteration = 0
        while running:
            iteration += 1
            print_separator()
            print(f"第 {iteration} 次获取人脸信息")
            print_separator()
            
            # 获取识别结果
            count = huskylens.getResult(ALGORITHM_FACE_RECOGNITION)
            
            if count is not None and count > 0:
                print(f"✓ 检测到 {count} 个人脸")
                print()
                
                # 打印所有人脸信息
                for index in range(count):
                    face = huskylens.getCachedResultByIndex(ALGORITHM_FACE_RECOGNITION, index)
                    if face:
                        print_face_info(face, index)
            elif count == 0:
                print("✗ 未检测到人脸")
            else:
                print("✗ 获取结果失败")
            
            # 等待2秒后继续下一次获取
            if running:
                print()
                print("等待2秒后继续...")
                print()
                time.sleep(2)
        
        print_separator()
        print("程序退出")
        print_separator()
        return 0
        
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
        return 1
    except Exception as e:
        print(f"\n\n程序运行出错: {e}")
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

