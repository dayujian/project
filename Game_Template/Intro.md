# README of Python Project

## 0. 【重要事项】公告栏

模板更新记录：

1. 2024/1/4:
   1. 将部分 `Maps.py` 中的函数移入 `Scene` 类方法
   2. 更新了 `Tiles.py`
   3. 优化了 `GameManager` 中常规 `update_regular()` 的逻辑
   4. 更加详细的解释了对 `GameManager` 中 `render()` 逻辑的说明
   5. 将代码部分用 `` 标出，优化了其他 markdown 语法
   6. 更新了欢迎致辞

---

## 1. 欢迎致辞

非常抱歉，大家要这么晚才能看到这份文档！  

这里是 Digital Interactive Experience, 旨在教大家入门使用 pygame，并开发一个简单的像素风格小游戏。

而这篇文档是对整个 Project 的一个概述，介绍了游戏的一些基本思想，以及我们提供的模板是如何实现了游戏的。  

这个 Project 的核心主要在于：游戏的框架，OOP 开发思想的学习，事件队列的概念，以及 git 的使用。  
让我们开始吧。  

---

## 2. 故事

> 您可以放心的跳过这一段内容。以下故事由 Chat-GPT 4.0 生成，SI 100B 团队不为此负任何责任或版权。

在繁华都市的一角，一位才华横溢的开发者，刚刚被自己投入心血的创业公司无情剔除。  
身无分文，他漫无目的地走到海边，坐在沙滩上，任由海风吹拂。波涛声似乎在告诉他，失败不是终点。他回想起自己对游戏的热爱，那些无数个夜晚熬夜编程的场景，那些和小伙伴们讨论创新游戏理念的时光。  
他深吸一口气，心中的迷茫逐渐消散，取而代之的是一股坚定的信念。他站起身，望着无垠的大海，心中有了答案：  
他要独立开发一款游戏，一款能够触动人心，带给人们快乐的游戏。他知道路途将会充满挑战，但他已准备好迎接未来的风浪。  
他微笑着，心中充满了希望和梦想，他要让世界看到，一个被抛弃的游戏开发者，同样能创造出震撼人心的作品。

---

## 3. 基础前置知识：游戏是如何运作的？

### 3.1 游戏画面是如何更新的？

您所看到的不断刷新的游戏界面其实也是一个逐帧播放的视频（帧：可以简单理解为一副画面，就像博物馆里的一幅画一样）。  

对帧的绘画叫做渲染(render)。这个过程在二维的游戏空间中（即本次 Project 的实践中）非常简单。先绘制的对象在下面，后绘制的对象在上面。绘制本身只需要把素材库中的图片画上去即可（调用 pygame 的内置函数）。但是对于三维模型，这个过程极为复杂，是计算机图形学(CG, Computer Graphics)的一部分。这在这门课中不会被涉及。

在游戏中，一帧(frame)的时长被称为一刻(tick)。一刻即为游戏内部的一个周期。在每一刻中，游戏中所有内容的状态都会被更新，对玩家的输入做出反应，然后再被显示到游戏界面上。

每一帧内不同的游戏内容可能会导致游戏以稍微不稳定的速率运行，但理想状态下，我们希望游戏运行中每一刻(tick)的时间是恒定的，比如每秒 30 帧。这在后续会被再次提及。

### 3.2 游戏内的对象是如何互相影响、互相交互的？我应该如何实现？

#### 3.2.1 什么是游戏里的对象？

面向对象编程(OOP)的思想在游戏中被广泛应用。我们可以将这个游戏的所有组成成分（玩家，敌人，障碍物，...）都抽象成一个个“游戏对象”。既然成为了一个 python 中的对象，那么它便可以用成员变量(member variables)来储存属于自己的信息（比如所在的 x, y 坐标、剩余的 HP等），也可以用成员函数(member functions)来定义自己应当做的行为（比如玩家如何移动）。

当然，有些内容并不需要同学们实现，因为可以通过继承(inheritance)来使得不同的类拥有相同的成员函数（亦可称为接口）或成员变量。继承是 python 或任何面对对象编程的语言拥有的重要特性，使得继承者（子类）可以拥有被继承者（父类）的同样的函数，或变量。如，游戏中的所有对象都需要拥有一些属性：表示其自身大小的方框；表示方框左上角的坐标（用来标识渲染的位置，等等）。这些都可以通过继承 pygame 提供的类 Sprite 来完成。这会在稍后被继续提及。

#### 3.2.2 游戏应该如何进行“更新”？

