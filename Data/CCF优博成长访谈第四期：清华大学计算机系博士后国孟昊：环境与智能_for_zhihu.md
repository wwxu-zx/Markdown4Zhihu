> 国孟昊 清华大学计算机系博士后



## **Notes**

### 1. **很多我们以为是“自身属性”的东西，其实是环境塑造的结果。**

![screenshot-20260426-171459](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第四期：清华大学计算机系博士后国孟昊：环境与智能_for_zhihu/screenshot-20260426-171459.png)



### 2. **<span style="color: inherit; background-color: rgba(255,246,122,0.8)">AI 协同进化三阶段</span>**

* **环境在演化，智能也在演化**

  * 从宏观来看，AI 从2010年到现在这十几年的发展可以看成&#x662F;**<span style="color: inherit; background-color: rgba(255,246,122,0.8)">环境与智能的协同进化</span>**。

    * **环境**：指的是比如说**数据、任务、交互的形式**。

    * **智能体**：我们可以把它理解成一个**系统**，它能够**感知环境、做出决策并采取行动**。

    ![screenshot-20260505-214507](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第四期：清华大学计算机系博士后国孟昊：环境与智能_for_zhihu/screenshot-20260505-214507.png)

  * 如果从一个动态的角度来看，**环境在不断变得丰富**，从早期的静态图像到多模态、到开放世界的问答，再到真实的物理世界的任务。**随着环境的变化，智能体也在不断的演化**，从最初单一的感知模型（e.g., ResNet, YOLO），逐渐发展成具备理解、推理，甚至自主行动的智能体。所以可以看到一个很明确的趋势，就&#x662F;**<span style="color: inherit; background-color: rgba(255,246,122,0.8)">环境在演化，智能也在演化。环境影响着智能的进化。</span>**

  ![screenshot-20260505-214640](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第四期：清华大学计算机系博士后国孟昊：环境与智能_for_zhihu/screenshot-20260505-214640.png)

  ![screenshot-20260505-214705-1](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第四期：清华大学计算机系博士后国孟昊：环境与智能_for_zhihu/screenshot-20260505-214705-1.png)



<table><colgroup><col width="197"><col width="169"><col width="169"><col width="262"></colgroup>
<thead>
<tr>
<th>时间阶段</th>
<th><strong>环境</strong></th>
<th><strong>智能体</strong></th>
<th>特点</th>
</tr>
</thead>
<tbody>
<tr>
<td>第一阶段（2010～2020）</td>
<td><strong>单一代理问答</strong>
<strong>(proxy QA)</strong></td>
<td><br /><strong>单问答模型</strong><br /></td>
<td><ol>
<li><strong>这个阶段的<span style="color: inherit; background-color: rgba(255,246,122,0.8)">环境是静态的，边界是明确的，定义是清楚的。</span></strong></li>
<li><strong><span style="color: inherit; background-color: rgba(255,246,122,0.8)">对单一任务所做的模型，大多都是单点能力很强，但是缺乏泛化性、鲁棒性、整体性。</span></strong></li>
</ol></td>
</tr>
<tr>
<td>第二阶段（2020～2025）</td>
<td><strong>开放问答</strong>
<strong>(open QA)</strong><br /></td>
<td><strong>开放问答模型</strong><br /></td>
<td><ol>
<li><strong>开放世界的问题，环境开始走向开放、多样。</strong></li>
<li><strong>不再完成单一任务，而是能统一地理解、回答各种问题。</strong></li>
<li><strong><span style="color: inherit; background-color: rgba(255,246,122,0.8)">给模型出题，让模型去解。</span></strong></li>
</ol><strong>     【这个阶段还是做题或问答】</strong></td>
</tr>
<tr>
<td>第三阶段（2025～至今）</td>
<td><strong>真实世界环境</strong>
<strong>(Agentic tasks)</strong></td>
<td><strong>智能体、机器人</strong></td>
<td><ol>
<li><strong>这个阶段的环境是动态的、开放的，充满不确定性的。</strong></li>
<li><strong>需要观察目标、理解目标、分解步骤、作出行动，并且甚至还需要反馈。</strong></li>
<li><strong><span style="color: inherit; background-color: rgba(255,246,122,0.8)">进入世界，在真实世界中完成任务，真正让模型去完成一个任务。</span></strong></li>
</ol></td>
</tr>
</tbody>
</table>

