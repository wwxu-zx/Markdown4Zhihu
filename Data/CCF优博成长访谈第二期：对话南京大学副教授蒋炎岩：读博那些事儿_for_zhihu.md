> 蒋炎岩 南京大学副教授，博士生导师



## **Notes**

### 1. **<span style="color: inherit; background-color: rgba(255,246,122,0.8)">数据就是知识，压缩就是智能。</span>**

* **<span style="color: inherit; background-color: rgba(255,246,122,0.8)">预训练决定模型“学会了什么、会到什么程度、以及以什么方式组织知识”</span>**

* **<span style="color: inherit; background-color: rgba(255,246,122,0.8)">正确的 reward 方式</span>**

  * **<span style="color: inherit; background-color: rgba(255,246,122,0.8)">知道什么是好的、什么是不好的。</span>**

  * **<span style="color: inherit; background-color: rgba(255,246,122,0.8)">知道怎么去获得好的。</span>**

  * 人类本质上还是Reward Hacker

    * Long-term reward（更长远的reward） or short-term reward?&#x20;



### 2. **<span style="color: inherit; background-color: rgba(255,246,122,0.8)">学习是一个不断积累，厚积薄发的过程（Grokking，顿悟）。</span>**

* 预训练，**Grokking（val dataset 比 train dataset 收敛更慢，需要更多Optimization Steps）**

  * [Grokking: Generalization Beyond Overfitting on Small Algorithmic Datasets](https://arxiv.org/abs/2201.02177)

  ![screenshot-20260407-151015](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第二期：对话南京大学副教授蒋炎岩：读博那些事儿_for_zhihu/screenshot-20260407-151015.png)

* **有了很好的基础，就可以看更难的东西了（难的东西一下子看不懂很正常，可能它所依赖的前置基础知识没学好**）

  * 当你把训练你的所有东西都忘得差不多的时候，但你又能把它 reconstruct 出来的时候，你就成了一个Matured Problem Solver（成熟的问题解决者）。

  * 当我把所有问题都忘掉的时候，我就真正理解了。

* Reward Hacking

  * Wikipedia: https://en.wikipedia.org/wiki/Reward\_hacking

    > **Reward hacking** or **specification gaming** occurs when an [AI](https://en.wikipedia.org/wiki/Artificial_intelligence) trained with [reinforcement learning](https://en.wikipedia.org/wiki/Reinforcement_learning) optimizes an [objective function](https://en.wikipedia.org/wiki/Objective_function)—achieving the literal, formal specification of an objective—without actually achieving an outcome that the programmers intended. [DeepMind](https://en.wikipedia.org/wiki/DeepMind) researchers have analogized it to the human behavior of finding a "shortcut" when being evaluated: "In the real world, when rewarded for doing well on a homework assignment, a student might copy another student to get the right answers, rather than learning the material—and thus exploit a [loophole](https://en.wikipedia.org/wiki/Loophole) in the task specification." This idea is strongly associated with [Goodhart's Law](https://en.wikipedia.org/wiki/Goodhart%27s_law), which argues that when a measure becomes a target, it ceases to be a good measure.

  * Reward Hacking in Reinforcement Learning: https://lilianweng.github.io/posts/2024-11-28-reward-hacking/



### 3. 蒋老师过往研究和AI

* Concurrency（并发）

  * Concurrency（并发）是个老大难的问题——从做计算理论的人、到做体系结构的人要造并行计算机、到操作系统的人要做并发控制、到编程语言的人要做语言机制、到软件工程的人要面向开发者——所有人都在乎 Concurrency。每个领域都有它自己的方法论，而且都是很不一样的方法论。

  * 读博那些事儿: https://zhuanlan.zhihu.com/p/82579410

* 蒋老师在分享中有多次借用或提到 LLM 相关的一些概念，也提到了 **<span style="color: inherit; background-color: rgba(255,246,122,0.8)">CS336, Percy Liang 课程</span>**

  * 蒋老师本身是做System的，但也在学习 LLM 相关新知识。

  * &#x20;**<span style="color: inherit; background-color: rgba(255,246,122,0.8)">CS336 </span>这门课真的值得看呀，**&#x43;S336: Language Modeling from Scratch: https://cs336.stanford.edu/



### 4. 对AI时代的反思

* 编程 = 翻译？你再仔细想想，**<span style="color: inherit; background-color: rgba(255,246,122,0.8)">什么工作不是“翻译”？</span>**

  * 话说Transformer最初就是用来做翻译的。

* 在AI时代，不要给自己设限，去做一些你对其有兴趣的事、自己想要做的事、自己内心喜欢的事。

  * 未来我可以做些什么？

  * 追求自己内心真正的梦想。





### References

**B站视频：**

【[戒读] 绿导师读博那些事儿 (八年后回看版)】 https://www.bilibili.com/video/BV1oTwkzvEFu/?share\_source=copy\_web\&vd\_source=6771d35251ef5959f68e7e6ca14fb957

【【优博之路】读博那些事儿】 https://www.bilibili.com/video/BV1icw7zYE9m/?share\_source=copy\_web\&vd\_source=6771d35251ef5959f68e7e6ca14fb957

**文字版：**

[如果将人生看作一个模型：蒋炎岩的“预训练、收敛与反规训”](https://mp.weixin.qq.com/s/DAhRbHqaJmNe3lDIlvSaQw)

**蒋老师相关链接：**

* **个人主页：**&#x68;ttps://ics.nju.edu.cn/\~jyy/

* **知乎：**

  * 读博那些事儿: https://zhuanlan.zhihu.com/p/82579410

  * 绿导师是怎样戴帽的：学术跃进运动的来龙去脉：https://zhuanlan.zhihu.com/p/1986494838795941546

* **小红书：**[我决定要在人生巅峰退休了 - 小红书](https://www.xiaohongshu.com/discovery/item/69be9beb000000001d01f8a2?source=webshare\&xhsshare=pc_web\&xsec_token=ABzH1mu50w-Rr7LFlcybO9WYII4MS9CpCW-QZeo6i8br8=\&xsec_source=pc_share)





***

## **附录：B站视频部分截图**

![screenshot-20260405-194835](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第二期：对话南京大学副教授蒋炎岩：读博那些事儿_for_zhihu/screenshot-20260405-194835.jpg)



![screenshot-20260405-195047](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第二期：对话南京大学副教授蒋炎岩：读博那些事儿_for_zhihu/screenshot-20260405-195047.jpg)



![screenshot-20260405-195323](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第二期：对话南京大学副教授蒋炎岩：读博那些事儿_for_zhihu/screenshot-20260405-195323.jpg)



![screenshot-20260405-202748](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第二期：对话南京大学副教授蒋炎岩：读博那些事儿_for_zhihu/screenshot-20260405-202748.jpg)



![screenshot-20260405-200034](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第二期：对话南京大学副教授蒋炎岩：读博那些事儿_for_zhihu/screenshot-20260405-200034.jpg)



![screenshot-20260405-200142](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第二期：对话南京大学副教授蒋炎岩：读博那些事儿_for_zhihu/screenshot-20260405-200142.jpg)



![screenshot-20260405-200441](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第二期：对话南京大学副教授蒋炎岩：读博那些事儿_for_zhihu/screenshot-20260405-200441.jpg)



![screenshot-20260405-200625](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第二期：对话南京大学副教授蒋炎岩：读博那些事儿_for_zhihu/screenshot-20260405-200625.jpg)



![screenshot-20260405-200941](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第二期：对话南京大学副教授蒋炎岩：读博那些事儿_for_zhihu/screenshot-20260405-200941.jpg)



![screenshot-20260405-201152](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第二期：对话南京大学副教授蒋炎岩：读博那些事儿_for_zhihu/screenshot-20260405-201152.jpg)

![screenshot-20260405-201203](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第二期：对话南京大学副教授蒋炎岩：读博那些事儿_for_zhihu/screenshot-20260405-201203.jpg)