刚刚提到过，在每一刻里，游戏的所有内容都会更新。在我们的游戏里，这一行为实现在了 游戏管理者 GameManager 的 update() 函数中。在一刻的时间中，我们可以对游戏对象执行一次 update()函数，也可以根据事件的不同以不同的方式影响画面。不同的对象对这个函数的内容需要各有实现：玩家可能需要根据 WASD 是否按下而决定是否移动；游戏本身需要检测是否有碰撞发生；背景图片很可能什么都不需要做。

update()后，我们的游戏就应当把新的状态显示在屏幕上。原有的上一帧的游戏显示将会被 pygame 自动清除，然后再根据您所实现的 update() 更新过的状态（比如移动后的所在位置），重新将所有游戏对象再画出来。游戏对象具有的动画也会被逐帧播放。在一次 update() 中或是逐帧动画的两帧之间，游戏对象通常不会移动太大的距离，从而使 update 与显示不断循环下的游戏界面看起来像是平滑的动画。

#### 3.2.3 游戏中的特殊事件应该如何处理？

最后，玩家的某些行为可能会触发特殊事件(Event)。这些事件会如何影响游戏？很显然，玩家可能并不能直接管理到 GameManager，或者游戏场景，或是敌人类。这时，需要引入事件队列的概念：

游戏中有一个队列（可以简单理解为一个列表，list）。里面拥有各种事件，例如在当前一刻(tick)中，玩家的鼠标移动了，按下了W键，松开了A键（这些事件由 pygame 产生，不需要您产生，但您需要读取并作出反应）。游戏管理者 GameManager 就可以通过读取事件队列，从而对不同的事件作出不同的更新。同样的，我们也可以添加自定义的事件——例如玩家与怪物碰撞了，来使 GameManager 可以处理这些开发者定义的特殊事件。

### 3.3 为什么有这么多文件？我不能只写一个 .py 文件吗？

当然，一个 .py 文件是可以做到当前这个项目的，但我们**极度不推荐您这么做**。*这也可能导致您无法在 check 中得到代码整洁性和模块化的分数。*

写成多个文件有若干好处。首先是一个文件中的内容并不会太长。之后各位同学也许会接触越来越大的文件和项目，彼时在一个 .py 中塞入上百万行代码似乎并不是一个好选择。他会及其难以阅读和开发。（甚至，这可能会影响运行缓存命中和运行效率。这部分内容并不需要您掌握。）其次，模块化可以使代码更加清晰。您可以通过 Player.py 就猜到里面大概实现了玩家对象的渲染，移动更新，等等功能。别的同学与您合作也会更加方便。

此外还有一个名为资源(assets)的文件夹。在游戏开发环境中，资源文件夹通常包含游戏运行所需的基本资源、视觉元素等。这个文件夹常见的包括图像、音频文件、关卡设计数据（简单来说，就是保存您地图的文件，比如瓷砖、特殊拾取物等）。将这些资源组织在一个资源文件夹中有助于简化开发流程，并使得管理和更新游戏内容变得更加容易。

您的最终 `Game_Project` 文件夹很可能会长这样：

├─Game_project  
│  │  Main.py  
│  │  NPC.py  
│  │  Player.py  
│  │  Settings.py  
│  │  ... (如果您需要更多文件，请自由添加并妥善的管理他们的名称和内容。请注意，名称中不要带中文或空格等字符。)  
│  │  
│  ├─assets  
│  │  ├─background  
│  │  │      menu.png  
│  │  │      ...  
│  │  │  
│  │  ├─...(如果您需要更多素材，如图片、音乐，请自由的在这里添加并管理好他们的路径。请注意，名称中，不要带空格或中文等字符。)  
│  │  
│  └─\_\_pycache\_\_  
│          (这个内容由 python 编译产生，您暂时不需要了解他的原理，也不需要刻意删除或改动他。请注意，虽然 python 是一门解释性语言，但是他仍然可以完成一定程度上的编译。请将其添加到您的 .gitignore 中，您可以直接复制 SI100B\_DIE\_Repo 中的 .gitignore。)

---

## 4. 好的，所以这么多东西我怎么写？

可想而知，从零开始写出一个完整的游戏绝不是能一蹴而就的小工程。本游戏的大量内容需要逐步完成。因此，我们将给出一个大致的实现顺序。例如，您可以先实现主城，从而使游戏启动后显示的不再是黑屏；然后可以让这个场景里开始产生 NPC；再开始添加 update, 更新玩家移动。接下来当您成功让玩家与 NPC 碰撞并产生对话框时，应该就对这次作业的做法了然于胸了。