* **第一阶段（2010—2020 左右）是<span style="color: inherit; background-color: rgba(255,246,122,0.8)">封闭环境</span>。**&#x6211;&#x4EEC;**<span style="color: inherit; background-color: rgba(255,246,122,0.8)">事先给模型准备好一个数据集、一个任务定义、一个评价指标</span>**，然后它就在这个框架里面进行优化。这样的环境其实就是在约束模型，你只需要在一个相对明确、相对标准化的这种任务中把答案做对就可以了。这个时候，我们要求的智能就是要完成这个环境里的任务（分类、检测、分割、追踪之类的一些问题）。这个阶段的代表性工作是 ResNet、YOLO、Fast-RCNN 这类模型，<span style="color: inherit; background-color: rgba(255,246,122,0.8)">它们在一个单点任务上可以做的很好，但是在开放世界中泛化性、鲁棒性就不行了</span>。为什么？因为当时的环境就是这样的——**<span style="color: inherit; background-color: rgba(255,246,122,0.8)">预先定义的任务和数据集，导致演化出来的智能也只能是单任务的解题器。</span>**

* **第二阶段（2020～2025）**&#x662F;**<span style="color: inherit; background-color: rgba(255,246,122,0.8)"> CLIP 之后的开放世界</span>**。从那个点开始，人们就不再关心“我在 ImageNet 上能从 85 跑到 90”这种问题，而是开始关注泛化性，出现了像 MMMU 这样把整个大学考试都拿出来让模型做的环境。这个阶段的代表是 GPT-4、Gemini、Qwen 这些大模型——**<span style="color: inherit; background-color: rgba(255,246,122,0.8)">它们不再完成单一任务，而是能统一地理解、回答各种问题。但这种方式还停留在“回答世界”，而不是真正“进入世界”</span>**。

* **第三阶段（2025～至今）是<span style="color: inherit; background-color: rgba(255,246,122,0.8)">真实世界的任务</span>。**&#x73B0;在我&#x4EEC;**<span style="color: inherit; background-color: rgba(255,246,122,0.8)">不再让模型做题</span>**，而是让&#x5B83;**<span style="color: inherit; background-color: rgba(255,246,122,0.8)">真正去完成任务</span>**——OS World、GUI 操作、Robotics。**<span style="color: inherit; background-color: rgba(255,246,122,0.8)">从 Question &amp; Answer 变成了 Task &amp; Action</span>**。这个阶段我们不关心模型中间过程懂没懂，**<span style="color: inherit; background-color: rgba(255,246,122,0.8)">只关心一件事：任务成功率</span>**。

  * 真正到了这个阶段，所谓的视觉智能才出现了它的端到端形态。从人的角度看，人的输出本质上就两类：一类是**语言**，另一类是**动作**。所以视觉的端到端智能必须落到动作上——你只要看到场景能把动作做对就够了。【人的两类输出，**语言和动作**；对于AI，现在动作还没解决，那是人擅长的部分。】

  **<span style="color: inherit; background-color: rgba(255,246,122,0.8)">现在的 AI 本质上是以语言为中心的，包括所谓的多模态大模型，核心还是语言。</span>**&#x5B83;可以解一道复杂数学题、写几万行代码，但却很难帮你叠一件衣服、在你家里工作。人平时就生活在真实的物理世界里，所以这个方面是要重点突破的——从**语言智能**真正走向**物理世界的智能**。【**具身智能**】

  ![screenshot-20260426-181633](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第四期：清华大学计算机系博士后国孟昊：环境与智能_for_zhihu/screenshot-20260426-181633.png)



### 3. **<span style="color: inherit; background-color: rgba(255,246,122,0.8)">AI 竞争已经从模型转向环境</span>**

* **<span style="color: inherit; background-color: rgba(255,246,122,0.8)">智能不是凭空出现的，是由环境塑造出来的。有什么样的环境，就会孕育出什么样的智能。</span>**

* **AI发展的核心挑战之一是环境**。现在的 AI 竞争，某种意义上已经从&#x62FC;**<span style="color: inherit; background-color: rgba(255,246,122,0.8)">模型的能力</span>**&#x8F6C;变成&#x62FC;**<span style="color: inherit; background-color: rgba(255,246,122,0.8)">环境的构造能力</span>**。e.g., 大厂洗数据，其实也是在给大模型构造环境，相当于提供高质量的数据/环境，它就能学得更好。**<span style="color: inherit; background-color: rgba(255,246,122,0.8)">谁能模拟更真实的环境，谁就更可能做出下一代更强的智能</span>**。

![screenshot-20260426-181944-1](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第四期：清华大学计算机系博士后国孟昊：环境与智能_for_zhihu/screenshot-20260426-181944-1.png)

![screenshot-20260510-191552-1](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第四期：清华大学计算机系博士后国孟昊：环境与智能_for_zhihu/screenshot-20260510-191552-1.png)



### 4. 训练你自己：<span style="color: inherit; background-color: rgba(255,246,122,0.8)">先成为一个“可训练”的人</span>

![screenshot-20260510-191259](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第四期：清华大学计算机系博士后国孟昊：环境与智能_for_zhihu/screenshot-20260510-191259.png)

