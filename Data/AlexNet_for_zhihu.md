# AlexNet (ImageNet Classification with Deep Convolutional Neural Networks)

**Title: ImageNet Classification with Deep Convolutional Neural Networks**

**Paper:** <https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf>

【**NIPS 2012**】



## 1. Introduction

* 60 million parameters

* 8 layers（five convolutional layers + three fully-connected layers）, 1000-way softmax

* **ReLU** (计算更简单；使训练模型更加容易)

* Reducing Overfitting

  * **Dropout (regularization)**

  * Data Augmentation (更大的训练样本量)

### 1.1 ImageNet

**ImageNet**: <https://www.image-net.org/>

![c110c996081b5b52ba3a5418544540e7](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/AlexNet_for_zhihu/c110c996081b5b52ba3a5418544540e7.png)

![9fc2316dce4d7713406122ada4d85d92](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/AlexNet_for_zhihu/9fc2316dce4d7713406122ada4d85d92.png)

AlexNet 赢下了 2012 ImageNet 竞赛后，标注着新一轮神经网络热潮的开始。

### 1.2 CNNs

![1793c88ca818f8a88e63a95f21d4a3ba](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/AlexNet_for_zhihu/1793c88ca818f8a88e63a95f21d4a3ba.png)

### 1.3 AlexNet带来第三波AI浪

![c9bda52a1da4bdb5e800275cf47c5951](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/AlexNet_for_zhihu/c9bda52a1da4bdb5e800275cf47c5951.jpg)

**人工特征 —> 神经网络自动提取特征**。如上图所示，左侧人工特征提取和SVM是**独立的过程**；而右侧通过神经网络自动提取特征和Softmax分类是**一起训练的过程**。

**<span style="color: inherit; background-color: rgba(255,246,122,0.8)">神经网络自动提取特征</span>**

* **<span style="color: inherit; background-color: rgba(255,246,122,0.8)">End-to-end（端到端，没有复杂的特征工程），直接处理原始像素（raw RGB values of the pixels），简化了数据预处理。</span>**

* **<span style="color: inherit; background-color: rgba(255,246,122,0.8)">Learn from data（数据驱动）</span>**

![0f66fed8dbfc762459d45999968ef9d5](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/AlexNet_for_zhihu/0f66fed8dbfc762459d45999968ef9d5.jpg)

**注：**

* 除了在训练集上对像素减去平均活跃度 (mean activity)，没有进行任何其他方式的预处理。

* 算均值时通常有两种计算方法。一种是 image mean，是对 RGB 三个通道都求均值，然后再从各个通道减去该均值；另一种是pixel mean，直接全图减去全部像素的均值。本文应该是取的第一种。

* 通过 **center crop** 对图片进行裁剪很常用。

  * e.g.，通过 Nano banana (Gemini Flash Image Model) API 得到的 16:9 图片，其实际 aspect\_ratio 并不是严格16:9的（w\*h=1344x768），若直接用之作为 first frame 调用 VEO 3.1 API 去生成 16:9 的视频，得到的视频左右两侧会有黑边。一个简单的解决方案是通过 center crop 将 image 裁剪为严格 16:9 宽高比（1344x768 -> 1344x756）。



## 2. AlexNet架构

![d1eed7b86fbb8b292ae2390a538fe44f](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/AlexNet_for_zhihu/d1eed7b86fbb8b292ae2390a538fe44f.jpg)

**AlexNet 可视化**：<https://dgschwend.github.io/netscope/#/preset/alexnet>

* Netscope 是一个在线可视化工具，使用它可以把 Caffe 的 .prototxt文件（定义模型结构）可视化，直观地理解模型结构和数据流动

![e1fec94dfade9aad79b5a3e8795d6078](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/AlexNet_for_zhihu/e1fec94dfade9aad79b5a3e8795d6078.jpg)

![7d11b1bfb5a3ae46aad48c4dd0cb7bc7](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/AlexNet_for_zhihu/7d11b1bfb5a3ae46aad48c4dd0cb7bc7.jpg)

**注意**