我们建议您先阅读以上的介绍和后续完整的题目说明，对这个游戏基本了解，之后再开工。**但如果您有较为充分的实力，完全可以按照自己的想法优化或重写我们提供的模板。**

### 4.1 我的哪些部分会纳入评分？哪些不会？

请注意，我们以**最终完整度和代码整洁度**为主要评分项目。同时，我们鼓励创新，支持您实现一些额外的小功能，使得游戏看起来更加**完整**，例如攻击动画、移动特效等。

我们**不评价**以下内容：

+ 游戏资源，贴图，音乐是否精致
+ 游戏是否好玩，数值是否合理
+ ...（仅跟游戏设计相关的内容都不会纳入评价）

## 5. 实现内容概述

==请注意，以下的内容是**您需要实现的功能**，但不是**您推荐实现的顺序**==。

### 5.1 `Main.py`

这部分应当是您的游戏的起点。（设想一个同学打开您的代码库，他应该从哪个文件开始运行？显然 `Main.py` 是一个明显的起点。）不过，这部分内容并不需要您们实现。为了代码整洁性（以及符合一般架构），`Main` 只需要初始化 `GameManager` 对象（5.2中介绍） 并在一个 `while True` 的循环中不断调用 `GameManager.update()`，最后调用 `pygame.display.flip()` 把 pygame window 对象中的内容渲染到屏幕即可。

**省流：您不需要书写或更改这部分内容。我们已经为您提供了代码。**

不过您可能会注意到，直接运行 `Main.py` 时，会产生一个报错：`pygame.error: Display mode not set`。这是因为您还没有在 `GameManager` 中书写初始化等内容。我们会在 5.2 中介绍。

### 5.2 `GameManager.py`

首先，您一定会想，什么是 `GameManager`? 为了理解它，我们可以设想一个狼人杀游戏：在一场12人的狼人杀中，同时还会存在一位“上帝”：他负责开局发牌；负责轮流让所有人发言；负责统计投票，负责让某个人发出遗言... 这位上帝负责了游戏整体运行过程，这也就是我们设计 `GameManager` 的意义：他负责让所有对象进行状态的更新（如位置移动，碰撞检测等），再渲染到屏幕。事实上，这部分内容在先前的课程中普遍是写在 `while True` 中的（为了方便各位理解）。不过，为了使代码更加整洁，我们最终要求其放在 `GameManager.py` 中。

那么，应当如何开始书写他呢？我们可以从 `__init__` 开始使您的游戏窗口能够正确的出现。

注：一些 `GameManager.py` 依赖的内容被整合在了 `Settings.py` 中。这部分的内容会以大驼峰命名法出现，如 `WindowSettings`。在这些类的内部您可以找到一些设置，如 `WindowSettings.name`。  
调用 `Settings.py` 是非常重要的。否则，可能会出现代码中数值不一致的情况，例如在屏幕设置的时候设置为 1280\*720 的屏幕，渲染时却渲染到了 1920\*1080 的屏幕上。

#### 5.2.1 `__init__(self)` 函数

这个内容在 `GameManager` 初始化时会被调用，也就意味着“上帝”角色的初始化（就像狼人杀中，上帝必须先拿牌、发牌一样）。对于 `GameManager` 而言，他最开始需要做到以下内容。（但并不局限于此。他后续会有更多需要做的内容。）

1. 初始化 `self.window`，使得您能拥有一个屏幕对象并与之交互。您的所有渲染操作都会将图片绘制到 `self.window`。
   1. (可选) 您可以选择给您的游戏一个标题，通过 `pygame.display.set_caption(WindowSettings.name)`。（`WindowSettings` 定义在 `Settings.py` 中）
2. 将当前游戏状态设置为 `GameState.MAIN_MENU`。
3. 初始化 `self.clock` 为 `pygame.time.Clock()`。后续会进行一些依赖于时间的判定。
4. 初始化 `BGMPlayer` 播放器对象。
5. 初始化您的玩家(`Player`)对象。这部分内容会在 5.3 进行介绍。
6. 初始化您的场景(`Scene`)对象。这部分内容会在 5.4 进行介绍。

#### 5.2.2 `update(self)` 函数

回想之前的内容，在 `Main.py` 中，`GameManager.update()` 在不断被调用。这是整体游戏一轮的更新，就像狼人杀中所有人都发言、投票、剔出一人的大循环一样。

这部分的内容大致应当是：

