"""
二哈识图V2 MQTT协议使用示例
真实MQTT通信示例代码
"""

import time
from dfrobot_huskylensv2_mqtt import (
    DFRobot_HuskylensV2,
    ALGORITHM_FACE_RECOGNITION,
    ALGORITHM_OBJECT_RECOGNITION
)

# 从主库导入默认配置
from dfrobot_huskylensv2_mqtt import (
    BROKER, PORT, TOPIC_CMD, TOPIC_RESP, 
    USERNAME, PASSWORD, TIMEOUT
)
USE_CONFIG_FILE = True


def main():
    """主函数"""
    # 创建Huskylens实例
    # 优先使用配置文件中的参数，也可以手动指定参数覆盖
    if USE_CONFIG_FILE:
        print("✓ 使用默认配置")
        print(f"  使用配置: {BROKER}:{PORT}, 主题: {TOPIC_CMD}/{TOPIC_RESP}")
        print()
    
    huskylens = DFRobot_HuskylensV2(
        broker_host=BROKER,             # MQTT broker地址
        broker_port=PORT,               # MQTT broker端口
        command_topic=TOPIC_CMD,        # 命令主题
        response_topic=TOPIC_RESP,      # 响应主题
        username=USERNAME,              # MQTT用户名（如果配置了）
        password=PASSWORD,              # MQTT密码（如果配置了）
        timeout=TIMEOUT                 # 命令超时时间（秒）
    )
    
    try:
        # 连接MQTT broker
        print("正在连接MQTT broker...")
        if not huskylens.connect():
            print("连接失败！")
            return
        
        print("连接成功！")
        
        # 获取算法列表
        print("\n获取算法列表...")
        algorithms = huskylens.getAlgorithmList()
        if algorithms:
            print(f"找到 {len(algorithms)} 个算法:")
            for algo in algorithms:
                print(f"  ID: {algo.get('id')} - {algo.get('name_cn')} ({algo.get('name_en')})")
        else:
            print("获取算法列表失败")
            return
        
        # 切换算法
        print("\n切换到人脸识别算法...")
        if huskylens.switchAlgorithm(ALGORITHM_FACE_RECOGNITION):
            print("切换成功！")
            print("(等待5秒，确保切换完成)")
            time.sleep(5)
        else:
            print("切换失败！")
            return
        
        # 获取识别结果（返回数量，结果被缓存）
        print("\n获取识别结果...")
        count = huskylens.getResult(ALGORITHM_FACE_RECOGNITION)
        if count is not None:
            print(f"检测到 {count} 个结果（结果已缓存）")
        
        # 检查结果是否可用
        if huskylens.available(ALGORITHM_FACE_RECOGNITION):
            print("结果可用！")
            
            # 获取最接近中心的结果
            center_result = huskylens.getCachedCenterResult(ALGORITHM_FACE_RECOGNITION)
            if center_result:
                # 排除 'used' 字段
                display_result = {k: v for k, v in center_result.items() if k != 'used'}
                print(f"中心结果: {display_result}")
            
            # 使用 popCachedResult 遍历所有结果
            print("\n遍历所有结果:")
            result_index = 0
            while huskylens.available(ALGORITHM_FACE_RECOGNITION):
                result = huskylens.popCachedResult(ALGORITHM_FACE_RECOGNITION)
                if result:
                    result_index += 1
                    print(f"  结果 #{result_index}: ID={result.get('id')}, Name={result.get('name')}")
        else:
            print("未检测到结果")
        
        # 使用上下文管理器的方式（推荐）
        print("\n使用上下文管理器方式...")
        with DFRobot_HuskylensV2(
            broker_host=BROKER,
            broker_port=PORT,
            command_topic=TOPIC_CMD,
            response_topic=TOPIC_RESP,
            username=USERNAME,
            password=PASSWORD,
            timeout=TIMEOUT
        ) as huskylens2:
            algorithms = huskylens2.getAlgorithmList()
            if algorithms:
                print(f"算法数量: {len(algorithms)}")
        
    except Exception as e:
        print(f"发生错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 断开连接
        print("\n断开连接...")
        huskylens.disconnect()
        print("已断开连接")


if __name__ == '__main__':
    main()