`(224-11)/4` 不能整除，会向下取整，也就是说 Kernel 在水平移动时，最后几个不足 kernel\_size 的像素会被丢掉。在 Netscope 中这里被修改了，里面的输入被 resize 到 `227*227*3`。

* [0, 10], [11, 20], ..., [211, 220]

* [221, 223]三个像素被丢掉

如想要计算 **Shape** 的变化，可参考：

<https://docs.pytorch.org/docs/stable/generated/torch.nn.Conv2d.html#conv2d>

![85f53fca2583a39bc19933a3b3e09f13](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/AlexNet_for_zhihu/85f53fca2583a39bc19933a3b3e09f13.png)

简化版的公式为：

`（w + 2*padding - kernel_size）/ stride + 1`

以这里 <https://zh-v2.d2l.ai/chapter_convolutional-modern/alexnet.html#id14> 网络各层shape变化为例，

**AlexNet 是更大更深的 LeNet。**&#x4E24;者对比如下：

![cd576b676097e58db7f4fc62e51ee429](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/AlexNet_for_zhihu/cd576b676097e58db7f4fc62e51ee429.png)

![f4f08e80736e766bb490d578c7c1f9bc](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/AlexNet_for_zhihu/f4f08e80736e766bb490d578c7c1f9bc.png)

![e5ebb248adcfee73a8441dcacbb46369](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/AlexNet_for_zhihu/e5ebb248adcfee73a8441dcacbb46369.png)



![e5cecad3fd01acabaa4f7896528c7a64](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/AlexNet_for_zhihu/e5cecad3fd01acabaa4f7896528c7a64.png)

## 3. 学习表征（Representations）

![506c1a5125ec18abaeabda52772c9f54](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/AlexNet_for_zhihu/506c1a5125ec18abaeabda52772c9f54.png)

如上图右侧第2行，这些大象图片之间的像素值本身非常不同，但是它们是高度相似的概念。【**semantically similar**】

AlexNet 确实学会了数据的高维表示。**This high dimensional space is often called a latent or embedding space.**

## 4. 数据/算力/模型的scaling

![24f4cef1a2cff9055a1fdca195b64a2e](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/AlexNet_for_zhihu/24f4cef1a2cff9055a1fdca195b64a2e.png)

![65160aeaf641b62229aa0f18a8a3b978](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/AlexNet_for_zhihu/65160aeaf641b62229aa0f18a8a3b978.png)

![33c1eec615a108b4213189594f4c65c8](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/AlexNet_for_zhihu/33c1eec615a108b4213189594f4c65c8.png)

**<span style="color: inherit; background-color: rgba(255,246,122,0.8)">scale of data and compute</span>**



## References

[Krizhevsky A, Sutskever I, Hinton G E. Imagenet classification with deep convolutional neural networks[J]. Advances in neural information processing systems, 2012, 25.](https://proceedings.neurips.cc/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf)

[Krizhevsky A, Sutskever I, Hinton G E. ImageNet classification with deep convolutional neural networks[J]. Communications of the ACM, 2017, 60(6): 84-90.](https://dl.acm.org/doi/pdf/10.1145/3065386)

[【7.1. 深度卷积神经网络（AlexNet）【动手学深度学习v2】】](https://zh-v2.d2l.ai/chapter_convolutional-modern/alexnet.html)

【9年后重读深度学习奠基作之一：AlexNet【论文精读·2】】 <https://www.bilibili.com/video/BV1ih411J7Kz/?share_source=copy_web&vd_source=6771d35251ef5959f68e7e6ca14fb957>

【AlexNet论文逐段精读【论文精读】】 <https://www.bilibili.com/video/BV1hq4y157t1/?share_source=copy_web&vd_source=6771d35251ef5959f68e7e6ca14fb957>

【24 深度卷积神经网络 AlexNet【动手学深度学习v2】】 <https://www.bilibili.com/video/BV1h54y1L7oe/?share_source=copy_web&vd_source=6771d35251ef5959f68e7e6ca14fb957>

【从 AlexNet 开始，人们就无法理解 AI 在干什么了】 <https://www.bilibili.com/video/BV1SvDfYDEDA/?share_source=copy_web&vd_source=6771d35251ef5959f68e7e6ca14fb957>
