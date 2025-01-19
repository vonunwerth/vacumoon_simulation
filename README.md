### Installation
```sudo apt install ros-humble-ros2-control ros-humble-ros2-controllers ros-humble-gazebo-ros2-control```

Create a new workspace, copy the package to the new workspace and run the launch file after building the workspace


### Usage
Launch the simulation using ```ros2 launch vacumoon_simulation launch_sim.launch.py ```

![readme_files/robot.png](readme_files/robot.png)

##### Move the robot

```
ros2 topic pub /position_forward_controller/commands std_msgs/msg/Float64MultiArray "{
  layout: {
    dim: [],
    data_offset: 0
  },
  data: [1.0, 3.0, 3.14]
}"

```
The first entry of the data field contains where to go in x-direction, the second where to go in y-direction and the third describes the orientation of the robot around the z-axis.


##### Move the arm

```
ros2 topic pub --once /joint_trajectory_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory "{
  header: {
    stamp: {sec: 0, nanosec: 0},
    frame_id: ''
  },
  joint_names: ['arm_joint'],
  points: [
    {
      positions: [0.2],
      velocities: [0.0],
      accelerations: [0.0],
      time_from_start: {sec: 1, nanosec: 0}
    }
  ]
}"

```