* 讲了这么多 AI，其实人也是一样的。**我们每个人都可以看成是在环境里训练我们自己——个人就是模型，你接触的人、所在平台、互联网上的知识就是训练语料，你追求的是论文、做系统、还是真实问题，就是你的损失函数。**&#x6240;以有时候研究生发展得好不好，并不是因为模型大、所谓“我聪明”，而是这个**环境对不对、目标清不清楚、训练过程能不能持续**。这件事在 AI 发展里也能看出来——**模型架构和初始化参数其实没那么重要，最大的壁垒是数据是什么**。

* 第一步是让自己成为一个可训练的人。可训练不是说你一开始就很强，而是你能不断吸收外部反馈、修正自己、持续进化。一个可训练的人愿意接受新鲜事物，能够走出舒适区，从失败中提取各种各样的信息，而不是抱怨。从机器学习的角度看，我&#x4EEC;**<span style="color: inherit; background-color: rgba(255,246,122,0.8)">要做一个有学习率、能否持续优化的系统</span>**。





### 5. 优化你的环境

![screenshot-20260426-182808](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第四期：清华大学计算机系博士后国孟昊：环境与智能_for_zhihu/screenshot-20260426-182808.png)

![screenshot-20260510-192617](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第四期：清华大学计算机系博士后国孟昊：环境与智能_for_zhihu/screenshot-20260510-192617.png)

**第二步是找到适合自己的环境，并且主动优化它。每个人的环境其实都不完美，需要去筛选、调整、甚至重构。**

具体来说，环境主要由三部分组成：

* 你周围的人

* 你所在的平台

* 用好AI和互联网，把我们的环境从一个小环境变成一个大环境。

  * 让AI尽量帮我们做更多的事；

  * 用好互联网环境，获取高质量的训练数据。



* **关注自己的环境，找到一个适合自己的环境**

  * 你是否真正在前沿？你的反馈质量高不高？你能不能真正地被激发出来？我现在所处的环境到底是不是真的能把我训练出来？

  * 什么样的信息值得输入？什么样的事情是低水平重复的？什么样的合作关系能让你真正地得到成长？什么样的社交对你有帮助？什么样的社交只会消耗你的注意力？什么目标是重要的？什么是短期噪声？

  * 在我们自己的环境里，什么样的成长路径才是最适合我们自己的？

* **筛选、调整，甚至是重构环境**

  * 如果把自己当作一个智能体，我们要**不断洗数据、洗环境，改善数据管线，改善环境管线，调整目标**。【**<span style="color: inherit; background-color: rgba(255,246,122,0.8)">洗自己的环境</span>**】

  * 一个人的瓶颈的上限有时候是接触了太多低质量的输入，导致上限被压低了。从模型的角度来看，垃圾数据是训不出来好模型的。如果我们处在一个垃圾环境里，很难让我们自己有一个非常高的表现的。【**<span style="color: inherit; background-color: rgba(255,246,122,0.8)">垃圾数据训不出好模型，垃圾环境也很难有高表现</span>**】

* **<span style="color: inherit; background-color: rgba(255,246,122,0.8)">最终目标是进入一个比较正向的循环。【正反馈的循环】</span>**

  ![screenshot-20260426-184315](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第四期：清华大学计算机系博士后国孟昊：环境与智能_for_zhihu/screenshot-20260426-184315.png)

  * 有一段时间，我们可能发现我们自己变强了，你其实进入了一个正反馈的循环。**你的学习率很好，你的环境也很好，你的反馈也很好，这样你的model更新起来就会顺畅很多。**



### 6. 一些有启发的认知

* **<span style="color: inherit; background-color: rgba(255,246,122,0.8)">不要用堆时间去掩盖你的效率问题。</span>**&#x5F62;式上的努力不一定有用。不要把“时间堆上”等同于“事情能做好”——不能用时间去掩盖自己的懒惰。

* **<span style="color: inherit; background-color: rgba(255,246,122,0.8)">道阻且长，行则将至</span>**

  * 正如最近有人评价《黑神话·悟空》团队时所说的那样：**“踏上取经路，比抵达灵山更重要”。**

  * **决策要符合自己内心的想法。**&#x575A;持自己的想法以后，不管这件事做成或没做成，最起码你不会后悔。

  * **人生没有白走的路。**&#x4F60;在过程中所积攒的经验、能力、历练，会最终成为你在某个时刻获得那本经书、获得预期大结果的原因。

