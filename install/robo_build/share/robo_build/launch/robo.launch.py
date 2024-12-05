import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # 获取默认的 URDF 文件路径
    urdf_tutorial_path = get_package_share_directory('robo_build')  # 获取整个包的路径
    default_model_path = urdf_tutorial_path + '/urdf/robo.urdf'  # 拼接出默认的 URDF 文件路径
    default_rviz_config_path = urdf_tutorial_path + '/config/rviz/display_model.rviz' #拼接得出rviz的路径
    # 为 launch 声明参数
    action_declare_arg_mode_path = launch.actions.DeclareLaunchArgument(
        name='model', 
        default_value=str(default_model_path),  # 设置默认值为默认的 URDF 文件路径
        description='URDF 的绝对路径'
    )

    # 通过命令读取 URDF 文件的内容，生成参数
    robot_description = launch_ros.parameter_descriptions.ParameterValue(
        launch.substitutions.Command(
            #['cat ', launch.substitutions.LaunchConfiguration('model')]),  # 使用 cat 命令读取文件内容
            ['xacro ', launch.substitutions.LaunchConfiguration('model')]),  # 使用 xacro 命令读取文件内容
        value_type=str  # 设置参数的值类型为字符串
    )

    # 状态发布节点：发布机器人状态信息
    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',  # 使用的 ROS 包
        executable='robot_state_publisher',  # 执行的节点程序
        parameters=[{'robot_description': robot_description}]  # 将 robot_description 作为参数传入
    )

    # 关节状态发布节点：发布机器人的关节状态
    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',  # 使用的 ROS 包
        executable='joint_state_publisher',  # 执行的节点程序
    )

    # RViz 节点：启动 RViz 可视化界面
    rviz_node = launch_ros.actions.Node(
        package='rviz2',  # 使用的 ROS 包
        executable='rviz2',  # 执行的节点程序
        arguments=['-d', default_rviz_config_path] #设置路径
    )

    # 返回 LaunchDescription，包含所有节点和参数
    return launch.LaunchDescription([
        action_declare_arg_mode_path,  # 声明的参数
        joint_state_publisher_node,    # 启动的关节状态发布节点
        robot_state_publisher_node,    # 启动的机器人状态发布节点
        rviz_node                      # 启动的 RViz 可视化界面节点
    ])