1. 调用 `self.clock.tick(30)`，来控制游戏帧率
2. 使用一个 if-elif-elif-...，根据不同的 `self.state`，调用不同的更新函数。

```python
self.tick(30)

if self.state == GameState.MAIN_MENU:
    self.update_main_menu(pygame.event.get())
elif self.state == GameState.GAME_PLAY_CITY:
    self.update_city(pygame.event.get())
elif self.state == GameState.GAME_PLAY_WILD:
    self.update_wild(pygame.event.get())
elif self.state == GameState.GAME_PLAY_BOSS:
    self.update_boss(pygame.event.get())
```

##### 5.2.2.1 `update_main_menu()` 函数

这部分的内容相对简单。由于 `GameState.MAIN_MENU` 状态下，就是游戏主界面，需要按下空格进入真正的游戏，所以这部分的 update 内容包含；

遍历 所有的事件  
-> 如果 `event` 为 `pygame.QUIT`, 则退出游戏。调用 `pygame.quit()` 与 `sys.exit()` 分别退出 pygame 和 程序。  
-> 如果 `event` 为 `pygame.KEYDOWN`, 则判定 `event.type` 是否为 `pygame.K_RETURN`。
->-> 如果判定成功，则调用 `self.flush_scene(SceneType.CITY)` 切换场景对象，并将 `self.state` 设置为 `GameState.GAME_PLAY_CITY`。  

##### 5.2.2.2 `update_city()` 和其他 update 函数

> update_city(), update_wild(), update_boss()

这部分内容主要负责了在一个指定的场景中需要 update 的内容。

之所以这么设计，是因为每个场景也许需要“观察”不同的事件。例如，您并不需要在主菜单中观察是否有玩家触发商店，也不需要在 city 和 wild 场景中观察是否有玩家和 boss 发生碰撞。

您的逻辑应当是：

遍历所有事件；  
如果有 `event` 为 `pygame.QUIT`, 则退出游戏；  
如果有 `event` 为 `GameEvent.EVENT_DIALOG`，则触发对话框。这部分内容应当在 `self.scene.trigger_dialog` 中实现；
... （其他事件也是同理。）  

最后，进行所有的常规判定。这些判定不依赖于事件发生。例如，您可能只有在按下 W 和松开 W 会产生 `pygame.KEYDOWN` 和 `pygame.KEYUP`, 但期间您仍然需要让玩家移动若干像素。（思考一下，如何实现？您可以试着在玩家类中实现一个 flag 表示他是否正在按下 W, 并在有按键按下或松开时更新这个成员变量）。

##### 5.2.2.3 `update_collide` 函数

显然，您需要更新玩家的碰撞状态。碰撞后，您需要：1. 向事件队列发送信号来表示发生事件 2. 更新玩家的碰撞状态(例如，一个布尔变量和一个他正在碰撞的对象)。

这部分的逻辑可能是：

使用 `pygame.sprite.spritecollide` 检测玩家是否和场景中由 障碍物构成的 `spriteGroup` 发生碰撞。如果是，更新玩家正在碰撞的障碍物，以及玩家是否正在和障碍物碰撞这两个玩家内的成员变量。（思考一下，为什么这里不需要向事件队列发送信号？）

同样的，检测玩家是否和 Monsters, NPC, Boss 碰撞。如果是，和上面一样更新玩家的状态，并向事件队列发送信号，表示需要触发对话框。

##### 5.2.2.4 `update_regular()` 函数

有些更新并不依赖于事件，例如 NPC 的自然浮动，玩家的移动，等等。您需要在 `update_regular()` 中实现这些操作，并添加到 5.2.2.2 的每个 update 的结尾。之所以这么做是为了代码复用，因为对于每个场景，总是有一些常规的 update 是完全相同的。

#### 5.2.3 `render()`

在游戏的 `GameManager` 的最后，我们要求了 `GameManager.render()`。根据场景的不同，render 会调用不同的渲染函数。

您的逻辑可能是：

当 `self.state == GameState.MAIN_MENU` 时，调用 `self.render_main_menu()`；
同样的, `self.state` 为其他状态的时，调用 `self.render_?()`, 其中?为对应场景的渲染函数。

代码可能会是这样：

```python
if self.state == GameState.MAIN_MENU:
    self.render_main_menu()
elif self.state == GameState.GAME_PLAY_CITY:
    self.render_city()
elif self.state == GameState.GAME_PLAY_WILD:
    self.render_wild()
elif self.state == GameState.GAME_PLAY_BOSS:
    self.render_boss()
```

