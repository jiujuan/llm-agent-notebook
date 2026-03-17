> 以下报告来自 metaso.cn 秘塔AI撰写的LLM大模型发展历史分析报告 2026.02

## **摘要**

大语言模型代表了人工智能领域自深度学习兴起以来最重大的范式转移之一。本报告系统性地梳理了LLM从早期思想萌芽到当前智能涌现状态的完整历史发展历程。报告首先追溯至20世纪中叶的计算语言学起源，分析ELIZA、SHRDLU等早期系统所体现的符号主义尝试，以及n-gram统计语言模型在语音识别领域奠定的数学基础。随后，报告深入剖析了神经网络复兴时代的关键突破，包括LSTM解决长程依赖问题、Word2Vec开创词嵌入新范式，以及Geoffrey Hinton、Yann LeCun、Yoshua Bengio三位“深度学习之父”的奠基性工作。

本报告的核心在于，详细阐述了2017年Transformer架构的革命性意义，它如何通过自注意力机制彻底改变了序列建模的范式，成为所有现代LLM的基石。基于此架构，报告进一步剖析了GPT系列（Radford等，2018-2020）与BERT（Devlin等，2018）所代表的两种预训练范式（自回归与自编码）的分野与竞争。报告特别关注了RLHF（基于人类反馈的强化学习）技术的兴起，以InstructGPT（Ouyang等，2022）为标志性工作，揭示了模型对齐成为与能力提升同等重要的核心技术维度。最后，报告将ChatGPT（2022）与Claude等产品的爆发置于完整的技术链条中进行定位，并展望了多模态、智能体等未来方向。

本报告通过追溯关键学术论文、代表人物、技术演进逻辑，旨在构建一个完整、连贯且深刻的大模型技术发展图谱，阐明各技术节点之间的承继与突破关系。

## **1. 思想萌芽与早期探索（1950s-1990s）**

### **1.1 符号主义的早期尝试：从规则到对话**

大语言模型的根源可追溯至人工智能研究的黎明期，其起点与整个AI领域的起点重合。1950年，**艾伦·图灵提出“机器可以思考吗？”**这一根本性问题，为后续所有智能机器的发展奠定了哲学基础 [[1]]。1956年的达特茅斯会议正式确立了“人工智能”这一术语，被视为AI元年 [[2]]。在这一时期，自然语言处理（NLP）的研究主要遵循符号主义范式，即通过显式规则和逻辑来处理语言。

这一时期的标志性系统包括ELIZA和SHRDLU。ELIZA由Joseph Weizenbaum于1966年开发，被广泛认为是第一个“聊天机器人”或自然语言处理程序 [[3]][[4]][[5]]。其原始论文标题为《ELIZA—a computer program for the study of natural language communication between man and machine》，发表于《计算机协会通讯》[[6]][[7]][[8]]。ELIZA的核心技术是简单的模式匹配和替换方法，它通过模仿心理治疗师的对话方式，展现出惊人的对话能力，尽管其本质并无真正的理解 [[9]][[10]][[11]]。ELIZA的出现证明了即使是非常简陋的技术，也能产生令人信服的交互错觉，这为后续自然语言交互研究提供了重要启示。

紧随其后，Terry Winograd于1968年（或1970年）开发了SHRDLU系统 [[12]][[13]][[14]]。SHRDLU是一个更为先进的交互式自然语言理解系统，它能够理解和响应关于一个虚拟积木世界的命令 [[15]][[16]][[17]]。与ELIZA不同，SHRDLU内部具有一个明确的世界模型，能够进行推理和规划，代表了早期符号主义AI在特定领域内实现深度语言理解的巅峰。然而，这些系统高度依赖手工编写的规则和领域知识，难以扩展到开放域对话，其局限性最终促使研究者寻求更数据驱动的方法。

### **1.2 统计语言模型的奠基：从n-gram到概率建模**

随着计算能力的提升和语料库的积累，统计方法在1970-1990年代逐渐成为自然语言处理的主流。统计语言模型的核心思想是为语言中的词序列分配概率，用于预测下一个词或评估句子的合理性。

n-gram模型是统计语言模型的基石。其起源可追溯至信息论的早期工作。根据研究，第一个明确的n-gram语言模型由Fred Jelinek及其同事在IBM托马斯·J·沃森研究中心，以及James Baker在卡内基梅隆大学（CMU）于1970年代中期独立开发 [[18]][[19]][[20]]。Jelinek等人于1975年发表的论文是这一方向的关键里程碑，他们首次明确将“语言模型”定义为描述语言属性（如语法、语义、语篇）如何影响词序列概率的模型 [[21]]。这些工作深受Claude Shannon和Leonard Baum等人早期工作的影响 [[22]][[23]]。n-gram模型最早应用于语音识别领域，并在1976年由Jelinek提出相关应用 [[24]]。

IBM在1980年代创建了第一个统计语言模型，用于预测句子中的下一个词 [[25]]。这些模型基于马尔可夫假设，认为一个词的出现概率只与其前面的n-1个词相关。尽管简单，n-gram模型在语音识别、机器翻译等任务中取得了巨大成功，并奠定了现代语言建模的数学基础。

然而，n-gram模型面临严重的数据稀疏问题，且无法捕捉语言中的长程依赖关系。隐马尔可夫模型（HMM）和最大熵模型（MEM）在1980-1990年代也被广泛应用于序列标注等任务，作为统计NLP的重要组成部分 [[26]]。这些统计方法为后来神经网络语言模型的发展提供了问题框架和评估基准。

### **早期里程碑总结**：

**ELIZA (1966)**：Joseph Weizenbaum，第一个聊天机器人，模式匹配技术 [[27]][[28]]。

**SHRDLU (1968/1970)**：Terry Winograd，领域受限的自然语言理解系统 [[29]][[30]]。

**n-gram模型起源 (1975)**：Fred Jelinek等人，首次明确定义和应用统计语言模型 [[31]][[32]]。



## **2. 神经网络复兴与关键技术积累（1980s-2010s）**

### **2.1 循环神经网络的挑战与LSTM的突破**

在统计方法占据主流的同时，神经网络的研究也在稳步推进。循环神经网络（RNN）因其固有的序列处理能力，成为语言建模的天然候选。然而，传统RNN在训练中面临严重的梯度消失或梯度爆炸问题，导致无法有效学习长距离依赖关系。

这一关键瓶颈在1997年由Sepp Hochreiter和Jürgen Schmidhuber提出的长短期记忆网络（LSTM）所突破 [[33]][[34]][[35]]。其开创性论文题为《Long Short-Term Memory》，发表于1997年 [[36]][[37]][[38]]。LSTM通过引入门控机制（输入门、遗忘门、输出门），能够有选择地保留或遗忘信息，从而有效解决了长程依赖问题。LSTM在时间序列预测、语音识别、文本生成等任务中取得了长期的成功，是Transformer时代之前处理序列数据的核心技术 [[39]][[40]][[41]]。搜索结果指出，LSTM思想在1997年提出，是关键的序列模型 [[42]][[43]][[44]]。

尽管LSTM取得了成功，但它仍然具有RNN的固有局限性：序列化的处理方式限制了训练的并行化效率，且长程依赖的捕捉能力仍受限于模型容量。

### **2.2 词嵌入的革命：Word2Vec与分布式表示**

另一个具有深远影响的方向是词的表示学习。传统方法如独热编码存在维度灾难和语义鸿沟问题。2003年，Yoshua Bengio等人发表了《A neural probabilistic language model》论文，首次提出了神经概率语言模型，通过学习词的分布式表示来解决维度灾难和泛化问题 [[45]][[46]]。这项工作是现代词嵌入技术的先驱。

2013年，Tomas Mikolov等人发表的论文《Efficient Estimation of Word Representations in Vector Space》将词嵌入技术推向了实用化和普及化 [[47]][[48]]。Word2Vec提供了两种高效的训练架构（Skip-gram和CBOW），能够在大规模语料上快速学习高质量的词向量。词向量不仅能捕捉词汇间的语义相似性，还能编码类比关系（如“国王-男人+女人=女王”）。Word2Vec的成功证明了在海量无标注数据上学习通用语义表示的可行性，为后来的预训练语言模型开辟了道路。

### **2.3 深度学习三巨头的奠基性贡献**

现代大模型的发展离不开Geoffrey Hinton、Yann LeCun和Yoshua Bengio三位科学家的奠基性工作，他们因此获得了2018年的图灵奖 [[49]][[50]][[51]]。

**Geoffrey Hinton**被称为“深度学习之父”，其贡献贯穿神经网络研究的多个时期。1986年，他与合作者发表了《Learning Internal Representations by Error Propagation》论文，系统阐述了反向传播算法，为深度神经网络的训练提供了核心技术 [[52]][[53]]。2006年，他提出了深度信念网络（DBN）和逐层预训练方法，为训练深层网络提供了可行路径，引发了深度学习的复兴 [[54]]。2015年，他与Yann LeCun、Yoshua Bengio共同在《自然》杂志发表了综述文章《Deep Learning》，系统阐述了深度学习的基本原理和应用前景 [[55]][[56]]。值得注意的是，Hinton也是2017年《Attention Is All You Need》论文的作者之一，该论文提出了Transformer架构 [[57]][[58]][[59]]。

