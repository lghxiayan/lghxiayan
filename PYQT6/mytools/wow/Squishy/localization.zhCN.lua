-- zhCN localization

local L = AceLibrary("AceLocale-2.2"):new("Squishy")

L:RegisterTranslations("zhCN", function() return {

	-- bindings
	["Target unit with highest priority"] = "定位第一优先单位。",
	["Target unit with 2nd highest priority"] = "定位第二优先单位。",
	["Target unit with 3rd highest priority"] = "定位第三优先单位。",

	-- from combatlog
	["(.+) begins to cast (.+)."] = "(.+)开始施放(.+)。",
	["(.+) gains (.+) Mana from (.+)'s Life Tap."] = "(.+)从生命分流获得了(.+)点法力值。",

	-- options	
	["Default"] = "Default",
	["Smooth"] = "Smooth",
	["Button"] = "Button",
	["BantoBar"] = "BantoBar",
	["Charcoal"] = "Charcoal",
	["Otravi"] = "Otravi",
	["Perl"] = "Perl",
	["Smudge"] = "Smudge",
	
	["always"] = "一直",
	["grouped"] = "组队时",
	
	["Frame options"] = "框体设置",
	["Show Border"] = "显示边框",
	["Shows/hides the frame border."] = "显示/隐藏窗体边框",
	["Show Header"] = "显示标题",
	["Shows/hides the frame header."] = "显示/隐藏窗体标题",
	["Scale"] = "缩放",
	["Scales the Emergency Monitor."] = "缩放紧急状况监视器。",
	["Number of units"] = "单位数量",
	["Number of max visible units."] = "最大显示单位数量",
	["Frame lock"] = "锁定框体",
	["Locks/unlocks the emergency monitor."] = "锁定/解锁紧急状况监视器。",
	["Show Frame"] = "框体显示",
	["Sets when the Squishy frame is visible: Choose 'always' or 'grouped'."] = "设置Squishy框体的显示方式。选择'一直'，'组队时'或'。",
	["Pet support"] = "宠物支持",
	["Toggles the display of pets in the emergency frame."] = "切换是否在紧急状况监视器中显示宠物。",
	
	["Unit options"] = "外观设置",
	["Alpha"] = "透明度",
	["Changes background+border visibility"] = "设定背景与边框的透明度。",
	["Style"] = "样式",
	["Color bar either by health, class or use the CTRA style."] = "根据生命值、职业或者CTRA方式给生命条着色",
	["Health"] = "生命值",
	["Class"] = "职业",
	["CTRA"] = "CTRA",
	["Texture"] = "材质",
	["Sets the bar texture. Choose 'Default', 'BantoBar', 'Button', 'Charcoal', 'Otravi', 'Perl', 'Smooth' or 'Smudge'."] = "设置状态条的材质。",
	["Health deficit"] = "生命减少量",
	["Toggles the display of health deficit in the emergency frame."] = "切换是否在紧急状况监视器中显示生命减少量。",
	["Unit bar height"] = "条高度",
	["Unit bar width"] = "条宽度",
	["Bar Spacing"] = "条间距",
	["Change the spacing between bars"] = "修改条之间的间距",
	["Inside Bar"] = "条内部",
	["Outside Bar"] = "条外部",
	["Name position inside bar"] = "名字在条内部显示",
	["Show name position inside bar"] = "名字在条外部显示",
	["Class colored name"] = "名字职业颜色",
	["Color names by class"] = "使用职业颜色对名字显示着色",
	
	["Class options"] = "职业相关设置",
	
	["Various options"] = "杂项设置",
	["Audio alert on aggro"] = "获得仇恨时发出声音警报",
	["Toggle on/off audio alert on aggro."] = "切换是否在获得仇恨时发出声音警报。",
	["Log range"] = "记录范围",
	["Changes combat log range. Set it to your max healing range"] = "设定战斗记录范围。设置为你治疗法术的最大施法距离。",
	["Version Query"] = "版本查询",
	["Checks the group for Squishy users and prints their version data."] = "检查队伍/团队内Squishy用户并打印他们的版本数据。",
	["Checking group for Squishy users, please wait."] = "正在检查Squishy用户，请稍候。",
	["using"] = "使用",

	-- notifications in frame
	[" is healing you."] = "正在治疗你。",
	[" healing your group."] = "正在治疗你的小组。",
	[" died."] = "死亡了。",
	
	-- frame header
	["Squishy Emergency"] = "Squishy紧急状况监视器",
	
	["Hide minimap icon"] = "隐藏小地图按钮",

	-- debuffs and other spell related locals
	["Mortal Strike"] = "致死打击",
	["Mortal Cleave"] = "致死顺劈",
	["Gehennas\' Curse"] = "基赫纳斯的诅咒",
	["Curse of the Deadwood"] = "死木诅咒",
	["Blood Fury"] = "血性狂暴",
	["Brood Affliction: Green"] = "龙血之痛：绿",
	["Necrotic Poison"] = "死灵之毒",
	["Conflagration"] = "燃烧",
	["Petrification"] = "石化",
} end)