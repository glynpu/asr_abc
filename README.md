# 语音识别的简单示例,主要在课堂演示使用

## 创建python虚拟环境


在linux 和macos 上验证通过

```
# 如果已经有pyhon3.6 环境，跳过该步骤，使用现有环境也可以
virtualenv ~/env/asr_abc --python=python3.8
. ~/env/asr_abc/bin/activate
```
## 安装本项目

```
python setup.py install
or 
pip install .
```

## 识别wav音频

Note: 输入音频采样率必须是16k,如果待识别音频不是16k,可以采用以下命令重采样为16k.

```
ffmpeg -i ks1_48k.acc -ar 16000 ks1_16k.wav
```

```
python decode.py
# 或debug 模式
python decode.py -d

#预期输出:
2021-12-24 17:08:31,736 INFO [decode.py:91] All files seem exist.
2021-12-24 17:08:31,736 INFO [decode.py:96] Start loading model.
2021-12-24 17:08:41,321 INFO [decode.py:113] Start loading dict.
2021-12-24 17:08:41,336 INFO [decode.py:119] Start recognize data/wavs/BAC009S0764W0143.wav.
2021-12-24 17:08:41,527 INFO [decode.py:134] Result: 在市场整体从高速增长进入中高速增长区间的同时
2021-12-24 17:08:41,527 INFO [decode.py:135] done.

# 也可以指定输入音频
python decode.py --input-wav=data/wavs/ks1_16k.wav
或者
python decode.py -i=data/wavs/ks1_16k.wav  # ks is short for "Kantanzhe Song"
# 预期输出：
2021-12-27 19:16:02,911 INFO [decode.py:91] All files seem exist.
2021-12-27 19:16:02,911 INFO [decode.py:96] Start loading model.
2021-12-27 19:16:08,405 INFO [decode.py:113] Start loading dict.
2021-12-27 19:16:08,409 INFO [decode.py:119] Start recognize data/wavs/ks1_16k.wav.
2021-12-27 19:16:08,449 INFO [decode.py:137] Result: 我们有火焰般的热情
2021-12-27 19:16:08,450 INFO [decode.py:138] done.
```

## 相关项目链接：

```
https://github.com/k2-fsa/icefall
https://github.com/k2-fsa/k2
https://github.com/lhotse-speech/lhotse
```


## 手动模型下载

如果上述`python decode.py` 已识别出预期结果，说明模型已自动从下载源1成功下载模型，无需关注以下内容。

下载源1:(decode.py 代码会自动访问这个源下载):
https://huggingface.co/GuoLiyong/cn_conformer_encoder_aishell/tree/main/data/lang_char

下载源2: 百度网盘
```
链接: https://pan.baidu.com/s/17tPOJM_Sm49q1kZrE3jfUQ
提取码: qa4p
```

对于访问下载源1有困难活着访问速度过慢的同学，可以手动从百度网盘下载.
下载完毕后按以下文件结构放置下载所得的"tokens.txt"和"conformer_encoder.pt"两个文件：

```
.
|-- README.md
|-- build
|   `-- bdist.linux-x86_64
|-- conformer.py
|-- data
|   |-- lang_char
|   |   |-- tokens.txt
|   `-- wavs
|       |-- BAC009S0764W0143.wav
|       |-- README.md
|       `-- transcript
|-- decode.py
|-- exp
|   `-- conformer_encoder.pt
|-- requirements.txt
|-- setup.py
`-- utils.py
```