##### 5.2.3.1 `render_main_menu()` 与其他渲染函数

这些函数会调用 `Scene` 的子类，如 `MainMenu` 内部的方法实现。因此，这些函数可能只有一行，直接调用对应的 `self.scene.render` 即可

您可能会想问：为什么渲染写在了 `Scene` 或其子类的类方法里面，而更新却是写在 `GameManager` 里？  
这是因为，渲染的所有对象都归 `Scene` 管理，但是更新的时候可能会涉及到不同游戏对象之间的交互。而一个游戏对象本身不应当管理其他对象，所以更新需要在 `GameManager` 中实现。不过，对对象本身的更新的确是在类内部实现，例如 `Player` 类中确实存在 `update()` 方法。  

### 5.3 `Player.py`

游戏怎么能少得了它最终要的组成部分——玩家，在 `Player.py` 文件中，我们将创建一个玩家的对象，并通过该对象进行相关的运动控制与属性管理。

#### 5.3.1 `__init__(self)`

在初始化一个玩家角色时，您需要载入玩家的图片、坐标，以及一些战斗属性的参数，例如生命值、攻击力、防御值、初始的金币等。`Player` 类继承自 `Sprite` 类，这样可以方便 `Player` 与游戏中其他对象的交互检测。注意到 `Player` 还继承自另外一个类叫做 `Collidable` ，这一父类在 `Attributes.py` 中实现，主要用来提供碰撞检测后存储结果的接口。通过继承，您可以调用 `Collidable` 中的方法来在 `Player` 类中获取它与其他物体的碰撞信息。

#### 5.3.2 `attr_update()`

这个函数用于更新玩家的属性参数，主要用于战斗结算后以及商店的交易中，例如获得或花费金币，提高生命值等操作。

#### 5.3.3 `reset_pos()`

这个函数用于重置玩家在场景中的位置，主要用在场景转换时，玩家在进入新场景后需要固定的坐标，否则可能会出现一些bug或直接进入战斗状态等不可预测的结果。

#### 5.3.4 `try_move()`

这个函数负责玩家的移动过程，根据键盘按键的响应，Player应当进行响应的移动，也就是坐标的改变。由于玩家有可能在移动之后碰到障碍物从而使得移动无效（也就是被撤销），所以在移动后还需要进行额外的碰撞检测以及位置的调整，所以该函数叫做 `try_move` 而不是 `move`。

#### 5.3.5 `update()`

这个函数会在玩家与场景的碰撞检测完成后被调用，因此它需要做的第一件事是进行碰撞的判定，并根据碰撞的结果调整自己的坐标，使得 `Player` 不再与障碍物相交。其次该函数还需要实现 `Player` 自身周期性的状态维护，例如在走动时的走动效果播放，也就是顺序播放素材库中逐帧的动画，实现一个运动特效

#### 5.3.6 `draw()`

该函数负责在窗口绘制自身，其中需要考虑场景 `camera` 的存在，需要在绘制时进行位置的偏移。

### 5.4 `NPCs.py`

有了玩家以后，大家自然能想到还会有 NPC，在我们的项目中，所有不由玩家控制的角色，包括以及敌人等对象，都在 `NPCs.py` 中实现。他们都继承自 `Sprite` 类，方便进行统一的交互管理。当我们需要同时管理多个类似的 `Sprite` 对象时，我们会创建一个 `Group` 用于管理 `Sprite`，并将 `Sprite` 加入 `Group` 中。我们可以对于整个 `Group` 进行碰撞检测，而不需要手动对场景中的每个 `Sprite` 进行检测。

在每个 `NPC` 类中都会有 `draw` 的方法用于绘制自身，并且需要考虑场景的 `Camera` 信息，进行位置的偏移。

#### 5.4.1 NPC

首先我们创建了一个 `NPC` 的基类，与玩家类似，它也继承自 `Sprite` 和 `Collidable` 类。`NPC` 会有许多子类，因此它也有一个 `type` 变量来记录它的类型，如 `NPCType.DIALOG`, `NPCType.SHOP` 等，方便对 `NPC` 类型的判定以及相应的功能实现。这些类型定义在 `Settings.py` 中。

##### 5.4.1.1 `__init__(self)`

在NPC的初始化中，我们需要设置该NPC的一些属性，比如名字，图片，坐标等等。我们还需要设置一个talkCD的变量用来实现NPC与玩家结束对话后短时间内不再触发的计时，以及一个talking变量用于记录NPC是否正在与玩家交互。