**Yann LeCun**是卷积神经网络（CNN）的主要推动者。他在1980-1990年代发展了卷积网络的理论和实践，并将其成功应用于手写数字识别（LeNet-5），奠定了CNN在计算机视觉领域的基础 [[60]]。CNN的思想（局部连接、权重共享、池化）也对序列建模产生了影响，例如一维卷积用于文本分类。

**Yoshua Bengio**在序列建模和生成模型方面做出了杰出贡献。除了前述的神经概率语言模型（2003），他还在2006年提出了《Greedy layer-wise training of deep networks》 [[61]]，与Hinton的工作共同推动了深度学习热潮。他在循环神经网络、注意力机制等方面也有重要研究。

这三位科学家的共同点在于，他们在神经网络被视为“死胡同”的时期坚持研究，并在2006年前后共同推动了深度学习的复兴，其工作为后来大模型所需的深度网络训练、分布式表示学习和序列建模能力奠定了坚实基础 [[62]][[63]]。

### **技术积累期里程碑总结**：

**LSTM (1997)**：Sepp Hochreiter & Jürgen Schmidhuber，解决长程依赖问题 [[64]][[65]]。

**神经概率语言模型 (2003)**：Yoshua Bengio等人，词分布式表示的先驱 [[66]]。

**Word2Vec (2013)**：Tomas Mikolov等人，高效词嵌入，大规模预训练的雏形 [[67]][[68]]。

**反向传播 (1986)**：Geoffrey Hinton等人，深度网络训练的核心算法 [[69]][[70]]。



## **3. 架构革命：Transformer的诞生与影响（2017）**

### **3.1 “Attention Is All You Need”：范式转移的起点**

2017年，**Ashish Vaswani等人发表的论文《Attention Is All You Need》**标志着自然语言处理领域的一个根本性转折点 [[71]][[72]][[73]]。这篇论文提出的Transformer架构完全摒弃了此前在序列建模中占主导地位的循环和卷积结构，仅依赖注意力机制来建模序列内部的长距离依赖关系 [[74]][[75]][[76]]。

Transformer的核心创新是自注意力机制。与RNN按顺序处理输入不同，自注意力机制允许模型在处理每个位置时，直接“看到”并加权整合序列中所有其他位置的信息 [[77]][[78]][[79]]。这种机制具有两大优势：首先，它天然地建模长距离依赖，距离不再是问题；其次，序列中所有位置的计算可以并行进行，极大地提高了训练效率 [[80]][[81]][[82]]。搜索结果明确指出，自注意力机制“解决了传统循环神经网络（RNN）和长短期记忆网络（LSTM）在处理长距离依赖关系时的困难，以及梯度消失/爆炸问题” [[83]][[84]][[85]]。

Transformer由编码器和解码器两部分组成。编码器将输入序列映射为一系列连续表示；解码器则根据编码器的输出和已生成的输出，自回归地生成目标序列。这种结构为后续的预训练语言模型提供了灵活的架构基础。

### **3.2 从RNN/CNN到Transformer的演变逻辑**

理解Transformer的革命性，需要将其置于RNN和CNN的演变脉络中。RNN（包括LSTM）的主要问题在于其序列化处理方式：每个时间步的计算必须等待前一个时间步完成，导致无法有效并行化，且长程信息在传递中逐渐衰减 [[86]][[87]][[88]]。CNN虽然支持并行计算，但在捕捉长距离依赖时需要堆叠多层，且感受野大小受限于卷积核大小和层数 [[89]][[90]][[91]]。

Transformer通过自注意力机制，在一步计算中即可建立序列中任意两个位置之间的直接连接，感受野覆盖整个序列，彻底打破了距离的限制 [[92]][[93]][[94]]。同时，由于所有位置的注意力权重可以同时计算，Transformer在GPU上实现了高度并行化，使得训练大规模模型成为可能。搜索结果总结道：“Transformer架构完全摒弃了传统的循环和卷积结构，完全依赖自注意力机制” [[95]][[96]][[97]]。

这种架构变革带来的影响是深远的。首先，它使得模型可以轻松扩展到前所未有的规模（参数量从数亿到数千亿），而训练时间仍在可接受范围内。其次，大规模模型展现出了惊人的涌现能力，这在小模型上从未出现过。Transformer因此成为所有现代大语言模型的基石架构。

### **架构革命里程碑**：

**Transformer (2017)**：Ashish Vaswani等人，《Attention Is All You Need》，自注意力机制，并行计算，长程依赖建模 [[98]][[99]][[100]]。



## **4. 预训练范式的兴起：GPT与BERT的分野（2018-2019）**

### **4.1 GPT系列：自回归预训练的探索**

在Transformer提出后不久，两个相互竞争又相互补充的预训练范式迅速出现。2018年，OpenAI的Alec Radford等人发表了论文《Improving Language Understanding by Generative Pre-training》（即GPT-1） [[101]][[102]][[103]]。GPT-1的核心思想是使用Transformer解码器结构，在大规模未标注文本上进行生成式预训练，然后在下游任务上进行微调。

GPT-1证明了生成式预训练能够学习到丰富的语言知识，并在多项自然语言理解任务上取得了当时最佳的结果。其工作流程是：首先，在大型文本语料库上训练一个语言模型（预测下一个词）；然后，在目标任务上通过微调进行调整。

2019年，Radford等人又提出了GPT-2，论文题为《Language models are unsupervised multitask learners》 [[104]][[105]][[106]]。GPT-2大幅增加了模型规模（参数量从1.17亿增至15亿），并展示了零样本学习的惊人能力：模型无需微调，仅通过提示就能完成翻译、摘要、问答等多种任务。GPT-2暗示了语言模型在足够大规模下可能涌现出通用任务解决能力。

GPT系列的代表作为GPT-3，由Tom Brown等人于2020年发表，论文题为《Language Models are Few-Shot Learners》 [[107]][[108]][[109]]。GPT-3将参数量提升到1750亿，并系统展示了大模型的少样本学习能力：通过提供少量示例（few-shot），模型就能适应新任务，无需更新参数。GPT-3的能力范围远超预期，包括生成、编程、创作等，成为后续ChatGPT的直接前身 [[110]][[111]]。

### **4.2 BERT：双向编码的深度理解**

几乎与GPT-1同时，Google的Jacob Devlin等人于2018年提出了BERT，论文题为《BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding》 [[112]][[113]][[114]]。BERT采用了与GPT不同的路径：使用Transformer编码器结构，并通过掩码语言模型（MLM）实现双向预训练。

BERT的预训练包含两个任务：掩码语言模型（随机遮盖输入中的词，让模型预测）和下一句预测（NSP，判断两个句子是否连续）。这使得BERT能够深度理解上下文中的双向关系，而非像GPT那样只能从左到右生成。

BERT一经提出，就在11项自然语言理解任务上刷新了最佳记录，迅速成为NLP领域的新范式。其“预训练+微调”的流程被广泛采用：先在大规模语料上预训练一个通用模型，然后在具体任务上用少量标注数据进行微调。Devlin因此成为预训练语言模型的关键人物之一 [[115]][[116]][[117]]。

### **4.3 两种范式的比较与融合**

GPT（生成式）和BERT（理解式）代表了基于Transformer的两种预训练范式。GPT使用单向注意力（从左到右），天然适合生成任务；BERT使用双向注意力，更适合理解任务。两者都是大规模预训练的成功实践，证明了在海量数据上学习通用表示的有效性。

这两种范式也催生了后续许多模型：RoBERTa（对BERT预训练策略的优化）、T5（Raffel等人，2019，将所有NLP任务统一为文本到文本格式）、PaLM（Chowdhery等人，2022，谷歌的大规模语言模型）等 [[118]][[119]][[120]]。其中，T5的论文《T5: Exploring the limits of transfer learning with a unified text-to-text transformer》提出将所有NLP任务建模为文本到文本转换，为统一建模提供了新思路 [[121]][[122]][[123]]。

### **预训练范式里程碑**：

**GPT-1 (2018)**：Alec Radford等人，生成式预训练，Transformer解码器 [[124]][[125]][[126]]。

**BERT (2018)**：Jacob Devlin等人，双向编码预训练，Transformer编码器 [[127]][[128]][[129]]。

**GPT-2 (2019)**：零样本学习能力的展示 [[130]][[131]][[132]]。

**GPT-3 (2020)**：Tom Brown等人，少样本学习，大规模涌现能力 [[133]][[134]][[135]]。

**T5 (2019)**：Raffel等人，统一的文本到文本框架 [[136]][[137]][[138]]。

## **5. 对齐工程与智能涌现：RLHF与ChatGPT（2022-）**

### **5.1 RLHF：从能力到意图的对齐**

随着GPT-3等模型展现出强大能力，一个新的问题凸显出来：如何让模型的行为更符合人类的意图和价值观？模型可能在能力上很强，但输出的内容可能有害、偏颇或不合用户期望。这催生了“对齐”问题。

OpenAI在2017年的论文《Deep Reinforcement Learning from Human Preferences》中首次提出了从人类偏好中进行强化学习的概念 [[139]][[140]]。但将这一思想成功应用于大型语言模型的是2022年的InstructGPT工作，由Long Ouyang等人完成，论文题为《Training Language Models to Follow Instructions with Human Feedback》 [[141]][[142]][[143]]。

InstructGPT引入了三阶段训练流程：

1.**监督微调（SFT）**：用人类编写的指令-回复示例微调预训练模型。

