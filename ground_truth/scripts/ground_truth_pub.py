#!/usr/bin/python3
# import pandas as pd
import csv
import rospy
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped, PointStamped
from ground_truth.msg import ground_truth



class GroundTruth():
    def __init__(self, file_name='./ground_truth/scripts/data.csv', node_name='qrcGroundTruth'):
        rospy.init_node(node_name, anonymous=True)
        
        self.file_name = file_name
        # 真实值的发布者
        self.ground_truth_pub = rospy.Publisher("/ground_truth", ground_truth, queue_size=10)
        # 轨迹的发布者
        self.trajectory_pub = rospy.Publisher("/ground_truth_trajectory", Path, queue_size=10)
        # 坐标点的发布者
        self.point_pub = rospy.Publisher("/ground_truth_point", PointStamped, queue_size=10)
        
        # 创建轨迹消息
        self.path_msg = Path()
        self.path_msg.header.frame_id = 'odom'

        self.point_msg = PointStamped()
        self.point_msg.header.frame_id = 'odom'
       
       
        self.rate = rospy.Rate(20) # 20Hz
        
        # 在此处运行主函数
        self.main(file_name=self.file_name)


    # def rviz_pub(self):
    #     # 发布riviz
    #     pass

    
    def main(self, file_name):
        with open(file_name, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader) # 跳过表头
            for i, row in enumerate(reader):
                if rospy.is_shutdown():
                    rospy.loginfo("The process is interrupted!!!")
                    break
                # if i < 1:
                #     continue
                current_time = rospy.Time.now()
                truth_msg = ground_truth()
                # 注意这里需要转化为float格式数据集
                # -------------- 读取所有数据 -----------------
                truth_msg.timestamp = float(row[0])
                truth_msg.p_RS_R_x = float(row[1])
                truth_msg.p_RS_R_y = float(row[2])
                truth_msg.p_RS_R_z = float(row[3])
                truth_msg.q_RS_R_w = float(row[4])
                truth_msg.q_RS_R_x = float(row[5])
                truth_msg.q_RS_R_y = float(row[6])
                truth_msg.q_RS_R_z = float(row[7])
                truth_msg.v_RS_R_x = float(row[8])
                truth_msg.v_RS_R_y = float(row[9])
                truth_msg.v_RS_R_z = float(row[10])
                truth_msg.b_w_RS_S_x = float(row[11])
                truth_msg.b_w_RS_S_y = float(row[12])
                truth_msg.b_w_RS_S_z = float(row[13])
                truth_msg.b_a_RS_S_x = float(row[14])
                truth_msg.b_a_RS_S_y = float(row[15])
                truth_msg.b_a_RS_S_z = float(row[16])

                # ----------------[rviz数据]:显示轨迹-----------------
                self.path_msg.header.stamp = current_time
                pose_data = PoseStamped()
                pose_data.pose.position.x = float(row[1])
                pose_data.pose.position.y = float(row[2])
                pose_data.pose.position.z = float(row[3])

                pose_data.pose.orientation.w = float(row[4])
                pose_data.pose.orientation.x = float(row[5])
                pose_data.pose.orientation.y = float(row[6])
                pose_data.pose.orientation.z = float(row[7])
                pose_data.header.stamp = current_time
                pose_data.header.frame_id = 'odom'
                self.path_msg.poses.append(pose_data)

                # ----------------[rviz数据]:显示点的位置--------------
                self.point_msg.header.stamp = current_time
                self.point_msg.point.x = float(row[1])
                self.point_msg.point.y = float(row[2])
                self.point_msg.point.z = float(row[3])

                self.point_pub.publish(self.point_msg)

                self.trajectory_pub.publish(self.path_msg)

                self.ground_truth_pub.publish(truth_msg)
                self.rate.sleep()

if __name__ == "__main__":
    # 使用文件的绝对路径
    truth = GroundTruth(r'/home/amov/locate_ws/src/ground_truth/scripts/data.csv')


        