##### 5.4.1.2 `update()`

其次是 `update` 方法，这个方法需要根据具体的NPC类型来实现，因此我们将该函数的内容设为 `raise NotImplementedError`，以避免子类未实现该方法时。它的功能主要包括角色立绘的更新、坐标的更新、`self.talkCD` 等更新信息，维护角色在场景中的特定行为。

##### 5.4.1.3 `reset_talkCD()`

该方法用于重置 `talkCD` 变量，当CD为0结束冷却时，可以调用该方法将冷却重置。您可以自由设置冷却时间的长度。

#### 5.4.2 `DialogNPC`

接下来主要是具体的 `NPC` 子类的实现。首先是 `DialogNPC`，顾名思义，这一类NPC主要特征在于他们会与玩家发生对话，因此他们有一个变量 `dialog` 来设定对话的内容。另外，他们会在场景中进行有规律的移动。当然，您可以任意地设计他们的行为。因此在初始化时，您需要设置一些移动相关的参数，例如移动的范围、速度等，并在 `update()` 函数中进行位置的更新。具体的触发对话的内容会由 `GameManager` 来执行。

#### 5.4.3 `ShopNPC`

该类的NPC主要实现了商店的功能，它通常是不动的，您只需要在创建时额外关注它商店中的商品信息，以及它的对话内容即可。在 `update()` 中，您只需要关注它的 `self.talkCD` 的更新。

#### 5.4.4 `Monster`

除了善良友好的NPC们，自然还有敌人需要我们去击败。`Monster` 类主要负责实现关于怪物的相关信息。同样的，它也继承自 `Sprite` 类。

##### 5.4.4.1 `__init__(self)`

在初始化时，我们需要载入它的图片，甚至于动画以及特效等等，确定它的初始坐标，以及它的战斗属性，如生命值，攻击力，防御值，还有它被击败后会掉落的奖励如金币。

##### 5.4.4.2 `update()`

您可以定义怪物的操作，例如原地不动、随机移动等，并在 `update()` 中进行相关的更新。由于怪物在被击败后就会消失，因此您不需要考虑 `self.talkCD` 相关的问题。

#### 5.4.5 `Boss`

最后是 `Boss` 的实现，其实它和 `Monster` 是类似的，在初始化时载入相关的图片、动画、坐标等，设置生命值、攻击力、防御值以及掉落的奖励。

### 5.5 `Scene.py`

我们建立了一个 `Scene` 的类用于管理不同的场景，以及场内的物体、交互行为等。主要分为三个场景：主城、野外（战斗）和boss图，他们也是 `Scene` 类的三个子类。此外，游戏的开始界面也在 `Scene` 文件中进行实现。

#### 5.5.1 `Scene`

这是所有场景类的基类，它会对整个场景的接口进行规定与实现，在父类中具体的元素都会被设置为默认值，例如 `None`，然后由子类来创建具体的对象等信息。

##### 5.5.1.1 `__init__(self)`

在一个场景的初始化中，您需要生成以下的内容：场景本身的属性，例如场景的大小，场景的背景贴图/地图，Camera系统，场景中可能的障碍物，场景中的npc、野怪、boss等，场景中可能的用于场景切换的传送门等，以上的内容通常都由 `Sprite` 的单元组成，因此把他们放进 `Group` 里会是一个比较好的选择。另外，场景中会发生对话、战斗、以及商店等特殊事件，因此也各自需要一个变量用于记录他们的状态，例如是否处在对话中等，并需要对对话框等组件进行生成。当没有进入对话时，这些组件会设置为 `None`，在进入事件时生成一个新的实例化对象进行调用。

##### 5.5.1.2 `trigger_dialog()` 等

接下来是一系列与对话、战斗以及商店交易相关的辅助函数，通过这些函数您可以对相关的状态量进行系统的处理与更新。`trigger_dialog()` 与`end_dialog()` 用于设置对话框的开始和结束状态，类似的，`trigger_battle()` 和 `end_battle()` 用于设置战斗界面的开始与结束，而 `trigger_shop()` 与 `end_shop()` 用于商店对话的开始与结束设置。您们需要在事件开始的时候生成新的对话框实例化对象，在结束时把该对话框重置为 `None`，此时 python 会自动销毁对象。

##### 5.5.1.3 `update_camera()`