2.**奖励模型（RM）训练**：用人类对模型输出的排序数据训练一个奖励模型，该模型能预测人类偏好。

3.**强化学习（PPO）**：使用奖励模型作为奖励信号，通过近端策略优化（PPO）算法进一步调整语言模型。

这一RLHF（Reinforcement Learning from Human Feedback）流程显著提高了模型遵循指令的能力，减少了有害输出，并使模型输出更符合人类偏好。InstructGPT论文明确指出，它是“将RLHF应用于大型语言模型以进行指令遵循的开创性工作” [[144]][[145]][[146]]。RLHF成为连接强大基础模型与实用、安全AI系统的关键技术桥梁。

### **5.2 ChatGPT与社会影响**

2022年底，OpenAI发布了基于GPT-3.5和RLHF技术的ChatGPT。ChatGPT迅速风靡全球，引发了公众对大语言模型前所未有的关注。它展示出的对话能力、知识问答、文本创作、代码生成等能力，让普通用户直观感受到AI的潜力。

ChatGPT的成功可以归因于两个因素的结合：一是大规模预训练模型（GPT系列）积累的强大底层能力；二是RLHF技术带来的出色交互体验和对齐效果。它不仅是技术突破，也是产品设计和工程集成的成功。

### **5.3 竞争与多样化：Claude等模型的出现**

ChatGPT的成功引发了科技公司的激烈竞争。Anthropic公司由OpenAI前研究副总裁Dario Amodei等人于2021年创立 [[147]]，并于2023年3月发布了Claude模型 [[148]]。Claude以信息论先驱Claude Shannon命名 [[149]]，强调安全、对齐、推理和代理任务能力 [[150]][[151]]。

Anthropic在RLHF的基础上，发展了“宪法AI”等对齐方法，试图构建更安全、更透明的AI系统。Claude系列模型（如Claude 2、Claude 3）在长上下文、推理能力等方面不断迭代，与GPT系列形成竞争格局。

谷歌也推出了PaLM（Pathways Language Model，2022年，Chowdhery等人） [[152]][[153]]和Gemini系列模型。Meta发布了LLaMA系列开源模型，促进了开源大模型生态的发展。大模型领域呈现百花齐放的态势。

### **对齐工程与涌现里程碑**：

**RLHF概念起源 (2017)**：OpenAI，《Deep Reinforcement Learning from Human Preferences》 [[154]][[155]]。

**InstructGPT (2022)**：Long Ouyang等人，RLHF成功应用于LLM指令遵循 [[156]][[157]][[158]]。

**ChatGPT (2022)**：产品发布，RLHF与大规模预训练的结合，引发全球关注。

**Claude (2023)**：Anthropic发布，强调安全与对齐 [[159]][[160]]。

**PaLM (2022)**：Chowdhery等人，谷歌的大规模语言模型 [[161]][[162]]。



## **6. 技术演进的内在逻辑与关系**

### **6.1 从序列建模到并行架构的演变**

大模型技术演进的核心逻辑之一，是解决序列数据建模中的计算效率和表示能力问题。早期RNN和LSTM模型采用序列化计算，虽然理论上能处理变长序列，但训练无法并行化，效率低下，且长程依赖问题难以根本解决 [[163]][[164]][[165]]。

Transformer的自注意力机制实现了范式转移：从“顺序处理”到“并行关系建模”。它通过让每个位置直接关注所有位置，在一步计算中捕获全局依赖，并将计算复杂度从序列长度的线性转变为二次，但换取了高度并行化 [[166]][[167]][[168]]。这种权衡在GPU算力高速发展的背景下极为有利，使得训练数十亿乃至数千亿参数的模型成为可能。

### **6.2 从任务特定模型到通用基础模型**

另一个清晰的演进脉络是从“任务特定模型”到“通用基础模型”。早期NLP系统（如ELIZA、SHRDLU）需要为特定任务手工设计规则和知识。统计方法时代，每个任务（如情感分析、机器翻译、命名实体识别）通常需要独立的模型和特征工程。

预训练语言模型的出现改变了这一局面。GPT和BERT证明了在一个大规模模型上学习通用语言表示，然后通过微调适应多种任务，是可行且高效的范式。GPT-3和InstructGPT更进一步，展示了大规模模型可以通过提示或少量示例，在无需参数更新情况下完成广泛任务，展现出“通用问题求解器”的雏形。

这种“基础模型”范式的成熟，与大模型规模化带来的“涌现能力”密切相关。研究发现，当模型规模超过一定阈值时，会突然展现出小模型所不具备的能力，如上下文学习、思维链推理等。涌现现象的出现，使得规模扩展本身成为一种有效的“技术路线”。

### **6.3 预训练、微调与对齐的三阶段流程**

现代大语言模型的开发已形成相对标准的三阶段流程，这三个阶段分别对应着不同技术的发展和融合：

**第一阶段：预训练**

预训练阶段的目标是让模型学习语言的统计规律和世界知识。这一阶段依赖于：

- Transformer架构提供的高效并行训练能力 [[169]][[170]][[171]]。

- 海量文本数据的可及性。

- 计算硬件（特别是GPU/TPU）的算力提升。

- 自监督学习目标（如掩码语言模型、下一词预测）。

预训练产生的模型称为“基础模型”，它已具备强大的语言理解和生成能力，但尚未精确对齐人类意图。

**第二阶段：微调**

微调阶段在特定任务或领域数据上调整预训练模型，使其专精于特定能力。技术包括：

- 监督微调（SFT），使用标注数据调整模型参数 [[172]][[173]][[174]]。

- 指令微调，使用指令-回复格式的混合任务数据，提升模型的指令遵循能力。

- 领域自适应微调，在专业领域（如医疗、法律）数据上调整。

**第三阶段：对齐**

对齐阶段解决的核心问题是：如何让模型的行为更符合人类意图、价值观和安全要求。主要技术是RLHF及其变体：

- 收集人类对模型输出的偏好排序数据。

- 训练奖励模型预测人类偏好。

- 使用强化学习算法（如PPO）优化语言模型策略 [[175]][[176]][[177]]。

这三阶段流程并非严格线性，实践中可能迭代进行。例如，ChatGPT就是GPT基础模型经过RLHF对齐后的产品。

## **7. 关键人物与贡献**

大模型的发展是集体智慧的结晶，但一些关键人物做出了决定性贡献。以下基于搜索结果梳理关键人物及其代表作：

### **Geoffrey Hinton**

深度学习的先驱，被称为“深度学习之父”。

1986年，反向传播算法论文《Learning Internal Representations by Error Propagation》 [[178]][[179]]。

2006年，深度信念网络论文《Deep Boltzmann Machines》 [[180]]。

2015年，与LeCun、Bengio合著《Deep Learning》综述 [[181]][[182]]。

2017年，Transformer论文《Attention Is All You Need》作者之一 [[183]][[184]][[185]]。

2018年图灵奖得主 [[186]][[187]][[188]]。

### **Yann LeCun**

卷积神经网络的奠基人。

2018年图灵奖得主 [[189]][[190]][[191]]。

推动了CNN在计算机视觉领域的应用，其思想影响了序列建模。

### **Yoshua Bengio**

序列建模和生成模型专家。

2003年，神经概率语言模型论文《A neural probabilistic language model》 [[192]][[193]]。

2006年，深度网络训练论文《Greedy layer-wise training of deep networks》 [[194]]。

2015年，与Hinton、LeCun合著《Deep Learning》综述 [[195]]。

2018年图灵奖得主。

### **Ashish Vaswani**

Transformer架构的共同发明人。

2017年，论文《Attention Is All You Need》第一作者 [[196]][[197]][[198]]。

### **Jacob Devlin**

BERT模型的提出者。

2018年，论文《BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding》 [[199]][[200]][[201]]。

### **Alec Radford**

GPT系列模型的共同开发者。

2018年，GPT-1论文《Improving Language Understanding by Generative Pre-training》 [[202]][[203]][[204]]。

2019年，GPT-2论文《Language models are unsupervised multitask learners》 [[205]]。

### **Tom Brown**

GPT-3论文的第一作者。

2020年，论文《Language Models are Few-Shot Learners》 [[206]][[207]][[208]]。

### **Ilya Sutskever**

深度学习和大型语言模型领域的关键人物。

与Hinton、Krizhevsky共同发表AlexNet论文（2012年），推动深度学习复兴 [[209]][[210]]。

OpenAI联合创始人及首席科学家，推动GPT系列发展。

### **Long Ouyang**

InstructGPT论文的主要作者之一。

2022年，论文《Training Language Models to Follow Instructions with Human Feedback》，将RLHF成功应用于LLM [[211]][[212]][[213]]。

### **Tomas Mikolov**

Word2Vec的主要开发者。

2013年，论文《Efficient Estimation of Word Representations in Vector Space》 [[214]][[215]]。

### **Sepp Hochreiter & Jürgen Schmidhuber**

LSTM的共同发明人。

1997年，论文《Long Short-Term Memory》 [[216]][[217]][[218]]。

## **8. 各种技术之间的关系图谱**

大模型技术生态由多个相互关联的技术维度构成，它们之间存在清晰的演进和依赖关系：

