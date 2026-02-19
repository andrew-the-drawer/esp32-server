# Deployment Architecture Diagram
![Please refer to - Full Module Deployment Architecture Diagram](../docs/images/deploy2.png)

# Method 1: Run All Modules with Docker
Starting from version `0.8.2`, the Docker images released by this project only support the `x86 architecture`. If you need to deploy on a CPU with `arm64 architecture`, follow [this tutorial](docker-build.md) to build an `arm64 image` locally.

## 1. Install Docker

If Docker is not installed on your computer yet, you can follow this guide: [Docker Installation](https://www.runoob.com/docker/ubuntu-docker-install.html)

There are two ways to install the full module stack with Docker. You can use the [quick script](#11-quick-script) (by [@VanillaNahida](https://github.com/VanillaNahida)), or use [manual deployment](#12-manual-deployment) to set it up from scratch.

The script automatically downloads the required files and configuration files.

### 1.1 Quick Script
Deployment is simple. You can refer to this [video tutorial](https://www.bilibili.com/video/BV17bbvzHExd/). The text tutorial is below:

> [!NOTE]
> Currently, one-click deployment is only supported on Ubuntu servers. Other systems have not been fully tested and may have unexpected bugs.

Use an SSH tool to connect to your server, then run the following script with root privileges:

```bash
sudo bash -c "$(wget -qO- https://ghfast.top/https://raw.githubusercontent.com/xinnan-tech/xiaozhi-esp32-server/main/docker-setup.sh)"
```

The script will automatically perform the following operations:
> 1. Install Docker
> 2. Configure image mirrors
> 3. Download/pull images
> 4. Download speech recognition model files
> 5. Guide server-side configuration

After it completes, do some basic configuration, then follow the 3 most important actions mentioned in [4. Run the Program](#4-run-the-program) and [5. Restart xiaozhi-esp32-server](#5restart-xiaozhi-esp32-server). After finishing those 3 configuration items, you can use the system.

### 1.2 Manual Deployment

#### 1.2.1 Create Directories

After installation, choose a directory to store this project’s configuration files. For example, create a folder named `xiaozhi-server`.

After creating it, you need to create `data` and `models` under `xiaozhi-server`, and then create `SenseVoiceSmall` under `models`.

The final directory structure should be:

```
xiaozhi-server
  ├─ data
  ├─ models
     ├─ SenseVoiceSmall
```

#### 1.2.2 Download Speech Recognition Model File

This project uses `SenseVoiceSmall` by default for speech-to-text. Because the model is large, it must be downloaded separately. After downloading, place the `model.pt` file in `models/SenseVoiceSmall`.
Choose either of the two download routes below.

- Route 1: ModelScope download [SenseVoiceSmall](https://modelscope.cn/models/iic/SenseVoiceSmall/resolve/master/model.pt)
- Route 2: Baidu Netdisk download [SenseVoiceSmall](https://pan.baidu.com/share/init?surl=QlgM58FHhYv1tFnUT_A8Sg&pwd=qvna), extraction code: `qvna`

#### 1.2.3 Download Configuration Files

You need to download two configuration files: `docker-compose_all.yaml` and `config_from_api.yaml` from the project repository.

##### 1.2.3.1 Download docker-compose_all.yaml

Open [this link](../main/xiaozhi-server/docker-compose_all.yml) in your browser.

On the right side of the page, find the `RAW` button. Next to `RAW`, find the download icon and click it to download `docker-compose_all.yml`. Save it into your `xiaozhi-server` directory.

Or download directly by running:

`wget https://raw.githubusercontent.com/xinnan-tech/xiaozhi-esp32-server/refs/heads/main/main/xiaozhi-server/docker-compose_all.yml`

After downloading, continue.

##### 1.2.3.2 Download config_from_api.yaml

Open [this link](../main/xiaozhi-server/config_from_api.yaml) in your browser.

On the right side of the page, find the `RAW` button. Next to `RAW`, find the download icon and click it to download `config_from_api.yaml`. Save it into `xiaozhi-server/data`, then rename `config_from_api.yaml` to `.config.yaml`.

Or download directly by running:

`wget https://raw.githubusercontent.com/xinnan-tech/xiaozhi-esp32-server/refs/heads/main/main/xiaozhi-server/config_from_api.yaml`

After downloading configuration files, confirm the full `xiaozhi-server` structure is:

```
xiaozhi-server
  ├─ docker-compose_all.yml
  ├─ data
    ├─ .config.yaml
  ├─ models
     ├─ SenseVoiceSmall
       ├─ model.pt
```

If your structure matches, continue. If not, check carefully for missed steps.

## 2. Back Up Data

If you have previously run the Admin Console successfully and it contains your key information, please copy important data out from the Admin Console first. During upgrade, original data may be overwritten.

## 3. Remove Old Images and Containers
Next, open your terminal/command line tool, enter your `xiaozhi-server` directory, and run:

```
docker compose -f docker-compose_all.yml down

docker stop xiaozhi-esp32-server
docker rm xiaozhi-esp32-server

docker stop xiaozhi-esp32-server-web
docker rm xiaozhi-esp32-server-web

docker stop xiaozhi-esp32-server-db
docker rm xiaozhi-esp32-server-db

docker stop xiaozhi-esp32-server-redis
docker rm xiaozhi-esp32-server-redis

docker rmi ghcr.nju.edu.cn/xinnan-tech/xiaozhi-esp32-server:server_latest
docker rmi ghcr.nju.edu.cn/xinnan-tech/xiaozhi-esp32-server:web_latest
```

## 4. Run the Program
Run the following command to start the new version containers:

```
docker compose -f docker-compose_all.yml up -d
```

After that, run this command to view logs:

```
docker logs -f xiaozhi-esp32-server-web
```

When you see output logs, your `Admin Console` has started successfully.

```
2025-xx-xx 22:11:12.445 [main] INFO  c.a.d.s.b.a.DruidDataSourceAutoConfigure - Init DruidDataSource
2025-xx-xx 21:28:53.873 [main] INFO  xiaozhi.AdminApplication - Started AdminApplication in 16.057 seconds (process running for 17.941)
http://localhost:8002/xiaozhi/doc.html
```

Please note: at this point, only the `Admin Console` is confirmed running. If port 8000 (`xiaozhi-esp32-server`) reports errors, ignore it for now.

Now use your browser to open the `Admin Console` at: `http://127.0.0.1:8002` and register the first user.
The first user is the super admin; all later users are normal users.
Normal users can only bind devices and configure agents; super admins can manage models, users, parameters, and more.

Next, there are three important things to do:

### First Important Thing

Use the super admin account to log in to the Admin Console. In the top menu, find `Parameter Management`, then find the first item in the list with parameter code `server.secret`, and copy its `Parameter Value`.

A note about `server.secret`: this value is very important. It allows the `Server` side to connect to `manager-api`.
`server.secret` is randomly generated each time the manager module is deployed from scratch.

After copying the value, open `.config.yaml` in `xiaozhi-server/data`. At this point your config should look like this:

```
manager-api:
  url:  http://127.0.0.1:8002/xiaozhi
  secret: your server.secret value
```

1. Copy the `server.secret` value from the Admin Console into `secret` in `.config.yaml`.

2. Because you are using Docker deployment, change `url` to `http://xiaozhi-esp32-server-web:8002/xiaozhi`.

3. Because you are using Docker deployment, change `url` to `http://xiaozhi-esp32-server-web:8002/xiaozhi`.

4. Because you are using Docker deployment, change `url` to `http://xiaozhi-esp32-server-web:8002/xiaozhi`.

The result should look like this:

```
manager-api:
  url: http://xiaozhi-esp32-server-web:8002/xiaozhi
  secret: 12345678-xxxx-xxxx-xxxx-123456789000
```

After saving, continue to the second important thing.

### Second Important Thing

Use the super admin account to log in to the Admin Console. In the top menu, go to `Model Configuration`, then click `Large Language Model` on the left sidebar. Find the first item `Zhipu AI`, click `Edit`, and in the pop-up, enter your registered `Zhipu AI` key into `API Key`, then click Save.

## 5.Restart xiaozhi-esp32-server

Now open your terminal/command line tool and run:

```
docker restart xiaozhi-esp32-server
docker logs -f xiaozhi-esp32-server
```

If you see logs similar to the following, it means the Server started successfully.

```
25-02-23 12:01:09[core.websocket_server] - INFO - Websocket address is      ws://xxx.xx.xx.xx:8000/xiaozhi/v1/
25-02-23 12:01:09[core.websocket_server] - INFO - =======The above address uses websocket protocol, do not open it in a browser=======
25-02-23 12:01:09[core.websocket_server] - INFO - To test websocket, use Chrome to open test/test_page.html
25-02-23 12:01:09[core.websocket_server] - INFO - =======================================================
```

Because you are deploying all modules, you have two important endpoints to write into ESP32.

OTA endpoint:
```
http://your-host-lan-ip:8002/xiaozhi/ota/
```

Websocket endpoint:
```
ws://your-host-ip:8000/xiaozhi/v1/
```

### Third Important Thing

Use the super admin account to log in to the Admin Console. In the top menu, find `Parameter Management`, then find parameter code `server.websocket`, and enter your `Websocket endpoint`.

Use the super admin account to log in to the Admin Console. In the top menu, find `Parameter Management`, then find parameter code `server.ota`, and enter your `OTA endpoint`.

Next, you can start using your ESP32 device. You can either `build the ESP32 firmware yourself`, or use `Xiage’s prebuilt firmware version 1.6.1 or above`. Choose either one.

1. [Build your own ESP32 firmware](firmware-build.md).

2. [Configure a custom server based on Xiage’s prebuilt firmware](firmware-setting.md).

# Method 2: Run All Modules from Local Source Code

## 1.Install MySQL Database

If MySQL is already installed on your machine, you can directly create a database named `xiaozhi_esp32_server`.

```sql
CREATE DATABASE xiaozhi_esp32_server CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

If MySQL is not installed yet, you can install MySQL via Docker:

```
docker run --name xiaozhi-esp32-server-db -e MYSQL_ROOT_PASSWORD=123456 -p 3306:3306 -e MYSQL_DATABASE=xiaozhi_esp32_server -e MYSQL_INITDB_ARGS="--character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci" -e TZ=Asia/Shanghai -d mysql:latest
```

## 2.Install Redis

If Redis is not installed yet, you can install Redis via Docker:

```
docker run --name xiaozhi-esp32-server-redis -d -p 6379:6379 redis
```

## 3.Run manager-api

3.1 Install JDK21 and configure JDK environment variables.

3.2 Install Maven and configure Maven environment variables.

3.3 Use VS Code to load the `manager-api` module.

3.4 Use VS Code to load the `manager-api` module.

Configure database connection in `src/main/resources/application-dev.yml`:

```
spring:
  datasource:
    username: root
    password: 123456
```

Configure Redis connection in `src/main/resources/application-dev.yml`:

```
spring:
    data:
      redis:
        host: localhost
        port: 6379
        password:
        database: 0
```

3.5 Run the main program.

This project is a Spring Boot project. Startup method:
Open `Application.java` and run the `Main` method.

```
Path:
src/main/java/xiaozhi/AdminApplication.java
```

When you see output logs, your `manager-api` has started successfully.

```
2025-xx-xx 22:11:12.445 [main] INFO  c.a.d.s.b.a.DruidDataSourceAutoConfigure - Init DruidDataSource
2025-xx-xx 21:28:53.873 [main] INFO  xiaozhi.AdminApplication - Started AdminApplication in 16.057 seconds (process running for 17.941)
http://localhost:8002/xiaozhi/doc.html
```

## 4.Run manager-web

4.1 Install Node.js.

4.2 Use VS Code to load the `manager-web` module.

Use terminal commands to enter the `manager-web` directory:

```
npm install
```

Then start it:

```
npm run serve
```

Please note: if your `manager-api` interface is not at `http://localhost:8002`, modify the path in `main/manager-web/.env.development` during development.

After startup succeeds, use your browser to open the `Admin Console` at: `http://127.0.0.1:8001`, and register the first user.
The first user is the super admin; all later users are normal users.
Normal users can only bind devices and configure agents; super admins can manage models, users, parameters, and more.

Important: After successful registration, use the super admin account to log in to the Admin Console. In the top menu, go to `Model Configuration`, then click `Large Language Model` on the left sidebar. Find the first item `Zhipu AI`, click `Edit`, and in the pop-up, enter your registered `Zhipu AI` key into `API Key`, then click Save.

Important: After successful registration, use the super admin account to log in to the Admin Console. In the top menu, go to `Model Configuration`, then click `Large Language Model` on the left sidebar. Find the first item `Zhipu AI`, click `Edit`, and in the pop-up, enter your registered `Zhipu AI` key into `API Key`, then click Save.

Important: After successful registration, use the super admin account to log in to the Admin Console. In the top menu, go to `Model Configuration`, then click `Large Language Model` on the left sidebar. Find the first item `Zhipu AI`, click `Edit`, and in the pop-up, enter your registered `Zhipu AI` key into `API Key`, then click Save.

## 5.Install Python Environment

This project uses `conda` to manage dependencies. If installing `conda` is inconvenient, install `libopus` and `ffmpeg` for your actual OS.
If you decide to use `conda`, install it first, then run the following commands.

Important reminder for Windows users: you can use `Anaconda` to manage environments.
After installing `Anaconda`, search for `anaconda` in Start, find `Anaconda Prompt`, and run it as administrator, as shown below.

![conda_prompt](./images/conda_env_1.png)

After launch, if you see `(base)` before the command prompt, you have entered the `conda` environment successfully. Then run:

![conda_env](./images/conda_env_2.png)

```
conda remove -n xiaozhi-esp32-server --all -y
conda create -n xiaozhi-esp32-server python=3.10 -y
conda activate xiaozhi-esp32-server

# Add Tsinghua mirror channels
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge

conda install libopus -y
conda install ffmpeg -y

# On Linux, if you encounter missing libiconv.so.2 dynamic library errors, install it with:
conda install libiconv -y
```

Please note: do not run all commands blindly at once. Execute them step by step and check output logs after each step.

## 6.Install Project Dependencies

First, download this project’s source code. You can use `git clone`. If you are not familiar with `git clone`:

Open this URL in your browser: `https://github.com/xinnan-tech/xiaozhi-esp32-server.git`

Find the green `Code` button, click it, then click `Download ZIP`.

Download the source zip. After downloading to your computer, extract it. The folder may be named `xiaozhi-esp32-server-main`.
Rename it to `xiaozhi-esp32-server`. In that folder, enter `main`, then `xiaozhi-server`. Please remember this `xiaozhi-server` directory.

```
# Continue using conda environment
conda activate xiaozhi-esp32-server
# Enter your project root, then main/xiaozhi-server
cd main/xiaozhi-server
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
pip install -r requirements.txt
```

### 7.Download Speech Recognition Model File

This project uses `SenseVoiceSmall` by default for speech-to-text. Because the model is large, it must be downloaded separately. After downloading, place `model.pt` into `models/SenseVoiceSmall`.
Choose either route below.

- Route 1: ModelScope download [SenseVoiceSmall](https://modelscope.cn/models/iic/SenseVoiceSmall/resolve/master/model.pt)
- Route 2: Baidu Netdisk download [SenseVoiceSmall](https://pan.baidu.com/share/init?surl=QlgM58FHhYv1tFnUT_A8Sg&pwd=qvna), extraction code: `qvna`

## 8.Configure Project Files

Use the super admin account to log in to the Admin Console. In the top menu, find `Parameter Management`, then find the first item in the list with parameter code `server.secret`, and copy its `Parameter Value`.

A note about `server.secret`: this value is very important. It allows the `Server` side to connect to `manager-api`.
`server.secret` is randomly generated each time the manager module is deployed from scratch.

If your `xiaozhi-server` directory does not have `data`, create a `data` directory.
If `data` does not contain `.config.yaml`, you can copy `config_from_api.yaml` from the `xiaozhi-server` directory into `data` and rename it to `.config.yaml`.

After copying the value, open `.config.yaml` under `xiaozhi-server/data`. At this point your config should look like this:

```
manager-api:
  url: http://127.0.0.1:8002/xiaozhi
  secret: your server.secret value
```

Copy the `server.secret` value you copied from the Admin Console into `secret` in `.config.yaml`.

The result should look like this:

```
manager-api:
  url: http://127.0.0.1:8002/xiaozhi
  secret: 12345678-xxxx-xxxx-xxxx-123456789000
```

## 5.Run the Project

```
# Make sure you execute this in the xiaozhi-server directory
conda activate xiaozhi-esp32-server
python app.py
```

If you see logs similar to the following, it indicates the project service started successfully.

```
25-02-23 12:01:09[core.websocket_server] - INFO - Server is running at ws://xxx.xx.xx.xx:8000/xiaozhi/v1/
25-02-23 12:01:09[core.websocket_server] - INFO - =======The above address uses websocket protocol, do not open it in a browser=======
25-02-23 12:01:09[core.websocket_server] - INFO - To test websocket, use Chrome to open test/test_page.html
25-02-23 12:01:09[core.websocket_server] - INFO - =======================================================
```

Because this is a full-module deployment, you have two important endpoints.

OTA endpoint:
```
http://your-computer-lan-ip:8002/xiaozhi/ota/
```

Websocket endpoint:
```
ws://your-computer-lan-ip:8000/xiaozhi/v1/
```

Be sure to write the two endpoint addresses above into the Admin Console. They affect websocket address distribution and auto-upgrade features.

1. Use the super admin account to log in to the Admin Console. In the top menu, find `Parameter Management`, then find parameter code `server.websocket`, and enter your `Websocket endpoint`.

2. Use the super admin account to log in to the Admin Console. In the top menu, find `Parameter Management`, then find parameter code `server.ota`, and enter your `OTA endpoint`.

Next, you can start using your ESP32 device. You can either `build the ESP32 firmware yourself`, or use `Xiage’s prebuilt firmware version 1.6.1 or above`. Choose either one.

1. [Build your own ESP32 firmware](firmware-build.md).

2. [Configure a custom server based on Xiage’s prebuilt firmware](firmware-setting.md).

# FAQ
Below are some common issues for reference:

1. [Why does Xiaozhi recognize many Korean, Japanese, or English words from my speech?](./FAQ.md)<br/>
2. [Why does “TTS task error: file does not exist” appear?](./FAQ.md)<br/>
3. [TTS often fails or times out](./FAQ.md)<br/>
4. [Wi-Fi can connect to self-hosted server, but 4G mode cannot](./FAQ.md)<br/>
5. [How can I improve Xiaozhi’s response speed?](./FAQ.md)<br/>
6. [I speak slowly; why does Xiaozhi interrupt me during pauses?](./FAQ.md)<br/>

## Deployment Tutorials
1. [How to automatically pull the latest code, auto-build, and start](./dev-ops-integration.md)<br/>
2. [How to deploy MQTT gateway and enable MQTT + UDP protocol](./mqtt-gateway-integration.md)<br/>
3. [How to integrate with Nginx](https://github.com/xinnan-tech/xiaozhi-esp32-server/issues/791)<br/>

## Extension Tutorials
1. [How to enable mobile number registration for Admin Console](./ali-sms-integration.md)<br/>
2. [How to integrate HomeAssistant for smart home control](./homeassistant-integration.md)<br/>
3. [How to enable vision model for photo object recognition](./mcp-vision-integration.md)<br/>
4. [How to enable MCP endpoint](./mcp-endpoint-enable.md)<br/>
5. [How to integrate MCP endpoint](./mcp-endpoint-integration.md)<br/>
6. [How to enable voiceprint recognition](./voiceprint-integration.md)<br/>
7. [News plugin source configuration guide](./newsnow_plugin_config.md)<br/>
8. [Weather plugin usage guide](./weather-integration.md)<br/>

## Voice Cloning / Local Voice Deployment Tutorials
1. [How to clone voice in Admin Console](./huoshan-streamTTS-voice-cloning.md)<br/>
2. [How to deploy and integrate index-tts local voice](./index-stream-integration.md)<br/>
3. [How to deploy and integrate fish-speech local voice](./fish-speech-integration.md)<br/>
4. [How to deploy and integrate PaddleSpeech local voice](./paddlespeech-deploy.md)<br/>

## Performance Testing Tutorials
1. [Component speed testing guide](./performance_tester.md)<br/>
2. [Regular public test results](https://github.com/xinnan-tech/xiaozhi-performance-research)<br/>