在场景中，由于我们的地图大小可能会大于窗口大小，因此我们需要一个`camera` 的对象来跟踪玩家的位移，例如当玩家在朝画面的右侧移动时让整个画面跟随玩家进行移动。您可以简单想象一个大地图上的小窗口，我们需要把大地图中的对象渲染到小窗口上，而物体的坐标是在大地图下的坐标，这个时候就需要通过 `camera` 记录小窗口所在的位置，将它作为偏移量参与地图中物体的渲染，从而实现镜头跟随主角的目的。具体实现时，您可以根据主角所在的位置计算 `camera` 应当设置的值，同时要对 `camera` 进行上下限的限定，防止镜头跑出大地图外。

##### 5.5.1.4 `render()`

作为父类中的 `render` 函数，它会对场景中每一个可能的存在进行渲染，具体来说就是对每一个成员进行 `draw()` 方法的调用。它需要先判定每个成员是否存在，（例如boss场景下可能不存在npc），随后对每个存在的对象进行渲染。在渲染前记得更新 `camera` 变量，并根据 `camera` 的值进行绘制。

#### 5.5.2 `StartMenu`

这个类用于处理和开始界面相关的内容。类似的，如果您想做一个游戏结束页，也可以采用相似的方式进行实现。

在初始化时，您需要设置开始界面的背景、显示的字体以及文字等信息，另外您还需要设置字体闪烁的时间间隔。当然，您也可以实现您自己的游戏开始界面。在 `render()` 中，您需要更新字体闪烁相关的信息，例如根据时间计数周期性地显示字体，并在一段时间后重置该闪烁。如果界面中有其他内容，也应当在 `render()` 方法中进行统一的渲染调用。

#### 5.5.3 `CityScene`

这个类继承自 `Scene`，主要负责实现主城的内容。在初始化时，您需要对主城进行生成，例如调用 `gen_CITY()`，并设置自己的 `type` 为 `SceneType.CITY`。您需要设置主城对应的背景、地图、障碍物、npc、传送门等。您可以自由地对您的主城进行构建。

#### 5.5.3.1 `gen_city_map()`等

`gen_wild_map()`, `gen_city_map()` 和 `gen_boss_map()` 分别实现了不同场景下的背景地图生成。在这些方法中，他们各自载入了不同场景下的地图的贴图，然后进行随机的地图生成。在这里，我们会用到 `SceneSettings` 中的 `tileXnum`， `tileYnum` 参数，这两个参数设定了场景中地图贴图的数量，这样方便了贴图位置的生成与计算。

#### 5.5.3.2 `gen_city_obstacle()`等

`gen_wild_obstacle()`, `gen_city_obstacle()`和`gen_boss_obstacle()` 分别实现了不同场景下使用 `block` 类的障碍物生成。由于障碍物 `block` 继承自 `Sprite` 类，因此我们将所有的 `block` 放在一个`Sprite` 构成的 `Group` 中。在主城和boss场景中，您可以简单地围绕地图生成一圈障碍物，或者您可以根据您自己的想法进行绘制。在野外，您可以随机生成一些障碍物。在我们的示例中，我们手动控制了障碍物生成的范围，使得角色出生点周围不会存在障碍物。您也可以尝试别的方法进行障碍物的生成，或者通过提前制作地图的形式进行导入。

#### 5.5.4 `WildScene`

这个类同样继承自 `Scene`，主要负责野外区域地内容。因此在初始化时调用 `gen_WILD()`，进行野外地图、障碍物、野怪以及传送门的生成。您通常需要随机生成多个怪物，而这在 `gen_monsters()` 中实现，它负责随机地生成怪物的坐标、属性，并确保它不会与现有的场景产生冲突等。

#### 5.5.5 `BossScene`

与前文类似，这个类负责 boss 场景下的生成。这里需要重写父类中的`trigger_battle()` 方法，因为战斗的对象变为了 boss。

### 5.6 `Tile.py`

在这个文件中，我们将实现与瓷砖相关的方法。

#### 5.6.1 `Tile`

首先是组成障碍物的 `Tile` 类，由于障碍物需要进行碰撞检测，因此它继承自 `Sprite` 类。在 `Tile` 的初始化中，我们需要载入对应的贴图，设置 `Tile` 所在的位置。在 `draw()` 中，对自身进行渲染。注意在`Tile` 的绘制中也需要考虑 `camera`的偏移。

### 5.7 `PopUpBox.py`

这个文件主要负责实现一些遭遇事件，例如与npc发生的对话、商店的购买，以及与怪物的战斗，由于他们是位于 `Scene` 图层的上方，作为独立的弹出窗口进行实现，因此叫 `PopUpBox`。它的启动和结束都由 `Scene` 控制，并作为 `Scene` 中的组件由 `Scene` 管理。注意，在这部分的组件中，绘制时都不需要考虑 `camera`，因为他们的位置是相对窗口进行设置的。