* **AI 时代最重要的是 <span style="color: inherit; background-color: rgba(255,246,122,0.8)">Insight</span> 和 <span style="color: inherit; background-color: rgba(255,246,122,0.8)">发现高价值问题的能力</span>。【人比AI强的地方】**

  * **不要尝试去和 AI 比赛——你用古法编程去和 AI 比谁编得好，这件事意义不大。**&#x91CD;要的是有好的科研品味、好的 idea，然后和 AI 一起把这件事做好就够了。你不需要证明自己比 AI 强，更应该好好利用 AI 去做事。

  * **找到那些重要并且值得做的问题能力很重要。**&#x41;I 时代带来了大量噪音，发现和定义重要问题、高价值问题的能力，AI 还比较难捕获。【**之前还会结合实现能力评估你，现在你的 label 就是你的想法、你解决的问题**】

* **认真科研，但也要<span style="color: inherit; background-color: rgba(255,246,122,0.8)">认真生活</span>。**&#x79D1;研很重要、成长很重要、追求卓越很重要——但人生并不是只有科研。我们前面一直讲环境怎么塑造智能，其&#x5B9E;**<span style="color: inherit; background-color: rgba(255,246,122,0.8)">你的人生体验、兴趣、家人朋友的关系、运动、阅读、旅行——这些同样是你的环境，同样在塑造你。</span>**





### References

**B站视频：**

【【优博之路】环境与智能】 https://www.bilibili.com/video/BV1iLdrBUEsS/?share\_source=copy\_web\&vd\_source=6771d35251ef5959f68e7e6ca14fb957

**文字版：**

[环境与智能：国孟昊的“三阶段进化、可训练人格与正反馈循环”](https://mp.weixin.qq.com/s/uvZS1-GbDNQpScUZC4IogA)

**国孟昊相关链接：**

**个人主页：**&#x68;ttps://menghaoguo.github.io/

[高年级学生代表国孟昊在2024级研究生开学典礼上的发言](https://www.cs.tsinghua.edu.cn/info/1058/6332.htm)





***

## **附录：B站视频部分截图**

![screenshot-20260426-170720](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第四期：清华大学计算机系博士后国孟昊：环境与智能_for_zhihu/screenshot-20260426-170720.png)



![screenshot-20260426-171459-1](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第四期：清华大学计算机系博士后国孟昊：环境与智能_for_zhihu/screenshot-20260426-171459-1.png)



![screenshot-20260505-214507-1](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第四期：清华大学计算机系博士后国孟昊：环境与智能_for_zhihu/screenshot-20260505-214507-1.png)



![screenshot-20260505-214534](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第四期：清华大学计算机系博士后国孟昊：环境与智能_for_zhihu/screenshot-20260505-214534.png)



![screenshot-20260505-214546](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第四期：清华大学计算机系博士后国孟昊：环境与智能_for_zhihu/screenshot-20260505-214546.png)



![screenshot-20260505-215012](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第四期：清华大学计算机系博士后国孟昊：环境与智能_for_zhihu/screenshot-20260505-215012.png)



![screenshot-20260505-214912](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第四期：清华大学计算机系博士后国孟昊：环境与智能_for_zhihu/screenshot-20260505-214912.png)



![screenshot-20260505-214640-1](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第四期：清华大学计算机系博士后国孟昊：环境与智能_for_zhihu/screenshot-20260505-214640-1.png)



![截屏2026-05-05 21.47.05-1-1](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第四期：清华大学计算机系博士后国孟昊：环境与智能_for_zhihu/截屏2026-05-05%2021.47.05-1-1.png)



![screenshot-20260426-181633-1](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第四期：清华大学计算机系博士后国孟昊：环境与智能_for_zhihu/screenshot-20260426-181633-1.png)



![screenshot-20260426-181927](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第四期：清华大学计算机系博士后国孟昊：环境与智能_for_zhihu/screenshot-20260426-181927.png)



![screenshot-20260426-181944](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第四期：清华大学计算机系博士后国孟昊：环境与智能_for_zhihu/screenshot-20260426-181944.png)



![screenshot-20260510-191552](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第四期：清华大学计算机系博士后国孟昊：环境与智能_for_zhihu/screenshot-20260510-191552.png)



![screenshot-20260510-191259-1](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第四期：清华大学计算机系博士后国孟昊：环境与智能_for_zhihu/screenshot-20260510-191259-1.png)



![screenshot-20260426-182808-1](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第四期：清华大学计算机系博士后国孟昊：环境与智能_for_zhihu/screenshot-20260426-182808-1.png)



![screenshot-20260510-192617-1](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第四期：清华大学计算机系博士后国孟昊：环境与智能_for_zhihu/screenshot-20260510-192617-1.png)



![screenshot-20260426-184315-1](https://cdn.jsdelivr.net/gh/wwxu-zx/Markdown4Zhihu@master/Data/CCF优博成长访谈第四期：清华大学计算机系博士后国孟昊：环境与智能_for_zhihu/screenshot-20260426-184315-1.png)
