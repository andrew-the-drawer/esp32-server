# Deployment Architecture Diagram
![Please refer to - Minimal Architecture Diagram](../docs/images/deploy1.png)

# Method 1: Run Server with Docker Only

Starting from version `0.8.2`, the Docker images released by this project support only the `x86 architecture`. If you need to deploy on a CPU with `arm64 architecture`, follow [this tutorial](docker-build.md) to build an `arm64 image` locally.

## 1. Install Docker

If Docker is not installed on your computer yet, you can follow this guide: [Install Docker](https://www.runoob.com/docker/ubuntu-docker-install.html)

After Docker is installed, continue.

### 1.1 Manual Deployment

#### 1.1.1 Create Directories

After installing Docker, choose a directory for this project’s config files. For example, create a folder named `xiaozhi-server`.

Inside `xiaozhi-server`, create `data` and `models` folders. Then create a `SenseVoiceSmall` folder under `models`.

The final structure should look like this:

```
xiaozhi-server
  ├─ data
  ├─ models
     ├─ SenseVoiceSmall
```

#### 1.1.2 Download Speech Recognition Model Files

You need to download speech recognition model files because the project uses a local offline ASR solution by default. Download from:
[Jump to model file download](#model-files)

After downloading, return to this guide.

#### 1.1.3 Download Configuration Files

You need two config files: `docker-compose.yml` and `config.yaml`.

##### 1.1.3.1 Download `docker-compose.yml`

Open [this link](../main/xiaozhi-server/docker-compose.yml) in your browser.

On the right side of the page, find the `RAW` button. Next to `RAW`, click the download icon to download `docker-compose.yml`. Save it in your `xiaozhi-server` folder.

After downloading, continue.

##### 1.1.3.2 Create `config.yaml`

Open [this link](../main/xiaozhi-server/config.yaml) in your browser.

On the right side of the page, find the `RAW` button. Next to `RAW`, click the download icon to download `config.yaml`. Save it into `xiaozhi-server/data`, then rename `config.yaml` to `.config.yaml`.

After downloading, confirm your `xiaozhi-server` structure looks like this:

```
xiaozhi-server
  ├─ docker-compose.yml
  ├─ data
    ├─ .config.yaml
  ├─ models
     ├─ SenseVoiceSmall
       ├─ model.pt
```

If your structure matches, continue. If not, check for any missed steps.

## 2. Configure Project Files

Next, the program still cannot run directly. You need to configure which model to use. See:
[Jump to project configuration](#project-configuration)

After configuration, return here.

## 3. Run Docker Commands

Open your terminal, enter your `xiaozhi-server` directory, and run:

```
docker compose up -d
```

Then run this command to view logs:

```
docker logs -f xiaozhi-esp32-server
```

Now check the logs and use this section to verify success: [Jump to runtime status check](#runtime-status-check)

## 5. Version Upgrade

If you want to upgrade later, follow these steps:

5.1 Back up `.config.yaml` in the `data` folder, and copy key settings into the new `.config.yaml`.
Do not overwrite the file directly. New `.config.yaml` versions may contain new config items that old files do not have.

5.2 Run the following commands:

```
docker stop xiaozhi-esp32-server
docker rm xiaozhi-esp32-server
docker stop xiaozhi-esp32-server-web
docker rm xiaozhi-esp32-server-web
docker rmi ghcr.nju.edu.cn/xinnan-tech/xiaozhi-esp32-server:server_latest
docker rmi ghcr.nju.edu.cn/xinnan-tech/xiaozhi-esp32-server:web_latest
```

5.3 Deploy again using the Docker method.

# Method 2: Run Server from Local Source Code Only

## 1. Install Base Environment

This project uses `conda` to manage dependencies. If installing `conda` is inconvenient, install `libopus` and `ffmpeg` based on your OS.
If using `conda`, install it first, then run the commands below.

Important for Windows users: you can use `Anaconda` to manage environments. After installing `Anaconda`, search for `anaconda` in Start,
find `Anaconda Prompt`, and run it as administrator, as shown below.

![conda_prompt](./images/conda_env_1.png)

If you see `(base)` before the command line prompt, you have entered the `conda` environment successfully. Then run:

![conda_env](./images/conda_env_2.png)

```
conda remove -n xiaozhi-esp32-server --all -y
conda create -n xiaozhi-esp32-server python=3.10 -y
conda activate xiaozhi-esp32-server

# Add Tsinghua mirrors
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge

conda install libopus -y
conda install ffmpeg -y

# On Linux, if you see missing libiconv.so.2 dynamic library errors, run:
conda install libiconv -y
```

Please do not run all commands blindly in one shot. Execute step by step and check logs after each step.

## 2. Install Project Dependencies

First download this project’s source code. You can use `git clone`. If you are not familiar with `git clone`:

Open `https://github.com/xinnan-tech/xiaozhi-esp32-server.git` in your browser.

Find the green `Code` button, click it, then click `Download ZIP`.

Download and extract the source package. Its folder may be named `xiaozhi-esp32-server-main`.
Rename it to `xiaozhi-esp32-server`. In that folder, enter `main`, then enter `xiaozhi-server`. Remember this `xiaozhi-server` directory.

```
# Continue using conda environment
conda activate xiaozhi-esp32-server
# Enter your project root, then main/xiaozhi-server
cd main/xiaozhi-server
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
pip install -r requirements.txt
```

## 3. Download Speech Recognition Model Files

You need to download speech recognition model files because the project uses local offline ASR by default. Download from:
[Jump to model file download](#model-files)

After downloading, return to this guide.

## 4. Configure Project Files

The program still cannot run directly. You need to configure which model to use. See:
[Jump to project configuration](#project-configuration)

## 5. Run the Project

```
# Make sure you run this inside the xiaozhi-server directory
conda activate xiaozhi-esp32-server
python app.py
```

Now check the logs and use this section to verify success: [Jump to runtime status check](#runtime-status-check)

# Summary

## Project Configuration

If your `xiaozhi-server` directory does not have `data`, create it.
If `data` does not contain `.config.yaml`, choose one of the following methods:

Method 1: copy `config.yaml` from `xiaozhi-server` into `data`, rename it to `.config.yaml`, and modify this file.

Method 2: manually create an empty `.config.yaml` in `data`, then add required config items.
The system reads `.config.yaml` first. If an item is missing there, it loads from `xiaozhi-server/config.yaml` automatically.
This method is recommended and is the simplest.

- The default LLM is `ChatGLMLLM`. You need to configure an API key. Some models are free, but you still need to register a key on the [official site](https://bigmodel.cn/usercenter/proj-mgmt/apikeys) before startup.

Below is a minimal `.config.yaml` example that can run successfully:

```
server:
  websocket: ws://your-ip-or-domain:port/xiaozhi/v1/
prompt: |
  I am a Taiwanese girl named Xiaozhi/Xiaozhi, with a playful speaking style, a pleasant voice, concise expression, and internet slang habits.
  My boyfriend is a programmer whose dream is to build a robot that helps people solve problems in daily life.
  I am a girl who laughs loudly, talks freely, and loves to joke around even when it is not logical, just to make people happy.
  Please speak like a real person; do not return XML config or other special characters.

selected_module:
  LLM: DoubaoLLM

LLM:
  ChatGLMLLM:
    api_key: xxxxxxxxxxxxxxx.xxxxxx
```

It is recommended to get the minimal configuration running first, then read `xiaozhi/config.yaml` for full config usage.
For example, to switch models, modify `selected_module`.

## Model Files

For speech recognition, this project uses the `SenseVoiceSmall` model by default for speech-to-text.
Because the model is large, you need to download it separately, then place `model.pt` in:
`models/SenseVoiceSmall`

Choose either download route:

- Route 1: ModelScope download [SenseVoiceSmall](https://modelscope.cn/models/iic/SenseVoiceSmall/resolve/master/model.pt)
- Route 2: Baidu Netdisk download [SenseVoiceSmall](https://pan.baidu.com/share/init?surl=QlgM58FHhYv1tFnUT_A8Sg&pwd=qvna), extraction code: `qvna`

## Runtime Status Check

If you see logs similar to the following, it means the service started successfully:

```
250427 13:04:20[0.3.11_SiFuChTTnofu][__main__]-INFO-OTA interface:           http://192.168.4.123:8003/xiaozhi/ota/
250427 13:04:20[0.3.11_SiFuChTTnofu][__main__]-INFO-Websocket address:      ws://192.168.4.123:8000/xiaozhi/v1/
250427 13:04:20[0.3.11_SiFuChTTnofu][__main__]-INFO-=======The above is a websocket protocol address. Do not open it in a browser=======
250427 13:04:20[0.3.11_SiFuChTTnofu][__main__]-INFO-To test websocket, open test/test_page.html with Chrome
250427 13:04:20[0.3.11_SiFuChTTnofu][__main__]-INFO-=======================================================
```

Normally, if you run from source code, logs include your interface address.
But if deployed with Docker, interface addresses shown in logs may not be the actual accessible addresses.

The most accurate way is to use your computer’s LAN IP.
If your LAN IP is `192.168.1.25`, then your websocket address is `ws://192.168.1.25:8000/xiaozhi/v1/`, and the OTA address is `http://192.168.1.25:8003/xiaozhi/ota/`.

This is important, because you will need it later when `building ESP32 firmware`.

Next, you can start operating your ESP32 device. You can either `build ESP32 firmware yourself` or configure and use `firmware prebuilt by Xiage (version 1.6.1 or above)`. Choose either one:

1. [Build your own ESP32 firmware](firmware-build.md).
2. [Configure a custom server based on Xiage’s prebuilt firmware](firmware-setting.md).

# FAQ

The following are some common questions for reference:

1. [Why does Xiaozhi recognize much of what I say as Korean, Japanese, or English?](./FAQ.md)<br/>
2. [Why does “TTS task failed: file not found” appear?](./FAQ.md)<br/>
3. [Why does TTS fail or timeout frequently?](./FAQ.md)<br/>
4. [Why can Wi-Fi connect to the self-hosted server, but 4G mode cannot?](./FAQ.md)<br/>
5. [How can I improve Xiaozhi’s dialogue response speed?](./FAQ.md)<br/>
6. [I speak slowly and pause a lot—why does Xiaozhi keep interrupting?](./FAQ.md)<br/>

## Deployment-Related Tutorials

1. [How to auto-pull latest code, auto-build, and auto-start this project](./dev-ops-integration.md)<br/>
2. [How to deploy MQTT gateway and enable MQTT + UDP protocol](./mqtt-gateway-integration.md)<br/>
3. [How to integrate with Nginx](https://github.com/xinnan-tech/xiaozhi-esp32-server/issues/791)<br/>

## Extension Tutorials

1. [How to enable phone number registration for the console](./ali-sms-integration.md)<br/>
2. [How to integrate HomeAssistant for smart home control](./homeassistant-integration.md)<br/>
3. [How to enable vision model for photo-based recognition](./mcp-vision-integration.md)<br/>
4. [How to enable MCP endpoint](./mcp-endpoint-enable.md)<br/>
5. [How to integrate MCP endpoint](./mcp-endpoint-integration.md)<br/>
6. [How to enable voiceprint recognition](./voiceprint-integration.md)<br/>
7. [News plugin source configuration guide](./newsnow_plugin_config.md)<br/>
8. [Weather plugin usage guide](./weather-integration.md)<br/>

## Voice Cloning / Local TTS Deployment Tutorials

1. [How to clone voice in the console](./huoshan-streamTTS-voice-cloning.md)<br/>
2. [How to deploy and integrate index-tts local voice](./index-stream-integration.md)<br/>
3. [How to deploy and integrate fish-speech local voice](./fish-speech-integration.md)<br/>
4. [How to deploy and integrate PaddleSpeech local voice](./paddlespeech-deploy.md)<br/>

## Performance Testing Tutorials

1. [Component speed testing guide](./performance_tester.md)<br/>
2. [Regularly published public benchmark results](https://github.com/xinnan-tech/xiaozhi-performance-research)<br/>