#### 5.7.1 `DialogBox`

在对话框的初始化中，您需要设置对话框中的对话内容，字体信息等，以及对话框的背景。如果您想要创建一个带有透明度的窗口，可以使用 `pygame.Surface( (width,height),pygame.SRCALPHA)` 进行实现。另外您需要设置对话框中的npc，用于对话框中立绘的绘制。与其他组件相同的，对话框会在 `draw()` 中进行自身的渲染。您需要绘制您的框体，您的npc图片，以及对话的内容。当您需要进行换行的时候，可以使用 `DialogSetting` 中的 `textVerticalDist` 属性进行语句高度位置上的偏移，从而达到换行的效果。

#### 5.7.2 `BattleBox`

战斗界面相对对话框会更复杂一些。在初始化的时候，除了需要设置默认的框体信息外，还需要加载角色的战斗信息，包括玩家的立绘、生命值、攻击力、防御值，以及怪物的立绘、生命值、攻击力、防御力等。在战斗的过程中，还需要一些变量用于记录战斗相关的信息，如攻击的是哪一方，是否处于绘制战斗动画状态，战斗动画的时长，战斗是否结束等信息。

在 `draw()` 中需要绘制整个窗体以及玩家和怪物的立绘，同时还需要显示二者实时的生命值。您需要进行战斗动画的绘制，当然您也可以在这过程中加入自己的战斗特效等。当一次攻击的动画被播放完并且战斗没有结束，就要进行下一次攻击的计算，被攻击者的生命值减去攻击者的攻击力与被攻击者防御力的差值。如果攻击力小于防御力，就不会造成伤害。计算完成后要对攻击的是哪一方等信息进行维护。当玩家或怪物任意一方的血量小于等于0时，战斗结束，设置战斗状态并进行结算。如果玩家战胜了怪物，显示相应文字并结算战斗的收益；如果玩家被怪物击败，显示相应文字并结束游戏，回到开始菜单。

#### 5.7.3 `ShoppingBox`

商店界面主要是基于对话框的逻辑进行，在初始化时首先设置框体、背景、字体等信息，然后创建一个新的窗口用于显示商店中的物品并进行交互。另外，我们还需要一个变量 `selectedID` 用于记录选中的是第几个商品，并对它进行显示上的额外处理。

在 `draw()` 中进行窗口内容的绘制。除了显示npc的对话以外，我们还需要显示商店的商品信息以及玩家的属性信息和持有的金币数量。在显示商品的时候，我们首先获取npc持有的商品，然后将他们一行一行地进行显示。当遇到 `selectedID` 对应的商品时，我们可以修改它的缩进，或者修改字体颜色、背景颜色等方法，让它和其他选项不一样，从而实现它的“选中”状态。

`ShoppingBox`还有一个方法`buy()`用于实现商品的交易，根据`selectedID`对`player`进行实际的属性修改操作。当您需要对商人设置库存时，您也可以在这里进行库存的更新。

### 5.8 `Portal.py`

在 `Portal` 中实现了一个传送门的类，用于放置在场景中进行场景的切换。在初始化时，需要载入它的贴图，坐标，以及它通往的由 `SceneType` 枚举类进行定义的场景。在 `draw()` 方法中进行自身的渲染，渲染时需要考虑 `camera` 的偏移。

### 5.9 `BgmPlayer.py`

在这个文件中我们创建了一个管理bgm播放的播放器，它由 `GamePlayer` 直接管理，并在场景切换时相应地切换背景音乐的播放。如果您需要实现自己的音效等功能，也可以通过它来进行管理。

#### 5.9.1 `__init__(self)`

在初始化中，`pygame.mixer.init()` 被调用，进行游戏音乐的初始化。载入不同场景下可能用到的bgm路径备用。

#### 5.9.2 `play()`

实现音乐的播放。调用 `pygame.mixer.music.load(路径)` 将bgm载入游戏的播放器，调用 `pygame.mixer.music.play(loop)` 进行播放。其中loop参数控制了播放的次数，默认值为-1表示一直循环播放。

#### 5.9.3 `stop()`

调用 `pygame.mixer.music.stop()`来终止当前音乐的播放。

#### 5.9.4 `update()`

在场景转换时切换相应的背景音乐，首先调用 `stop()` 停止当前播放的音乐，然后根据 `update` 输入的参数播放新的音乐。