```shell
词嵌入
  ↓ 改进表示学习，提供预训练思想雏形
序列模型（RNN/LSTM）
  ↓ 解决长程依赖，但训练效率低
注意力机制
  ↓ 增强长程依赖建模
Transformer架构
  ↓ 提供并行训练基础，成为大模型基石
  ┌───────────┴─────────┐
编码器路径          解码器路径
(BERT等)          (GPT等)
  ↓                ↓
理解型任务       生成型任务
  └─────┬────────┘
   预训练+微调范式
      ↓
   大规模涌现能力
      ↓
   对齐问题凸显
      ↓
    RLHF技术
    ↓      ↓
ChatGPT  Claude等应用
```



**横向依赖**：Transformer的成功依赖于早期词嵌入的思想（分布式表示）、LSTM对序列建模的探索、以及注意力机制的初步引入。

**纵向演进**：从架构到训练范式：Transformer解决了架构效率问题 → 预训练范式解决了知识获取问题 → RLHF解决了意图对齐问题。

**范式融合**：当前SOTA模型多为多种技术的融合体。例如，ChatGPT = Transformer解码器 + 大规模预训练 + RLHF对齐。

**多模态扩展**：基础模型范式正从文本扩展到图像、音频、视频等多模态领域，Transformer及其变体（如ViT）成为跨模态的统一架构。

## **9. 历史规律与未来展望**

### **9.1 发展历史的核心规律**

回顾大模型七十余年的发展历程，可以总结出几条核心规律：

**规律一：范式革命驱动质变**

大模型的发展并非匀速进步，而是由若干范式革命推动的阶跃式发展。从符号规则到统计方法，从统计方法到神经网络，从RNN/LSTM到Transformer，每一次范式革命都开启了新的可能性空间。Transformer的出现尤为关键，它直接催生了预训练语言模型和规模扩展两大技术路线，是当前大模型时代的起点。

**规律二：规模扩展带来涌现**

GPT-3等一系列模型证明，在特定架构下，单纯扩展模型规模（参数量、数据量、计算量）能够带来意想不到的能力涌现。这种“规模即规律”的发现，改变了AI研究的方向，使得算力、数据和工程效率成为与算法创新同等重要的竞争力。

**规律三：工程与科学的深度融合**

大模型是典型的工程驱动型科学领域。GPT-3论文有三十多位作者 [[219]]，涵盖了工程、算法、数据等多个方面，表明大模型开发已是一个系统工程。从数据清洗、分布式训练框架、到推理优化，工程能力直接决定了模型能否成功训练和部署。

**规律四：开源与闭源生态并存**

以LLaMA为代表的开源模型与以GPT-4为代表的闭源模型形成了互补生态。开源模型促进了学术研究和应用创新，闭源模型则代表了商业前沿能力。这种双生态格局可能长期存在。

### **9.2 未来发展方向**

基于历史脉络和当前趋势，大模型可能朝以下方向演进：

**方向一：架构创新**

尽管Transformer占主导，但其二次复杂度对长序列处理不利。注意力机制的改进（如线性注意力、状态空间模型）、混合专家模型、以及新型架构可能带来效率提升。

**方向二：多模态融合**

当前模型正从纯文本扩展到图像、音频、视频等多模态。能够理解并生成多种模态内容的统一大模型是明确趋势。

**方向三：推理与规划**

现有大模型在复杂推理、规划、决策等能力上仍有不足。结合思维链、搜索算法、工具使用等技术，提升模型的高阶认知能力是关键方向。

**方向四：对齐与安全**

随着模型能力增强，对齐问题愈发重要。除RLHF外，可解释性研究、可控生成、红队测试、宪法AI等方法正在发展，以构建更安全、更透明的AI系统。

**方向五：效率与普及**

训练和部署大模型成本高昂。模型压缩、知识蒸馏、高效推理、边缘部署等技术将使大模型更普及、更可持续。

**方向六：智能体与自主系统**

大模型作为“大脑”，与外部工具、数据库、API结合，形成能够自主规划、执行、反思的智能体，是当前前沿探索方向。

## **10. 结论**

大语言模型的技术发展历程，是一部从简单规则到统计学习，从浅层模型到深度网络，从任务特定系统到通用基础模型的宏大史诗。它的起点可追溯至1950年代图灵的哲学追问和ELIZA的初步尝试，经历了符号主义的起伏、统计方法的成熟，并在深度学习复兴时代汲取了反向传播、词嵌入、循环网络等关键技术养分。

2017年Transformer架构的诞生是一个划时代的事件，它提供了能够支撑规模化扩展的高效架构基础。基于此，GPT系列和BERT分别开创了自回归和自编码两种预训练范式，证明了大规模预训练的有效性。GPT-3展示了规模扩展带来的涌现能力，而InstructGPT则通过RLHF技术解决了模型与人类意图对齐的问题，直接催生了ChatGPT的现象级成功。

这一历程的关键人物包括：深度学习三巨头Hinton、LeCun、Bengio奠定了理论基础；Vaswani等人提出的Transformer开启了新时代；Devlin、Radford、Brown等人推动了预训练模型的发展；Ouyang等人通过RLHF实现了对齐突破。他们的贡献交织成网，共同推动了大模型从学术概念走向社会现实。

各种技术之间不是孤立的，而是存在深刻的演进和依赖关系：词嵌入改进了表示学习，LSTM探索了序列建模，注意力机制增强了长程依赖捕捉，而Transformer将这些思想整合并革命性突破了并行化瓶颈。在此基础上，预训练范式解决了知识获取问题，RLHF解决了对齐问题，形成了“架构-预训练-对齐”的技术链条。

展望未来，大模型将继续在架构效率、多模态融合、推理能力、对齐安全等方向演进，并更深入地与物理世界和人类工作流结合，向通用人工智能的方向迈进。理解这一历史进程，对于把握技术趋势、制定发展策略、应对社会影响都具有重要意义。大模型的故事远未结束，我们正处于一个激动人心的变革时代的中段。

## **11. 文献来源**

