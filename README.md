<img align="right" width="20%" height="20%" src="./asset/allegrohand_v4.png">

> [!WARNING]
> # 📦 Repository Status: Archived
> # This repository is no longer maintained. Please refer to the latest ROS 2 controller implementation at [Wonikrobotics-git/allegro_hand_ros2](https://github.com/Wonikrobotics-git/allegro_hand_ros2)

# allegro_hand_linux_v4
> Official Code Repository for controlling the Allegro Hand V4 on Linux System

This repository is the official release for controlling the **Allegro Hand V4**.

There are [ROS1 API](./ros_source/), [ROS2 API](./ros2_source) and [C++ API](./cpp/) for [Allegro Hand V4](https://www.allegrohand.com/ah-v4-main)

# Setup

This section provides instructions on setting up your PC and installing the PCAN driver to connect the **Allegro Hand V4** to your system.

> [!IMPORTANT]
> Make sure to choose the correct version for your setup. The **Setup Manual** and **Source Code** differ depending on the project you are working on.

<!--
|  | **C++ API** | **ROS1 API** | **ROS2 API** |
|---|------------|-------------|-------------|
| **System** | Ubuntu 20.04 | Ubuntu 20.04 | Ubuntu 22.04 |
| **Source** | [cpp/](./cpp/) | [ros_source/](./ros_source/) | [ros2_source/](./ros2_source/) |
| **Setup Manual** | 🔵 Type 1 | 🔵 Type 1 | 🟣 Type 2 |
-->

|  | **C++ API** | **ROS1 API** | **ROS2 API** |
|---|------------|-------------|-------------|
| **System** | Ubuntu 20.04/22.04 | Ubuntu 20.04 | Ubuntu 22.04 |
| **Source** | [cpp/grasp_2004/](./cpp/grasp_2004/)/[cpp/grasp_2204/](./cpp/grasp_2004/) | [ros_source/](./ros_source/) | [ros2_source/](./ros2_source/) |
| **Setup Manual** | 🔵 Type 1/🟣 Type 2 | 🔵 Type 1 | 🟣 Type 2 |

<details>
<summary><b>🔵 Type 1</b></summary>

## Project Setup of Type 1

### 1. Install Ubuntu 20.04

- **Download & Create Bootable USB**
   - Get the [Ubuntu 20.04 LTS ISO](https://releases.ubuntu.com/focal/).
   - Use [Rufus](https://rufus.ie/) (Windows) or [Etcher](https://www.balena.io/etcher/) (macOS/Linux) to create a bootable USB.
- **Install Ubuntu**
   - Boot from the USB and follow the installation steps (language, keyboard, disk setup, user info).
   - Reboot after installation.


### 2. `libBHand` Installation

- Check your system architecture:
  ```bash
  getconf LONG_BIT
  ```
  This will determine whether you need the 32-bit or 64-bit version.

- Navigate to the `libBHand/libBHand_{32|64}` directory and install `libBHand`:
  ```bash
  cd libBHand/libBHand_{32|64}
  sudo make install
  sudo ldconfig
  ```

- If you need to **uninstall** `libBHand`, navigate to the `libBHand_{32|64}` directory and run:
  ```bash
  sudo make uninstall
  sudo ldconfig
  ```

- The library source can also be downloaded from the [Grasping Library for Linux](https://www.allegrohand.com/ah-v4-grasping-library-for-linux).
  - Click the button to download.
  - Locate `LibBHand_32.zip` or `LibBHand_64.zip` (found in the `/Allegro Hand V4 | File` folder).
  - Unzip the source file and install it according to the instructions above.

### 3. Install the PCAN Driver

> Before using the hand, you must install the **PCAN drivers**. These instructions assume you are using a **Peak Systems PCAN-USB adapter**.

- **Install dependencies:**
  ```bash
  sudo apt-get install libpopt-dev ros-noetic-libpcan
  ```

- **Download the latest drivers:**
  [Peak-System Linux Driver](http://www.peak-system.com/fileadmin/media/linux/index.htm#download)

- **Install the drivers:**
  ```bash
  make clean; make NET=NO_NETDEV_SUPPORT
  sudo make install
  sudo /sbin/modprobe pcan
  ```

- **Verify installation:**
  Run the following command to check if the interface is installed correctly. You should see streaming output.
  ```bash
  cat /proc/pcan
  ```

- **Check for available interfaces:**
  When the hand is connected, you should see `pcanusb0` or `pcanusbN` (`N` can be any number).
  ```bash
  ls -l /dev/pcan*
  ```

  - If no files are listed, try running the following command from the **downloaded PCAN driver folder**. It manually creates the device files if the system has not done so automatically.
    ```bash
    sudo ./driver/pcan_make_devices 2
    ```

- **(Optional) CAN Communication Tutorial**
  - If you are not familiar with PCAN, refer to the [CAN Communication Tutorial](https://www.allegrohand.com/ah-v4-can-communication).

</details>

<details>
<summary><b>🟣 Type 2</b></summary>

## Project Setup of Type 2

### 1. Install Ubuntu 22.04

- **Download & Create Bootable USB**
   - Get the [Ubuntu 22.04 LTS ISO](https://releases.ubuntu.com/jammy/).
   - Use [Rufus](https://rufus.ie/) (Windows) or [Etcher](https://www.balena.io/etcher/) (macOS/Linux) to create a bootable USB.
- **Install Ubuntu**
   - Boot from the USB and follow the installation steps (language, keyboard, disk setup, user info).
   - Reboot after installation.

### 2. `libBHand` Installation

- `BHandLib` is located in `/src/bhand/lib/libBHand.so`.
- By default, the library is compiled for **64-bit** systems. If your system is **32-bit**, replace the `/lib` folder with the appropriate version.

- Library Structure:
  ```bash
  src/
  └── bhand/
      ├── include/bhand/
      ├── lib/
      │   └── libBHand.so  # Default (64-bit) used when building the source
      ├── libBHand_32/lib/
      │   └── libBHand.so  # Replace with this if using a 32-bit system
      └── libBHand_64/lib/
          └── libBHand.so  # Replace with this if using a 64-bit system
  ```

### 3. ROS 2 and PCAN Support

- ROS 2 no longer supports **PCAN**. Instead, use `can-utils` for **SocketCAN**:
  ```bash
  sudo apt install can-utils
  ```

- **CAN Setup:**
  Before launching, ensure your CAN device is configured and active. The system is configured to use can0 at a bitrate of 1000000.

   ```bash
   sudo ip link set can0 down
   sudo ip link set can0 type can bitrate 1000000
   sudo ip link set can0 up
   ```
   > NOTE
   > If you are using dual hands, you must also activate can1. This example maps the CAN devices as follows:
   > - can0 : right hand
   > - can1 : left hand

</details>


# File Structure

This repository is structured into three main sections:
- `cpp/`: Contains the standalone C++ API for the Allegro Hand V4.
- `ros_source/`: Includes the ROS1 package for controlling the Allegro Hand.
- `ros2_source/`: Includes the ROS2 package for controlling the Allegro Hand.

Each section has its own **README.md** with setup and build instructions.

```
.
├── libBHand
│   ├── libBHand_64
│   └── libBHand_32
├── cpp
│   ├── 📃 README.md   # Instructions for building the C++ library
│   └── grasp
├── ros_source
│   ├── 📃 README.md   # Instructions for building the ROS1 package
│   └── src
│       ├── allegro_hand_controllers
│       │   ├── launch
│       │   │   ├── allegro_hand.launch
│       │   │   └── allegro_viz.launch
│       │   ├── package.xml
│       │   ├── CMakeLists.txt
│       │   └── src
│       ├── allegro_hand_description
│       ├── allegro_hand_driver
│       ├── allegro_hand_keyboard
│       ├── allegro_hand_parameters
│       ├── allegro_hand_python
│       └── bhand
├── ros2_source
│   ├── 📃 README.md   # Instructions for building the ROS2 package
│   └── src
│       ├── allegro_hand_controllers
│       ... (Similar to the `ros_source` structure)
│       └── bhand
└── 📃 README.md       # Instructions for setting up the Allegro Hand V4
```

# C++ API

Step-by-step instructions are provided for running the motion demo of the **Allegro Hand V4** using the **C++ API** on **Ubuntu 20.04/22.04** (independent of ROS).
For more details, see 📃 [cpp/README.md](./cpp/README.md).

# ROS1 API

The **ROS1 API** allows you to control the **Allegro Hand V4** using **ROS1 Noetic** on **Ubuntu 20.04**.
For more details, see 📃 [ros_source/README.md](./ros_source/README.md).

# ROS2 API

The **ROS2 API** enables control of the **Allegro Hand V4** using **ROS2 Humble** on **Ubuntu 22.04**.
For more details, see 📃 [ros2_source/README.md](./ros2_source/README.md).


# User Manual

- For more information about Allegro Hand V4, see [User Manual 1.1](./asset/Allegro%20Hand%20V4_Users%20Manual_1.1.pdf).
- Note: The wiki page at wiki.wonikrobotics.com/AllegroHandWiki is **no longer available!**
- In the "Using Allegro Hand Sample Program" section, the source code has been replaced with the following GitHub repositories:
  - **Linux System:** [allegro_hand_linux_v4](https://github.com/Wonikrobotics-git/allegro_hand_linux_v4)
  - **Windows System:** [allegro_hand_windows_v4](https://github.com/Wonikrobotics-git/allegro_hand_windows_v4)


# Discussion & Issues

If you encounter any issues or would like to discuss improvements, you can use the following channels:

- [**GitHub Issues**](https://github.com/Wonikrobotics-git/allegro_hand_linux_v4/issues)
- [**Allegro Hand Forum**](https://allegrohand.com/forum)


# Contribution

We welcome contributions! 🚀
If you'd like to contribute, feel free to submit a **pull request** with a **clear and concise explanation** of its purpose.

### **Special Thanks to Contributors**

We sincerely appreciate the contributions that have helped improve this repository:

- **Interfaces and controllers** by [@felixduvallet](https://github.com/felixduvallet)
- **New torque controller** by [@nisommer](https://github.com/nisommer)

Thank you for your valuable contributions! 🙌

