#!/usr/bin/env python3
#coding=utf-8
import time
from Arm_Lib import Arm_Device
import numpy as np
import ikpy.chain
import ikpy.link

#初期設定
dofbot_chain = ikpy.chain.Chain(links=[
    ikpy.link.OriginLink(), # 0: 地面
    
    ikpy.link.URDFLink(
        name="id1_base_turn",   # 1: サーボID 1 (台座)
        origin_translation=np.array([0.0, 0.0, 0.0675]), 
        origin_orientation=np.array([0.0, 0.0, 0.0]), # ★追加：初期の傾き（0度）
        rotation=np.array([0.0, 0.0, 1.0]), bounds=(np.radians(-90), np.radians(90))
    ),
    ikpy.link.URDFLink(
        name="id2_shoulder",    # 2: サーボID 2 (肩)
        origin_translation=np.array([0.0, 0.0, 0.040]),  
        origin_orientation=np.array([0.0, 0.0, 0.0]), # ★追加
        rotation=np.array([0.0, 1.0, 0.0]), bounds=(np.radians(-90), np.radians(90))
    ),
    ikpy.link.URDFLink(
        name="id3_elbow",       # 3: サーボID 3 (肘)
        origin_translation=np.array([0.0, 0.0, 0.08285]), 
        origin_orientation=np.array([0.0, 0.0, 0.0]), # ★追加
        rotation=np.array([0.0, 1.0, 0.0]), bounds=(np.radians(-80), np.radians(80))
    ),
    ikpy.link.URDFLink(
        name="id4_wrist_pitch", # 4: サーボID 4 (手首上下)
        origin_translation=np.array([0.0, 0.0, 0.08285]), 
        origin_orientation=np.array([0.0, 0.0, 0.0]), # ★追加
        rotation=np.array([0.0, 1.0, 0.0]), bounds=(np.radians(-75), np.radians(75))
    ),
    ikpy.link.URDFLink(
        name="id5_wrist_roll",  # 5: サーボID 5 (手首ひねり)
        origin_translation=np.array([0.0, 0.0, 0.07905]), 
        origin_orientation=np.array([0.0, 0.0, 0.0]), # ★追加
        rotation=np.array([0.0, 0.0, 1.0]), bounds=(np.radians(-90), np.radians(90))
    ),
    ikpy.link.URDFLink(
        name="gripper_tip",     # 6: ハサミの先端（ダミー）
        origin_translation=np.array([0.0, 0.0, 0.1203]),  
        origin_orientation=np.array([0.0, 0.0, 0.0]), # ★追加
        rotation=np.array([0.0, 0.0, 0.0]), bounds=(0, 0)
    )
], active_links_mask=[False, True, True, True, True, True, False])



def main():
    #オブジェクト作成
    Arm = Arm_Device()
    time.sleep(.1)

        # =====================================================================
    # 2. 動かしたい「目標の場所（座標）」を決める
    # =====================================================================
    # 例：ロボットの正面「まっすぐ前方に15cm、高さ25cm」の位置へ移動させたい場合
    target_x = -0.05  # 前後 (15cm)
    target_y = 0.00  # 左右 (真っ直ぐ正面なので 0)
    target_z = 0.40255  # 高さ (25cm)
    target_position = np.array([target_x, target_y, target_z])
    
    # 手先の向き：ハサミを「真下」に向ける（ピッチ90度）
    pitch = np.radians(90)
    target_orientation = np.array([
        [np.cos(pitch),  0.0, np.sin(pitch)],
        [0.0,            1.0, 0.0          ],
        [-np.sin(pitch), 0.0, np.cos(pitch)]
    ])
    
    # 4x4の目標行列（ターゲットフレーム）を作成
    target_frame = np.eye(4)
    target_frame[:3, :3] = target_orientation
    target_frame[:3, 3] = target_position
    
    # =====================================================================
    # 3. 逆運動学の計算をスタート
    # =====================================================================
    # 初期姿勢（垂直ポーズ）から計算を開始する
    initial_angles = [0.0] * len(dofbot_chain.links)
    
    # IKの実行（目標ポーズに届く各関節の角度をラジアンで一瞬で計算）
    computed_angles = dofbot_chain.inverse_kinematics_frame(target_frame, initial_position=initial_angles)
    
    # =====================================================================
    # 4. 計算結果を実機用の角度に直して表示
    # =====================================================================
    print("=========================================")
    print("          Dofbot IK 計算完了             ")
    print("=========================================")
    print(f"目標座標 ➔ X: {target_x*100:.1f}cm, Y: {target_y*100:.1f}cm, Z: {target_z*100:.1f}cm\n")
    
    servo_ids = [1, 2, 3, 4, 5]
    target_angles = {} # 実機命令用の角度を保存する辞書
    
    # index 1〜5（可動する5つのサーボ）の結果を取り出す
    for i, angle_rad in enumerate(computed_angles[1:6]):
        angle_deg = np.degrees(angle_rad)
        
        # 90度を足して、実機サーボ用の命令角度（0度〜180度）に変換
        dofbot_servo_angle = 90.0 + angle_deg
        
        # 小数点第1位までに丸めて保存・表示
        target_angles[servo_ids[i]] = round(dofbot_servo_angle, 1)
        print(f"サーボ ID {servo_ids[i]} ➔  {target_angles[servo_ids[i]]:.1f} °")
    
    print("=========================================")
    
    Arm.Arm_serial_servo_write6(target_angles[1], target_angles[2], target_angles[3], target_angles[4], target_angles[5], 90, 5000)
    time.sleep(2)

    # for id in range(6):
    #     arm_position=Arm.Arm_serial_servo_read_any(id+1)
    #     print(f'{id+1} arm position {arm_position}')

if __name__=="__main__":
    main()