[[18,37,38,45,58,61,91\]. Attention is All you Need](https://arxiv.org/abs/1706.03762)

[[22,35,36,44,65,83\]. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://doi.org/10.18653/v1/N19-1423)

[[33,34,43,64,82\]. Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165)

[[46\]. PaLM 2 Technical Report](https://arxiv.org/abs/2305.10403)

[[66\]. Language Models are Unsupervised Multitask Learners](https://www.semanticscholar.org/search?q=Language Models are Unsupervised Multitask Learners&sort=relevance)

[[67,85\]. Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer](https://arxiv.org/abs/1910.10683)

[[115,121,124,203,206,212,215,218,221,224,227,230,233,236,239,581,584,587,598,601,604,610,613,616,632,641,682,685,688\]. LLaMA: Open and Efficient Foundation Language Models](https://arxiv.org/abs/2302.13971)

[[125\]. Large Language Models as Master Key: Unlocking the Secrets of Materials Science with GPT](https://doi.org/10.48550/arXiv.2304.02213)

[[138,533,550,659\]. Large Language Models: A Survey](https://doi.org/10.48550/arXiv.2402.06196)

[[144,155,536,662,675\]. Recent Advances in Generative AI and Large Language Models: Current Status, Challenges, and Perspectives](https://doi.org/10.1109/TAI.2024.3444742)

[[161,163,166,596,678\]. A Survey of Large Language Models](https://arxiv.org/abs/2303.18223)

[[164,167,597\]. Think Outside the Code: Brainstorming Boosts Large Language Models in Code Generation](https://doi.org/10.48550/arXiv.2305.10679)

[[168,170,590,686\]. Large language models for generative information extraction: a survey](https://doi.org/10.1007/s11704-024-40555-y)

[[198\]. Transformers in Vision: A Survey](https://doi.org/10.1145/3505244)

[[310,315,321,325,327,395,412,415,652\]. LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)

*以下来源未被直接引用*

[GPT-4 Technical Report](https://arxiv.org/abs/2303.08774)

[Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361)

[Dated Data: Tracing Knowledge Cutoffs in Large Language Models](https://doi.org/10.48550/arXiv.2403.12958)

[ToolComp: A Multi-Tool Reasoning & Process Supervision Benchmark](https://doi.org/10.48550/arXiv.2501.01290)

[Large Language Models](https://doi.org/10.1145/3606337)

[Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155)

[ChatGLM-RLHF: Practices of Aligning Large Language Models with Human Feedback](https://doi.org/10.48550/arXiv.2404.00934)

[Embodied Spatial Intelligence: from Implicit Scene Modeling to Spatial Reasoning](https://arxiv.org/abs/2509.00465)

## **12. 其他来源**

[[1,5,10,13,14,15,522\]. Fine-Tuning of Large Language Models (LLMs)](https://www.ijies.net/finial-docs/finial-pdf/2206249513.pdf)

[[2,4,27\]. An Exhaustive Analysis Of Large Language Models](https://nano-ntp.com/index.php/nano/article/download/5458/4370/10687)

[[3,8,17,28\]. From Past to Present: A Survey of Malicious URL Detection Techniques, Datasets and Code Repositories](https://www.arxiv.org/pdf/2504.16449)

[[6,11\]. Bridging the Data Gaps to Democratize AI in Science, Education and Society](https://2024.euro-par.org/fileadmin/2024/files/Altintas-Keynote-EuroPar-30August2024.pdf)

[[7,12\]. Towards Small Large Language Models](https://orbi.uliege.be/bitstream/2268/318779/1/Nelie_Poster (1).pdf)

[[9\]. LLMs4All: A Review of Large Language Models Across Academic Disciplines](https://www.preprints.org/frontend/manuscript/e9a781ac7e8f0b59a3b6f70e7407654c/download_pub)

[[16,20,24,26,30\]. When Experimental Economics Meets Large Language Models: Tactics with Evidence](https://arxiv.org/pdf/2505.21371)

[[19,23,29\]. Introduction to Generative AI and Large Language Models (LLMs)](https://www.vanhansewijck.com/assets/files/intro-slides-pt1-dfdce96450c877f70190d0835ff5239c.pdf)

[[21,25,31\]. Improving Large Language Models in Repository Level Programming through Self-Alignment and Retrieval-Augmented Generation](https://edoc.sub.uni-hamburg.de/informatik/volltexte/2024/275/pdf/MA_final.pdf)

[[32\]. DeepSeek大模型及其企业应用实践](https://files.metaso.cn/api/public-file/preview?fileName=8673664289745682432.pdf)

[[39,50,481,482\]. 大模型浪潮商业机遇、产业变革与未来趋势](https://files.metaso.cn/api/public-file/preview?fileName=8692489343423995904.pdf)

[[40\]. 大小微模型赋能先进制造：实践与思考](https://files.metaso.cn/api/public-file/preview?fileName=8714925146142662656.pdf)

[[41\]. GLOBALinks 115 NEWSLETTER SEP. 2024 ISSUE.](https://file.mitacsynnex.com/catalog/globalink_NO.115.pdf)

[[42,699\]. 美国工程院外籍院士张宏江：AI大爆炸至少将持续十年](https://finance.sina.cn/tech/2023-07-06/detail-imyztiiu8826681.d.html?from=wap)

[[47\]. 蚂蚁集团开源理解与生成统一多模态大模型Ming-lite-omni](https://news.qq.com/rain/a/20250527A09K5500)

[[48\]. 大规模语言模型：从理论到实践（第2版）](https://mp.weixin.qq.com/s?__biz=MjM5OTEzMjg3Mw==&mid=2653901049&idx=2&sn=19221fe88236a1843ddf068155ad78e2&chksm=bcd83958164d79f6c058effbf46d27ac765379741f7ee6efbc5d1c251c860b1f68fb7318a838&scene=27)

[[49\]. 大模型的前世今生：技术、挑战与未来](https://mp.weixin.qq.com/s?__biz=MzA5OTEwNzg3OQ==&mid=2650400577&idx=1&sn=0dfeaca6f375423c321030455d22da8d&chksm=89cdf71dd3d334808651773eea9d0fec9622382ba699ac04d7489498ccc88f4306d2d297ddc4&scene=27)

[[51\]. AIGC重构应用开发 智能化新格局](https://files.metaso.cn/api/public-file/preview?fileName=8677605896568754176.pdf)

[[52,55,70,76,88,566,643\]. 深入解析：大模型的几大阶段演变过程（更多的数据、更大的模型规模（参数）、更先进的架构)](https://www.cnblogs.com/lxjshuju/p/19130674)

[[53,56,77,89,567,644\]. 大模型RNN](https://blog.csdn.net/mayaohao/article/details/148437935)

[[54\]. 2024年中国人工智能产业研究报告](https://files.metaso.cn/api/public-file/preview?fileName=8692381569416527872.pdf)

[[57,78,81,90,568,645\]. 大模型核心技术解析](https://blog.csdn.net/2401_84205765/article/details/143359528)

[[59,62,73,79,92\]. 《大模型时代-ChatGPT开启通用人工智能浪潮》精华摘抄-腾讯云开发者社区-腾讯云](https://cloud.tencent.com/developer/article/2452145?policyId=1003)

[[60,63,80,94\]. 大模型：从‘大’到‘跃迁’的核心逻辑](https://www.woshipm.com/ai/6149286.html)

[[68,74,86,96\]. 火爆的大模型背后，有哪些的核心技术！](https://blog.csdn.net/weixin_49895216/article/details/142355173)

[[69,75,87,93,95,97\]. 今天我们一同来探讨一下那些大模型背后的核心技术！](https://mp.weixin.qq.com/s?__biz=MzI1MjQ2OTQ3Ng==&mid=2247643924&idx=1&sn=53b8be044d3419b7576762e61a20da78&chksm=e9efba9fde9833891f0abf7afd1ba10c404fb4a2e2028fa621722998a225834708bbace3741b&scene=27)

[[71\]. 人工智能带动 5G 爆发，自主可控迫在眉睫](https://fiatas.com/temp/whitepaper/行业趋势分析报告/2023 通信行业深度研究：人工智能带动5G爆发，自主可控迫在眉睫.pdf)

[[72\]. 生成式人工智能赋能智慧司法及相关思考](https://files.metaso.cn/api/public-file/preview?fileName=8692383160196763648.pdf)

[[84\]. Transformer 与大语言模型的技术发展与应用综述](https://paper.medpeer.cn/static/file/tmp/export/30457_2024-12-252186/Transformer与_original_76992.docx)

[[98,107,118,122,200,207,213,216,219,551,578,585,588,611,614\]. 大模型涉及到的比较经典的论文](https://www.cnblogs.com/wanghengbin/p/17924667.html)

[[99,103,143,158,251,278,287,302,304,539,665\]. Introduction to Large Language Models](https://web.stanford.edu/class/cs124/lec/LLM2024.pdf)

[[100,106,114,594,609,681\]. Recent Advances in Large Language Models: An Upshot](https://ijrpr.com/uploads/V5ISSUE6/IJRPR29621.pdf)

[[101,108,119,123,202,553,580\]. 大模型发展关键里程碑](https://blog.csdn.net/2401_87723776/article/details/146281711)

[[102,109,120,217,586,612\]. 第一讲 - 文本分析与数据挖掘概论](https://zhangjianzhang.github.io/text_mining/files/slides/lecture_1.pdf)

[[104,110,112,592,607,679\]. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://files.metaso.cn/api/public-file/preview?fileName=8673664287292014592.pdf)

[[105,111,113,593,608,680\]. BERT, or Bidirectional Encoder Representations from Transformers](https://github.com/Aloha0424/bert)

[[116,127,162,165,208,209,214,280,282,289,291,293,295,582,595,605,683\]. A Comprehensive Overview of Large Language Models (LLMs)](https://www.ijfmr.com/papers/2025/1/34609.pdf)

[[117,223,226,583,606,684\]. Tokenization and Word2Vec](https://www.ee.cityu.edu.hk/~lmpo/ee4016/pdf/2024A_AI_L05A_Word2Vec.pdf)

[[126,210\]. IMN Internationale Mathematische Nachrichten Nr. 254 Dezember 2023 Österreichische Mathematische Gesellschaft Large Language Models for Mathematicians](https://risc.jku.at/wp-content/uploads/2024/01/OeMG_Mitteilungen_Dez_2023.pdf)

[[128,130,132,523\]. Demystifying Large Language Models and GPT](https://www.iiwas.org/downloads/ABC-GPT-iiWAS2023.pdf)

[[129,131,133,211,225,229,238,240,524,600,633,642\]. Artificial Intelligence for Improved Patient Outcomes—The Pragmatic Randomized Controlled Trial Is the Secret Sauce](https://www.kjronline.org/src/PDFs/kjr-v25n2.pdf)

[[134,145,151,242,245,266,269,542\]. The Evolution and Impact of Large Language Model Systems: A Comprehensive Analysis](https://alochana.org/wp-content/uploads/10-AJ2169.pdf)

[[135,149,173,175,284,300,690\]. Genius Makers](https://files.metaso.cn/api/public-file/preview?fileName=8684524982233219072.pdf)

[[136,147,150,243,256,267,543\]. Brief History of AI and ChatGPT](http://www.aiotlab.org/teaching/dl_app/slides/1_AI_history.pdf)

[[137,139,140,141,246,248,249,276,285,532,534,535,537,549,658,660,661,663\]. Jailbreaking Large Language Models Against Moderation Guardrails via Cipher Characters](https://nips.cc/media/neurips-2024/Slides/96243_YGqWxyx.pdf)

[[142,538,664\]. STA303: Artificial Intelligence Introduction](https://fangkongx.github.io/Teaching/STA303/Fall2025/Lecture 1 - intro.pdf)

[[146\]. 大型语言模型领域50位关键意见领袖（KOL）盘点](https://earlmind.com/50-ai-kol-by-openai-deepresearch/)

[[148,152\]. Yoshua Bengio - C.V.](https://yoshuabengio.org/wp-content/uploads/2021/08/CV_Yoshua_Bengio_07-21-2021.pdf)

[[153,154,525,541,546,672,674\]. Foundations of Large Language Models](https://www.neurohackingly.com/content/files/2025/05/Foundations-of-Large-Language-Models-by-Tong-Xiao-and-Jingbo-Zhu.pdf)

[[156,159,676\]. Large Language Models: Introduction and Recent Advances](https://lcs2-iitd.github.io/ELL881-AIL821-2401/static_files/presentations/1.pdf)

[[157,160,677\]. History, Development, and Principles of Large Language Models—An Introductory Survey](https://arxiv.org/pdf/2402.06853)

[[169,171,172,174,591,687\]. A survey on large language models](https://dl.acm.org/doi/10.1145/3654674)

[[176,179,186,305,311,312,391,396,398,555,557,563,569,572,576,646\]. DeepSeek: Paradigm Shifts and Technical Evolution in Large AI Models](https://www.sciengine.com/doi/pdfView/01B0580106E74A6B8840ED08D68111B5)

[[177,180,183,187,189,556,558,561,564,577,650\]. Large language models and large concept models in radiology: Present challenges, future directions, and critical perspectives](https://www.f6publishing.com/forms/main/DownLoadFile.aspx?Type=Digital&TypeId=22&id=10.4329%2Fwjr.v17.i11.114754&FilePath=8B896BF1236799B3E300C6F9A32C392F9E923F175DACDE58263D37FCC80CE5E1C240E3A65161892162984D94737E3891A135B40CAA1FA476)

[[178,184,559,562,651\]. Deep Contextual Understanding: A Parameter-Efficient Large Language Model Approach To Fine-Grained Affective Computing](https://aimjournals.com/index.php/ijaair/article/download/314/288/680)

[[181,565\]. LOCAL RETRIEVAL AUGMENTED GENERATION WITH LARGE LANGUAGE MODELS ON EXTENSIVE TEXT CORPORA](https://dspace.cvut.cz/bitstream/handle/10467/122664/F8-DP-2025-Kucera-Jakub-thesis.pdf?sequence=-1)

[[182,185,188,191,554,560,575,649\]. Foundation Models and ICL](https://people.math.ethz.ch/~wueth/Lecture/InternationalSummerSchool/Lecture 13/Lecture-13.pdf)

[[190,309,324,332,334,335,394,422\]. ChatGPT's Technical Foundations: Transformers to RLHF](https://intuitionlabs.ai/pdfs/chatgpt-s-technical-foundations-transformers-to-rlhf.pdf)

[[192,196\]. Enhancing Transformer-Based Vision Models: Addressing Feature Map Anomalies Through Novel Optimization Strategies](https://arxiv.org/html/2509.19687v1)

[[193,197\]. Transformer in Touch: A Survey](http://poster-openaccess.com/files/icic2024/354.pdf)

[[194,199\]. 大模型时代](https://www.tup.com.cn/upload/books/yz/113235-01.pdf)

[[195\]. Exploring the Responses of Large Language Models to Beginner Programmers' Help Requests](https://acris.aalto.fi/ws/portalfiles/portal/122216038/Exploring_the_Responses_of_Large_Language_Models_to_Beginner_Programmers_Help_Requests.pdf)

[[201,204,234,552,579\]. 大模型简介](https://juejin.cn/post/7467969744307879945)

[[205,222\]. AgentTune: An Agent-Based Large Language Model Framework for Database Knob Tuning](https://renata.borovica-gajic.com/data/2026_sigmod.pdf)

[[220,241,589,615\]. ENHANCING EDUCATIONAL AI EDUCHAT WITH FINE-TUNED OPEN-SOURCE LANGUAGE MODELS](https://trepo.tuni.fi/bitstream/handle/10024/229163/SadiqJunaid.pdf?sequence=2)

[[228\]. Implementation of the first paper on word2vec - Efficient Estimation of Word Representations in Vector Space](https://github.com/OlgaChernytska/word2vec-pytorch)

[[231,237,602,617\]. Transformer模型及其变种](https://www.jianshu.com/p/c669d3978649)

[[232,235,599,603,618\]. Natural Language Processing: An Overview of Models, Transformers and Applied Practices](https://riunet.upv.es/bitstream/handle/10251/206356/CanchilaMeneses-ErasoCasanoves-Boix - Natural language processing An overview of models transform....pdf?sequence=1)

[[244,252,255,262,273,529,666,669\]. Hinton, LeCun and Bengio Receive 2018 Turing Award](https://www.i-programmer.info/news/82-heritage/12645-hinton-lecun-and-bengio-receive-2018-turing-award.html)

[[247,296,298,301\]. 低碳智慧建筑技术创新发展白皮书 2024（运行管理篇）](https://files.metaso.cn/api/public-file/preview?fileName=8676823095794880512.pdf)

[[250,277,279,281,286,288,290,292,294,303\]. Seminal Papers about Large Language Models](https://www.tensorloops.it/2024/01/06/seminal-papers-about-large-language-models/)

[[253,258,259,270,530,540,667,670\]. 人工智能](https://oos-cn.ctyunapi.cn/esnai-course/2305260857378005.pdf)

[[254,261,263,265,272,274,531,668,671\]. Large Language Models](https://www.cis.lmu.de/~hs/teach/23s/chatgpt/assets/talkl.pdf)

[[257,260,264,268,271\]. Yann LeCun, Geoffrey E. Hinton, and Yoshua Bengio](https://blog.csdn.net/weixin_30563319/article/details/94791295)

[[275\]. 六人畅谈人生关键时刻](http://finance.sina.com.cn/stock/t/2025-11-07/doc-infwqrfr2413733.shtml)

[[283,689\]. The Disruptive Influence of Large Language Models on Data Management](https://dl.acm.org/doi/abs/10.14778/3611479.3611527)

[[297\]. 本科教学动态](https://jwc.lzu.edu.cn/jwc/upload/files/20250320/73af6b8115d5494ba3bb8d49129ccbe8.pdf)

[[299,526,673\]. Foundations of Large Language Models](https://readwise-assets.s3.amazonaws.com/media/wisereads/articles/foundations-of-large-language-/2501.09223v1.pdf)

[[306,570\]. 大型语言模型的发展历程与技术解析](https://www.163.com/dy/article/JS5H3RHV05561000.html)

[[307,571\]. Evolution of Neural Networks to Large Language Models in Detail](https://www.labellerr.com/blog/evolution-of-neural-networks-to-large-language-models/)

[[308,393\]. Framework for Deep Learning-Based Language Models Using Multi-Task Learning in Natural Language Understanding: A Systematic Literature Review and Future Directions](https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?arnumber=9706456)

[[313,316,399,401,573,647\]. Large Language Models: A Survey](https://arxiv.org/pdf/2402.06196v1.pdf?trk=public_post_comment-text)

[[314,317,322,330,405,574,648\]. Transformers and Large Language Models](https://web.stanford.edu/~jurafsky/slp3/10.pdf)

[[318\]. Self-attention & Transformer](https://xjtu.app/uploads/short-url/Tgv1ZhLw7yO4h7jnoQrCpEU3zx.pdf)

[[319,323,406,409,417,418\]. Dive into Deep Learning](https://d2l.ai/d2l-en.pdf)

[[320,329,408,411,654\]. The Generative AI Journey for Enterprise](https://marketing.neutradc.com/summit_ebook.pdf)

[[326,328,413,416,653\]. LIFT: Efficient Layer-wise FineTuning for Large Language Models](https://openreview.net/pdf?id=u0INlprg3U)

[[331\]. Explainability in Large Language Models: Pathways to Refinement and Alignment](https://clarenceluo78.github.io/assets/papers/MRes_thesis_haoyanluo.pdf)

[[333,404\]. The Full Story of Large Language Models and RLHF](https://www.atomosphere.in/blog/the-full-story-of-large-language-models-and-rlhf)

[[336,351,486,508\]. 一文带你了解大语言模型LLM的过去、现在及未来](https://blog.csdn.net/qq_46883219/article/details/141709839)

[[337,352,487\]. The Emergent Impact of Large Language Models on Human Society, Economics, and Culture](https://www.oxjournal.org/economic-social-legal-cultural-impacts-large-language-models/)

[[338,353,488\]. Studio sperimentale su LLM di piccole dimensioni : Prestazioni, Ragionamento logico matematico, Risposte dirette e Tecniche di Retrieval-Augmented Generation](https://thesis.unipd.it/retrieve/9c2dac6b-7665-41b7-8cea-8a2776789023/Djossa_Edgar_Carlos_Komi.pdf)

[[339\]. Designing Large Language Model Applications](https://elibrary-dev.nusamandiri.ac.id/assets/fileebook/250217.pdf)

[[340,349,485\]. Large Language Models (LLMs): A Comprehensive Overview](https://www.johnsnowlabs.com/introduction-to-large-language-models-llms-an-overview-of-bert-gpt-and-other-popular-models/)

[[341,358,361,494\]. SHRDLU](https://iacampus.net/wp-content/uploads/2024/07/Historia-de-la-Inteligencia-Artificial.pdf)

[[342,345,362,364,483,489,495,507\]. Fine-Tuning of Large Language Models (LLMs)](https://old.ijies.net/finial-docs/finial-manuscripts/155348220620249513.docx)

[[343,367,368,505\]. Investigating Knowledge Elicitation Automation with Large Language Models](https://www.semantic-web-journal.net/system/files/swj3868.pdf)

[[344\]. Duże modele językowe i ich zastosowanie w analizach językoznawczych – przegląd wybranych badań](https://mediaispoleczenstwo.ubb.edu.pl/api/files/view/2863046.pdf)

[[346,348,484,490\]. Large language models in radiology: fundamentals, applications, ethical considerations, risks, and future directions](https://www.infodottori.it/wp-content/uploads/2023/10/Large-language-models-in-radiology-2.pdf)

[[347,491\]. FUZZ TESTING LARGE LANGUAGE MODELS](https://oulurepo.oulu.fi/bitstream/handle/10024/58020/nbnfioulu-202508225543.pdf?sequence=1&isAllowed=y)

[[350,363\]. Extraction automatique d'arguments par le biais de grands modèles de langage adaptés / Argument Mining with Customized and Feature-Injected Large Language Models](https://theses.fr/api/v1/document/2023ASSA0049)

[[354\]. 大模型崛起](https://files.metaso.cn/api/public-file/preview?fileName=8673664295730954240.pdf)

[[355,359,371,372,492,509\]. A Survey on Symbolic Knowledge Distillation of Large Language Models](http://www.arxiv.org/pdf/2408.10210)

[[356,360,365,493,496,510\]. 大语言模型极速入门：技术与应用](https://mag.qq.com/read/1056611312/7)

[[357,366,497\]. Integration of Large Language Models in Marketing and Business Processes](https://www.theseus.fi/bitstream/handle/10024/865770/Pearson_Jacob.pdf?sequence=2)

[[369,370\]. Logs to the Rescue: Creating meaningful representations from log files for Anomaly Detection](https://repository.tudelft.nl/file/File_e7b87d6c-c274-480a-895f-0035a98ccd23?preview=1)

[[373,376,513,516,544,696\]. Long Short-Term Memory (LSTM) networks were first proposed by Sepp Hochreiter and Jürgen Schmidhuber in 1997 for modeling sequence data.](https://github.com/tmatha/lstm)

[[374,514\]. RNN](https://www.cnblogs.com/duye/p/9393441.html)

[[375,377,515,517,697\]. Introducing JudgerAI - the revolutionary NLP application that predicts legal judgments with stunning accuracy!](https://github.com/MohammedAly22/JudgerAI)

[[378,518,545,698\]. Natural Language Processing in Action](http://kingcall.oss-cn-hangzhou.aliyuncs.com/blog/pdf/Natural Language Processing in Action57661606615143319.pdf)

[[379,383,388,519\]. LLM Primer — The Modern AI Reference 2025](https://llmprimer.com/)

[[380,520\]. LSTM神经网络](https://www.cnblogs.com/energy1010/articles/10663310.html)

[[381,521\]. Unlocking the Secrets in Semantics](https://www.ram-ai.com/sites/default/files/2020-04/202003_-ram-ai-unlocking-the-secrets-in-semantics.pdf)

[[382,385,527,547,694\]. word2vec最初是Tomas Mikolov发表的一篇文章](https://developer.aliyun.com/article/396709)

[[384,389\]. Word2Vec词向量扛鼎之作](https://www.bilibili.com/read/cv14921723)

[[386,528,548,695\]. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://files.metaso.cn/api/public-file/preview?fileName=8672129041080459264.pdf)

[[387\]. 大语言模型](https://baike.baidu.com/item/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/62884793)

[[390,397,400,403\]. 第1讲：Transformers 的崛起：从RNN到Self-Attention](https://www.cnblogs.com/1314520xh/p/18845484)

[[392,402\]. THE RISE OF LARGE LANGUAGE MODELS: A BEGINNER'S SURVEY](https://periodicos.newsciencepubl.com/arace/article/download/9901/11593/35933)

[[407\]. Natural Language Understanding with Python](https://download.bibis.ir/Books/Artificial-Intelligence/Natural-Language-Processing/2023/Natural Language Understanding with Python_bibis.ir.pdf)

[[410,414,420,421,423\]. Reinforcement Learning from Human Feedback (RLHF) Explained](https://intuitionlabs.ai/pdfs/reinforcement-learning-from-human-feedback-rlhf-explained.pdf)

[[419\]. Towards Effective and Efficient Language Models: RNN-Based Generative Model Enhancements, Transfer Learning, and Inference Optimization](https://publishup.uni-potsdam.de/opus4-ubp/files/67119/hu_diss.pdf)

[[424,427,432,624\]. A Survey of Large Language Models](https://openreview.net/pdf/3746fd898a147036cc09abd50bba2532904e68fb.pdf)

[[425,625\]. Summary of ChatGPT/GPT-4 Research and Perspective Towards the Future of Large Language Models](https://arxiv.org/pdf/2304.01852v2)

[[426,429,433,435,442,621,626,636,655,691\]. Understanding Large Language Models](https://magazine.sebastianraschka.com/p/understanding-large-language-models?utm_campaign=Data_Elixir&utm_source=Data_Elixir_434)

[[428\]. 大規模言語モデル(LLM)の学習方法 - Qiita](https://qiita.com/ys_dirard/items/a2eb6a8b3eb28746633a)

[[430,434,622,637,656,692\]. Deep Reinforcement Learning with Python: RLHF for Chatbots and Large Language Models, Second Edition](https://download.bibis.ir/Books/Artificial-Intelligence/Deep-Learning/2024/Deep Reinforcement Learning with Python_bibis.ir.pdf)

[[431,436,443,623,638,657,693\]. 驯服大型语言模型中的过度自信：RLHF中的奖励校准](https://www.alphaxiv.org/zh/overview/2410.09724v1)

[[437,444\]. REINFORCE++: An Efficient RLHF Algorithm with Robustness to Both Prompt and Reward Models](https://arxiv.org/pdf/2501.03262)

[[438,440,441,619,634\]. RLHF: 人类反馈强化学习在大语言模型中的应用与进展](https://developer.aliyun.com/article/1684041)

[[439,620,635\]. Preference-Aligned sLLM for Safe and Helpful RAG-Based Battlefield Analysis System](https://journal.kci.go.kr/jksci/archive/articlePdf?artiId=ART003212655)

[[445,450,627,628,640\]. 生成式AI加速创新，行业迎历史性机遇](https://files.metaso.cn/api/public-file/preview?fileName=8692425725846208512.pdf)

[[446,451,630,639\]. Claude Sonnet 4.5: A Technical Analysis & Benchmarks](https://cirra.ai/articles/pdfs/claude-sonnet-4-5-technical-analysis.pdf)

[[447\]. Anthropic推出首款混合推理模型Claude 3.7 Sonnet](https://www.gelonghui.com/live/1839838)

[[448\]. Claude 3.7 Sonnet: il nuovo modello di Anthropic](https://www.mathesisbergamo.it/wp-content/uploads/2025.03.05-A21-BlogAI.pdf)

[[449,629\]. ПРИНЯТИЕ РЕШЕНИЙ НА ОСНОВЕ КОРПОРАТИВНОЙ АНАЛИТИКИ](https://elib.bsu.by/bitstream/123456789/333568/1/ДР_ПИ_ЛаптёнокЕД_2025.pdf)

[[452,631\]. Analisi ed esperienze nel contesto della Generative AI e dei Large Language Model Analyses and experiences in the context of Generative AI and Large Language Model](https://tesi.univpm.it/bitstream/20.500.12075/17980/1/Tesi Mario Maio (1).pdf)

[[453\]. 研究觀點](https://www.mystockhk.com/UploadFiles/2025/10/231115455803DD84.pdf)

[[454\]. AI 大模型通報](https://www.mystockhk.com/UploadFiles/2025/10/231131260CF1BCB4.pdf)

[[455\]. Claude (Anthropic) — Claude（Anthropic 的大語言模型）](https://systems-analysis.ru/int/index.php?title=Claude_(Anthropic)_—_Claude（Anthropic_的大语言模型）&variant=zh-hant)

[[456\]. The Claude 3 Model Family: Opus, Sonnet, Haiku](https://www-cdn.anthropic.com/f2986af8d052f26236f6251da62d16172cfabd6e/claude-3-model-card.pdf)

[[457\]. Model Card and Evaluations for Claude Models](https://www.anthropic.com/claude-2-model-card)

[[458\]. The Illusion of Artificial Inclusion](https://arxiv.org/pdf/2401.08572v1)

[[459\]. Human Language Understanding & Reasoning](https://www.amacad.org/publication/human-language-understanding-reasoning)

[[460,461\]. The Georgetown-IBM Experiment Demonstrated in January 1954](https://link.springer.com/chapter/10.1007/978-3-540-30194-3_12)

[[462,465,471,472,498,501,511\]. Speech and Language Processing: An Introduction to Natural Language Processing, Computational Linguistics, and Speech Recognition with Language Models](https://web.stanford.edu/~jurafsky/slp3/ed3bookaug20_2024.pdf)

[[463,466,473,499,502\]. N-gram Language Models](https://web.stanford.edu/~jurafsky/slpdraft/3.pdf)

[[464,467,469,474,500,503,504,512\]. DATA-EFFICIENT DOMAIN ADAPTATION FOR PRETRAINED LANGUAGE MODELS](https://dr.ntu.edu.sg/server/api/core/bitstreams/dcd7c767-f32d-4fb2-92cb-5e73e618c754/content)

[[468,475\]. Automatic Evaluation of Dialogue-Systems Using Neural-Network Methods](https://bonndoc.ulb.uni-bonn.de/xmlui/bitstream/handle/20.500.11811/10873/7098.pdf?sequence=2)

[[470\]. N-gram 模型](https://www.cnblogs.com/MarisaMagic/p/17947487)

[[476,506\]. From ELIZA to ChatGPT: The Evolution of NLP and Financial Applications](https://dspace.mit.edu/bitstream/handle/1721.1/150502/2023_NLP_JPM.pdf?sequence=1&isAllowed=y)

[[477\]. Spoken Language Modeling from Raw Audio](https://theses.hal.science/tel-04646644v1/file/146137_NGUYEN_2024_archivage.pdf)

[[478\]. Word Embedding Models and Their Applications in Natural Language Processing](https://github.com/PaddlePaddle/book/blob/develop/04.word2vec/README.md)

[[479\]. Neural net language models](http://www.scholarpedia.org/article/Neural_net_language_models)

[[480\]. 预训练语言模型](https://cloud.tencent.com/developer/article/2117256)

*以下来源未被直接引用*

[大语言模型](https://llmbook-zh.github.io/LLMBook.pdf)

[Large Language Models Meet Next-Generation Networking Technologies: A Review](https://www.eurecom.fr/publication/7998/download/comsys-publi-7998.pdf)

[Generative AI for cyber threat intelligence: applications, challenges, and analysis of real-world case studies](https://link.springer.com/content/pdf/10.1007/s10462-025-11338-z.pdf)

[Application Analysis of the Language Model](https://www.itm-conferences.org/articles/itmconf/pdf/2025/01/itmconf_dai2024_04001.pdf)

[A Review of Large Language Models: Fundamental Architectures, Key Technological Evolutions, Interdisciplinary Technologies Integration, Optimization and Compression Techniques, Applications, and Challenges](https://www.mdpi.com/2079-9292/13/24/5040)

[Characterization of Large Language Model Development in the Datacenter](https://tianweiz07.github.io/Papers/24-nsdi.pdf)

[大模型](https://m.douban.com/doulist/158046013/)

[Intro to large language models](https://web.stanford.edu/class/biods271/assets/lectures/L2.pdf)

[CPEN 455: Deep Learning Lecture 6: Recurrent Neural Networks](https://lrjconan.github.io/UBC-CPEN455-DL/assets/slides_2025/rnn.pdf)

[The evolution, applications, and future prospects of large language models: An in-depth overview](https://www.ewadirect.com/proceedings/ace/article/view/10056/pdf)

[A Survey of Large Language Models](https://arxiv.org/pdf/2303.18223.pdf?fbclid=IwAR3GYBQ2P9Cww2HVM3oUbML9i5i3DMDBVv5_FvYWfEi-vdZqZoSM78jE2-s)

[Benchmarking Large Language Models for Decision-Making in Supply Chain](https://webthesis.biblio.polito.it/37210/1/tesi.pdf)

[大模型核心基础简介目录](https://blog.csdn.net/qq_36801966/article/details/147857810)

[Deep contextualized word representations](https://files.metaso.cn/api/public-file/preview?fileName=8672129130012286976.pdf)

[Generative AI and Large Language Models: A Comprehensive Scientific Review](https://www.preprints.org/manuscript/202504.0413/v1/download)

[A Survey on Multimodal Large Language Models](https://github.com/mbrukman/Awesome-Multimodal-Large-Language-Models/blob/main/README.md)

[Language Modeling and Large Language Models](https://link.springer.com/chapter/10.1007/978-981-95-4632-9_2)

[Pretraining the Vision Transformer using self-supervised methods for vision-based deep reinforcement learning](https://fenix.tecnico.ulisboa.pt/downloadFile/1970719973968748/91049_dissertation.pdf)

[Towards Principled Training and Serving of Large Language Models](https://escholarship.org/content/qt78s027gc/qt78s027gc.pdf)

[Benchmarking Techniques for Evaluation of Large Language Models](https://dspace.cvut.cz/bitstream/handle/10467/115227/F3-DP-2024-Jirkovsky-Adam-DP-final.pdf)

[Improving Large Language Models in Repository Level Programming through Self-Alignment and Retrieval-Augmented Generation](https://www.inf.uni-hamburg.de/en/inst/ab/lt/teaching/theses/completed-theses/2024-ma-strich.pdf)

[AI-based Generation of Descriptions for Protein Signatures: Fine-Tuning of Large Language Models and Comparative Analysis](https://thesis.unipd.it/retrieve/c7db3b85-c0a1-4c62-8dff-af44b87e5a15/Data_Science_MsC_Thesis_Angela_Kralevska.pdf)

[Pre-Trained Models: Past, Present and Future ](https://keg.cs.tsinghua.edu.cn/jietang/publications/AIOPEN21-Han-et-al-Pre-Trained Models- Past, Present and Future.pdf)

[LLMs Explained](https://accubits.com/large-language-models-leaderboard/transformer/)

[Deep learning](https://www.bcs-sgai.org/seminars/2023-05/info/p1-LLMs_v2modOpt.pdf)

[Large Language Model主题的若干论文简述](https://www.cnblogs.com/Java-Starter/p/17402834.html)

[第1讲：Transformers 的崛起：从RNN到Self-Attention](https://blog.51cto.com/melon0809/13877013)

[ENHANCING NATURAL LANGUAGE PROCESSING THROUGH TRANSFORMER MODELS AND LARGE SCALE PRETRAINED NETWORKS](https://scholar9.com/publication/FET_04_02_001_1746095935.pdf)

[Learnings from three Large Language Model Proofs of Concept](https://prod-g2g-assets.s3.amazonaws.com/documents/AI_POC_Learnings_Note_2024.pdf)

[TRUDO MAGAZINE ISSUE 03](https://trudo.tech/Trudo_Magazine_03.pdf)

[大模型是文化社会技术](https://www.thepaper.cn/newsDetail_forward_30634004)

[ПРИМЕНЕНИЕ БОЛЬШИХ ЯЗЫКОВЫХ МОДЕЛЕЙ В ОБРАЗОВАТЕЛЬНОМ ПРОЦЕССЕ](https://vestnik.volbi.ru/upload/numbers/368/article-368-4150.pdf)

[LSTM: A Search Space Odyssey](https://blog.csdn.net/peaceinmind/article/details/50848128)

[The Evolution of Generative AI](https://aitoolssoftware.com/the-fascinating-evolution-of-generative-ai/)

[Artificial Intelligence: Foundations of Computational Agents](https://mrce.in/ebooks/AI Foundations of Computational Agents 3rd Ed.pdf)

[LSTM 由Hochreiter & Schmidhuber (1997)提出 LSTM结构](https://blog.51cto.com/nav/neural-network_p_97)

[Jürgen Schmidhuber](https://www.doradolist.com/experts/jurgen-schmidhuber)

[General Principles of Human and Machine Learning](https://hmc-lab.com/downloads/teaching/GPHML_lecture10.pdf)

[LLM Glossary (draft version)](https://projects.academiccloud.de/api/v3/attachments/76033/content)

[Word2Vec and LSTM based deep learning technique for context-free fake news detection](https://link.springer.com/article/10.1007/s11042-023-15364-3)

[六、TensorFlow 和 Keras 中的 RNN · ApacheCN 深度学习译文集](https://www.kancloud.cn/apachecn/apachecn-dl-zh/1956023)

[结合RNN与Transformer双重优点，深度解析大语言模型RWKV](https://www.cnblogs.com/huaweiyun/p/18285808)

[Secrets of RLHF in Large Language Models Part I: PPO](https://arxiv.org/pdf/2307.04964v1)

[NLPとVision-and-Languageの基礎・最新動向 (1)](https://event.dbsj.org/deim2023/post/tutorial/deim2023_tutorial_T4_part1_nlp.pdf)

[InstructGPT Overview](https://yuezhou-oh.github.io/blog/llm/ChatGPT.pdf)

[Leveraging Large Language Models for Firm-Intelligence: A RAG Framework Approach.](https://lup.lub.lu.se/student-papers/record/9144767/file/9144772.pdf)

[Aligning Large Language Models: A Study on Reinforcement Learning from Human Feedback](https://amslaurea.unibo.it/id/eprint/32630/1/TESI-6.pdf)

[大模型落地-从理论到实践](https://www.cnblogs.com/justLittleStar/p/17845341.html)

[Claude Code is the Inflection Point](https://files.metaso.cn/api/public-file/preview?fileName=8708989130165764096.pdf)

[克劳德3模型家族：Opus、Sonnet、Haiku](http://library.qiangtu.com/download/814/pdf/814.pdf)

[MISR: MEASURING INSTRUMENTAL SELF-REASONING IN FRONTIER MODELS](https://openreview.net/pdf?id=kDF2Nw3non)

[Ai2 Scholar QA: Organized Literature Synthesis with Attribution](https://arxiv.org/pdf/2504.10861v2)

[Claude Code 是转折点 --- Claude Code is the Inflection Point](https://files.metaso.cn/api/public-file/preview?fileName=8708989165914734592.pdf)

[Claude](https://www.amazon.com/dp/2884742018)

[Building Our First Neural LM](https://self-supervised.cs.jhu.edu/sp2025/files/slides/07.mlp-language-modeling.pdf)

[N-gram](https://en.academic.ru/dic.nsf/enwiki/494102)

[n-Gram Models](https://link.springer.com/chapter/10.1007/978-1-4471-6308-4_6)

[Efficient and Robust Distributed System for Large n-gram Language Models](https://www.163.com/dy/article/EOM1KAIA0511K58A.html)

[Statistical Language Models Based on Neural Networks](https://www.fit.vut.cz/person/imikolov/public/rnnlm/thesis.pdf)

[LSTM Neural Networks for Language Modeling](https://blog.csdn.net/qq_32113189/article/details/79475049)

[N-gram模型](https://www.cnblogs.com/dahuang123/p/11990665.html)

[Speech and Language Processing](https://karczmarczuk.users.greyc.fr/TEACH/TAL/Doc/jurafsky_martin.pdf)