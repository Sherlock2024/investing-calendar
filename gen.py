from icalendar import Calendar, Event, vRecur
from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo
NY=ZoneInfo("America/New_York"); SH=ZoneInfo("Asia/Shanghai")
BLS="https://www.bls.gov/schedule/2026/home.htm"; BLS27="https://www.bls.gov/schedule/2027/home.htm"
BEA="https://www.bea.gov/news/schedule (JSON: https://apps.bea.gov/API/signup/release_dates.json)"
CEN="https://www.census.gov/retail/release_schedule.html"; ISM="https://www.ismworld.org/supply-management-news-and-reports/reports/rob-report-calendar/"
FED="https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"; NYSE="https://www.nyse.com/markets/hours-calendars"
DOL="https://www.dol.gov/ui/data.pdf"
AF="https://afterns.com/en/calendar/monthly/"
ev=[]  # (cat, uid, title, start, end_or_None, desc, allday)
def T(cat,uid,title,d,hm,src,note="",dur=30):
    s=datetime(*d,*hm,tzinfo=NY)
    desc=f"美东时间: {s:%Y-%m-%d %H:%M} ET\n北京时间: {s.astimezone(SH):%Y-%m-%d %H:%M}\n{note}\n来源: {src}".replace("\n\n","\n")
    ev.append((cat,uid,title,s.astimezone(SH),s.astimezone(SH)+timedelta(minutes=dur),desc,False))
def A(cat,uid,title,d,src,note=""):
    ev.append((cat,uid,title,date(*d),date(*d)+timedelta(1),f"{note}\n来源: {src}".strip(),True))
for d,m,s in [((2026,11,10),"10月",BLS),((2026,12,10),"11月",BLS),((2027,1,13),"12月",BLS27),((2027,2,11),"1月",BLS27),((2027,3,10),"2月",BLS27)]:
    T("宏观","cpi-%04d%02d%02d"%d+"@investing",f"美国{m}CPI",d,(8,30),s)
for d,m,s in [((2026,11,13),"10月",BLS),((2026,12,15),"11月",BLS),((2027,1,14),"12月",BLS27),((2027,2,12),"1月",BLS27),((2027,3,12),"2月",BLS27)]:
    T("宏观","ppi-%04d%02d%02d"%d+"@investing",f"美国{m}PPI",d,(8,30),s)
for d,m,s in [((2026,11,6),"10月",BLS),((2026,12,4),"11月",BLS),((2027,1,8),"12月",BLS27),((2027,2,5),"1月",BLS27),((2027,3,5),"2月",BLS27)]:
    T("宏观","nfp-%04d%02d%02d"%d+"@investing",f"美国{m}非农就业报告",d,(8,30),s)
for d,m in [((2026,11,3),"9月"),((2026,12,1),"10月")]:
    T("宏观","jolts-%04d%02d%02d"%d+"@investing",f"美国{m}JOLTS职位空缺",d,(10,0),"https://www.bls.gov/schedule/news_release/jolts.htm")
for d,p,g in [((2026,11,25),"10月","三季度GDP修正值(第二次估算)"),((2026,12,23),"11月","三季度GDP终值(第三次估算)"),((2027,1,28),"12月","四季度GDP初值"),((2027,2,25),"1月","四季度GDP修正值"),((2027,3,31),"2月","四季度GDP终值")]:
    n="2027年日期与时间已由BEA官方JSON列出；GDP初值/修正值/终值轮次按BEA惯例标注" if d[0]==2027 else ""
    T("宏观","pce-%04d%02d%02d"%d+"@investing",f"美国{p}PCE/个人收入与支出",d,(8,30),BEA)
    T("宏观","gdp-%04d%02d%02d"%d+"@investing",f"美国{g}",d,(8,30),BEA,n)
for d,m in [((2026,11,17),"10月"),((2026,12,16),"11月"),((2027,1,15),"12月"),((2027,2,17),"1月"),((2027,3,16),"2月")]:
    T("宏观","retail-%04d%02d%02d"%d+"@investing",f"美国{m}零售销售",d,(8,30),CEN,"Census Advance Monthly Retail Trade Report")
for d,m in [((2026,11,2),"10月"),((2026,12,1),"11月")]:
    T("宏观","ismm-%04d%02d%02d"%d+"@investing",f"ISM{m}制造业PMI",d,(10,0),ISM)
for d,m in [((2026,11,4),"10月"),((2026,12,3),"11月")]:
    T("宏观","isms-%04d%02d%02d"%d+"@investing",f"ISM{m}服务业PMI",d,(10,0),ISM)
for d,m,k in [((2027,1,4),"12月","制造业"),((2027,2,1),"1月","制造业"),((2027,3,1),"2月","制造业"),((2027,1,6),"12月","服务业"),((2027,2,3),"1月","服务业"),((2027,3,3),"2月","服务业")]:
    A("宏观","ism%s-%04d%02d%02d"%(("m" if k=="制造业" else "s"),*d)+"@investing",f"(预计) ISM{m}{k}PMI",d,ISM,"ISM尚未公布2027年日程；按ISM规则（制造业=每月第1个工作日，服务业=第3个工作日，10:00 ET）推算。10:00 EST = 北京时间23:00")
# FOMC
for d,nm in [((2026,12,9),"12月"),((2027,1,27),"1月"),((2027,3,17),"3月")]:
    T("FOMC","fomc-stmt-%04d%02d%02d"%d+"@investing",f"FOMC{nm}利率决议/声明",d,(14,0),FED,"会议为两天，第二天14:00 ET发布声明"+("；附经济预测(SEP)" if nm in("12月","3月") else ""))
    T("FOMC","fomc-pc-%04d%02d%02d"%d+"@investing",f"美联储主席新闻发布会({nm}FOMC)",d,(14,30),FED,"按惯例声明后30分钟举行",dur=60)
for d,nm in [((2026,11,18),"10月"),((2026,12,30),"12月"),((2027,2,17),"1月")]:
    T("FOMC","fomc-min-%04d%02d%02d"%d+"@investing",f"(预计) FOMC{nm}会议纪要",d,(14,0),FED,"预计：按会后三周惯例推算，美联储未在日历页列出具体日期")
# holidays
for d,n in [((2026,11,26),"感恩节"),((2026,12,25),"圣诞节"),((2027,1,1),"元旦"),((2027,1,18),"马丁路德金纪念日"),((2027,2,15),"总统日"),((2027,3,26),"耶稣受难日")]:
    A("休市","nyse-closed-%04d%02d%02d"%d+"@investing",f"美股休市（{n}）",d,NYSE)
for d,n in [((2026,11,27),"感恩节次日"),((2026,12,24),"平安夜")]:
    T("休市","nyse-early-%04d%02d%02d"%d+"@investing",f"美股提前收盘13:00 ET（{n}）",d,(13,0),NYSE,"NYSE 13:00 ET 提前收盘（期权13:15）",dur=15)
# earnings confirmed
T("财报","er-aapl-20261102@investing","苹果财报 FY26Q4（盘后）",(2026,11,2),(16,30),"https://investor.apple.com/investor-relations/event-details/2026/FY-26-Fourth-Quarter-Results/default.aspx","公司已确认：财报16:30 ET发布，电话会17:00 ET",dur=60)
T("财报","er-amd-20261103@investing","AMD财报 Q3（盘后）",(2026,11,3),(17,0),"https://ir.amd.com/news-events/ir-calendar/detail/20261103-amd-fiscal-third-quarter-2026-financial-results","公司已确认：盘后发布，电话会17:00 ET（所示时间为电话会）",dur=60)
T("财报","er-nvda-20261117@investing","英伟达财报 FY27Q3（盘后）",(2026,11,17),(16,20),"https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Sets-Conference-Call-for-Third-Quarter-Financial-Results/default.aspx","公司已确认：约16:20 ET发布，电话会17:00 ET",dur=60)
T("财报","er-avgo-20261209@investing","博通财报 FY26Q4（盘后）",(2026,12,9),(17,0),"https://www.fool.com/earnings/call-transcripts/2026/09/09/broadcom-avgo-q3-2026-earnings-call-transcript/ ; https://investors.broadcom.com","公司已确认（IR负责人Ji Yoo于FQ3电话会宣布）：12/9美股盘后发布，电话会14:00 PT/17:00 ET（所示时间为电话会；新闻稿通常约16:15 ET）。原预计12/10，已更正",dur=60)
T("财报","er-jpm-20270114@investing","摩根大通财报 Q4（盘前）",(2027,1,14),(6,45),"https://www.jpmorganchase.com/ir","公司已确认：约06:45 ET发布，电话会08:30 ET",dur=105)
for d,co,tm,code in [((2026,12,14),"甲骨文","盘后","orcl"),((2026,12,23),"美光","盘后","mu"),((2027,1,14),"台积电","美股盘前","tsm"),((2027,1,14),"摩根士丹利","盘前","ms"),((2027,1,19),"高盛","盘前","gs"),((2027,1,19),"奈飞","盘后","nflx"),((2027,1,27),"微软","盘后","msft"),((2027,1,27),"特斯拉","盘后","tsla"),((2027,1,27),"Meta","盘后","meta"),((2027,1,28),"英特尔","盘后","intc"),((2027,2,3),"谷歌Alphabet","盘后","googl"),((2027,2,4),"亚马逊","盘后","amzn")]:
    A("财报",f"er-{code}-%04d%02d%02d"%d+"@investing",f"(预计) {co}财报（{tm}）",d,AF+"%04d-%02d"%d[:2]+" ; https://www.wallstreethorizon.com","公司尚未确认，日期为第三方财报日历预测，可能变动。注意：美东盘后≈北京时间次日早晨")

# ===== 市场预期数据（每日更新此处；uid -> (标题后缀, 预期说明, 来源)）=====
EXP_DATE="2026-11-03"
EXP_NEW="2026-11-12"
# uid -> last expectation refresh date (overrides EXP_DATE/EXP_NEW when present)
EXP_UPDATED={
"er-aapl-20261102@investing":"2026-11-04",
"er-amd-20261103@investing":"2026-11-04",
"retail-20261117@investing":"2026-11-12",
"jolts-20261103@investing":"2026-11-04",
"ismm-20261102@investing":"2026-11-03",
"isms-20261104@investing":"2026-11-05",
"er-avgo-20261209@investing":"2026-11-02",
"er-orcl-20261214@investing":"2026-11-02",
"er-mu-20261223@investing":"2026-11-02",
"er-jpm-20270114@investing":"2026-11-02",
"er-gs-20270119@investing":"2026-11-02",
"er-ms-20270114@investing":"2026-11-02",
"er-msft-20270127@investing":"2026-11-02",
"er-tsla-20270127@investing":"2026-11-02",
"er-meta-20270127@investing":"2026-11-02",
"er-intc-20270128@investing":"2026-11-02",
"er-googl-20270203@investing":"2026-11-02",
"er-amzn-20270204@investing":"2026-11-02",
"er-tsm-20270114@investing":"2026-11-02",
"nfp-20261106@investing":"2026-11-07",
"cpi-20261110@investing":"2026-11-11",
"ppi-20261113@investing":"2026-11-12",
"pce-20261125@investing":"2026-11-08",
"gdp-20261125@investing":"2026-11-08",
"fomc-stmt-20261209@investing":"2026-11-12",
"fomc-stmt-20270127@investing":"2026-11-07",
"fomc-stmt-20270317@investing":"2026-11-07",
"er-nvda-20261117@investing":"2026-11-12",
}
REFRESHED=set(k for k,v in EXP_UPDATED.items() if v==EXP_NEW)
EXP={
"er-aapl-20261102@investing":("（实际EPS $2.10/营收$1144.8亿；预期$1.99/$1134亿）","已公布：FQ4营收$1144.8亿（+12% YoY，高于一致预期约$1134亿）、EPS $2.10（+14% YoY，高于一致预期$1.99）；iPhone销售强劲但大中华区营收低于预期。赛前一致预期：营收约$1133–1134亿，EPS $1.98–1.99","Apple Newsroom、MarketBeat、Investing.com、Yahoo Finance 2026-11-04查"),
"ppi-20261113@investing":("（预期环比+0.4%）","一致预期：最终需求PPI环比约+0.4%（TD Economics/Bloomberg、Investing.com/Econvitals/MarketScreener等；前值实际+1.3%）。核心PPI环比预期约+0.3%（9月约+0.7%；gov.house核心同比约4.9%，前值5.0%）。WSJ调查（11/9更新，20位经济学家）整体环比+0.4%、核心+0.3%、剔除食品能源及贸易+0.3%，同比整体约+6.6%；高盛预计+0.3%/+0.2%；Briefing.com共识+0.4%/+0.3%。Bloomberg（11/8）预计整体同比升至约6.6%（近四年最陡；此前Continuum估约6.7%，前值6.3%）。11/13 21:30北京时间公布","TD Economics、Bloomberg、gov.house、Dow Jones/WSJ(11/11：环比+0.4%、核心+0.3%、同比+6.6%)、StockTitan、Trade2Spike 2026-11-12查"),
"er-amd-20261103@investing":("（实际EPS $2.09/营收$133.8亿；预期$1.95/$130.9亿）","已公布（11/3盘后）：Q3营收$133.77亿（+45% YoY，一致预期约$130.6–130.9亿），调整后EPS $2.09（+74% YoY，一致预期$1.94–1.95），GAAP EPS $1.46；数据中心营收创纪录$85亿（+97%，预期$82亿）；Q4指引营收约$170亿±3%（分析师预期$162.3亿），非GAAP毛利率约55%；CEO称2027年营收增长超80%（分析师预期77%）；财报后盘后股价约+8%","AMD IR新闻稿、CNBC(LSEG)、Reuters/Investing.com 2026-11-04查"),
"er-nvda-20261117@investing":("（预期EPS ~$2.47–2.49/营收~$1088–1092亿）","一致预期：营收约$1088–1092亿（MarketBeat $108.8B；Yahoo/Zacks $108.99B；LSEG $109.2B），调整后EPS约$2.47–2.49（MarketBeat 2.47；LSEG 2.48；Zacks 2.49，30天上修0.61%）；同比约+91%。公司指引营收$1080亿±2%（不含中国数据中心计算收入），毛利率74%±0.5pt。关注：黄仁勋治理风波、Vera Rubin放量、毛利率压力。11/17盘后约16:20 ET发布，电话会17:00 ET","MarketBeat、Yahoo Finance/Zacks、IG(LSEG)、Investing.com 2026-11-12查"),
"er-avgo-20261209@investing":("（预期EPS ~$3.83–3.90）","一致预期：营收约$349–356亿，调整后EPS约$3.82–3.90（Backpack/drillr $3.82–3.83；FXEmpire/hulicalendar $355.7亿/$3.90）；公司指引营收约$348亿、AI半导体营收$217亿","Backpack/drillr/FXEmpire/hulicalendar、Broadcom IR 2026-11-02查"),
"er-orcl-20261214@investing":("（预期EPS $1.89）","一致预期：营收约$213.3亿，调整后EPS $1.89；公司指引EPS $1.85–1.93，营收同比+30%~34%","Backpack/TipRanks、CNBC(2026-09-10) 2026-11-02查"),
"er-mu-20261223@investing":("（预期EPS ~$38.2）","一致预期：营收约$615–617亿，EPS约$38.20–38.29；公司指引营收$615亿±15亿，EPS $38.15±1.00","micronstock.com/Theta Research、Micron IR 2026-11-02查"),
"er-jpm-20270114@investing":("","一致预期：营收约$511亿，EPS约$5.89–5.91","Benzinga/Investing.com 2026-11-02查（远期，波动大）"),
"er-gs-20270119@investing":("","一致预期：营收约$172亿，EPS约$16.50","BusinessQuant 2026-11-02查（单一来源，待核实）"),
"er-ms-20270114@investing":("","一致预期：营收约$202亿，EPS约$2.95","Backpack 2026-11-02查（单一来源，待核实）"),
"er-msft-20270127@investing":("","一致预期（2026年12月季）：营收约$900亿，EPS约$4.74","ADVFN/TipRanks 2026-11-02查（单一来源，待核实）"),
"er-tsla-20270127@investing":("","一致预期：营收约$293亿，EPS约$0.50","Theta Research 2026-11-02查（单一来源，待核实）"),
"er-meta-20270127@investing":("","一致预期：营收约$584亿，EPS约$8.17","搜索汇总(Investopedia相关) 2026-11-02查（单一来源，待核实）"),
"er-intc-20270128@investing":("","一致预期：营收约$171亿，EPS约$0.44（注：英特尔Q4指引$150–160亿，预期可能下修）","Yahoo Finance 2026-11-02查；指引见TradingKey"),
"er-googl-20270203@investing":("","一致预期：营收约$1424亿，EPS约$3.21","Yahoo Finance 2026-11-02查"),
"er-amzn-20270204@investing":("","一致预期：营收约$2443亿，EPS约$2.44","Yahoo Finance 2026-11-02查"),
"er-tsm-20270114@investing":("","公司指引Q4营收$523–543亿；EPS一致预期暂无可靠来源","SharpeIQ引述TSMC指引 2026-11-02查"),
"fomc-stmt-20261209@investing":("（市场押注加息25bp，概率约88–91%；另有约9–12%押注50bp）","当前目标区间3.75%–4.00%（10/28以10-2投票维持不变）。CME FedWatch（11/12）：12月加息25bp至4.00%–4.25%概率约88.4%–90.8%、加息50bp至4.25%–4.50%约9.2%–11.6%、维持不变0%（盘中不同时点有差异）；一周前约72%加息、23%维持。到1月累计：加50bp 61.9%、加25bp 30.6%、加75bp 7.6%（FXBus 11/12）。理事Waller主张12月加息、若通胀恶化可更大幅；达拉斯联储Logan称需至少再加两次25bp。2年期美债收益率周二升17bp，10年期约4.98%。12/9 14:00 ET公布","CME FedWatch(经Investing.com、ATFX、FXBus、Financial World) 2026-11-12查"),
"fomc-stmt-20270127@investing":("","FinBoss（11/7，基于延迟联邦基金期货自算，可与CME差几个百分点）：1月会后目标区间落在4.00%–4.25%概率约96%、仍在3.75%–4.00%约4%——即若12月加息一次，1月大概率按兵不动。非农前（FXBus/CME 11/6附近）曾为：累计维持27.0%、累计+25bp 63.6%、累计+50bp 9.5%。路径已随非农重新上修，但仍以“到1月共加一次”为主","FinBoss 2026-11-07查；对照CME FedWatch经FXBus 11/6（远期）"),
"fomc-stmt-20270317@investing":("","非农后路径上修：The Edge引CME（11/6）：至3月累计至少加息一次概率89.1%（前值83.1%）、累计至少两次42.8%（前值34.7%）、维持不变10.9%。FinBoss（11/7）：3月会后落在4.00%–4.25%约64%、4.25%–4.50%约36%。至2027年12月，最可能区间为4.25%–4.50%（约36.4%），累计至少两次加息概率约62.2%（11/5为54.0%）","CME FedWatch(经The Edge 11/6)、FinBoss 2026-11-07查（远期）"),
"retail-20261117@investing":("（预期环比+0.6%，扣汽车+0.5%）","10月零售销售一致预期：整体环比+0.6%（gov.house共识；Continuum预测+0.2%，Kalshi市场对>0.2%概率约64%）；扣汽车+0.5%（Continuum预测+0.4%）；扣汽油与汽车+0.3%；控制组+0.1%。前值（9月）整体+0.8%（预期+0.4%，其中汽油站贡献约71%增量）、扣汽车+0.9%。11/17 21:30北京时间公布。分歧较大，仅供参考","gov.house共识、Continuum Economics、Kalshi 2026-11-12查"),
"nfp-20261106@investing":("（实际 +16.5万/失业率4.1%；预期约+5.9~6.5万）","已公布（11/6 08:30 ET）：非农新增就业+16.5万（远超华尔街预期：CNBC/Dow Jones约+5.9万、Haver/共识约+6.5万、Reuters调查中位数约+6.5万）；失业率降至4.1%（预期4.2%，前值4.2%）；平均时薪环比+0.4%、同比+3.1%（预期分别+0.3%/+2.9%）；平均工时34.4小时持平。8月上修至+18.6万（+5.3万）、9月上修至+6.0万（+3.1万），合计上修+8.4万。专业商务服务+7.0万、医疗保健约+4.2~5.5万、制造业+1.9万；劳动力增加42.1万、劳动参与率升至61.9%；U-6升至7.9%（+0.3pt）。11月非农预计12/4公布","BLS、CNBC、Haver Analytics、Reuters/MarketScreener 2026-11-07查"),
"jolts-20261103@investing":("（实际752.3万/预期716万）","已公布：9月职位空缺752.3万（预期约715–716万，Dow Jones 715万、Econoday 716万、Reuters 710万；8月上修至719.0万），环比+33.3万，职位空缺率4.5%；离职人数336.5万（18个月新高）、招聘540.2万、裁员164.1万（自2025年3月以来最低）。每1名失业者对应约1.05个空缺。10月JOLTS将于12/1公布","BLS、CNBC、Econoday(CME)、Quartz 2026-11-04查"),
"ismm-20261102@investing":("（实际55.5/预期54.6）","已公布：10月制造业PMI 55.5（一致预期54.6，前值54.5），连续第10个月扩张；价格支付指数75.2（预期77.0，前值77.9）；就业52.4（预期53.0）；新订单55.5","Sigmanomics经济日历、FXStreet 2026-11-03查"),
"isms-20261104@investing":("（实际54.5/预期54.8）","已公布（11/4 23:00北京时间）：10月服务业PMI 54.5（Reuters调查预期54.8，Action Economics预期54.7，Dow Jones预期54.6；前值54.9），连续第28个月扩张、为三个月低点；商业活动指数53.8（前值56.5）、新订单55.9（前值59.8）、就业51.4（前值50.1）、价格指数73.0（前值74.0）。ISM称关税与燃料成本是最主要的供应链问题。11月数据将于12/3公布","ISM官网、Reuters/Investing.com、Haver Analytics、Forex Factory 2026-11-05查"),
"cpi-20261110@investing":("（实际环比+0.4%/核心+0.3%；预期+0.3%/+0.2%）","已公布（11/10 08:30 ET）：10月CPI环比+0.4%（Dow Jones/Reuters预期+0.3%；9月+0.6%），连续第三个月涨幅≥0.4%；核心CPI环比+0.3%（预期+0.2%；9月+0.3%），连续第三个月+0.3%。BLS因2025年10月停摆无同比官方数字；Reuters引经济学家估计核心同比约2.8%（9月2.6%）。数据高于预期，推升12月加息预期","CNBC、Reuters/Investing.com 2026-11-11查"),
"pce-20261125@investing":("（Nowcast环比约+0.27%）","暂无统一街市共识。克利夫兰联储Nowcast（11/6更新，周末无新值）：10月PCE环比+0.27%、核心+0.26%；同比模型估计3.77%/核心3.20%。前值（9月，10/29公布）：PCE环比+0.5%/同比3.6%，核心环比+0.3%/同比3.1%。11/25 21:30北京时间与三季度GDP修正值同日公布","Cleveland Fed Nowcasting(11/6)、gov.house、BEA 2026-11-08查"),
"gdp-20261125@investing":("（初值年化+3.4%）","三季度GDP初值（10/29已公布）年化增长3.4%（当时一致预期约3.2%）。11/25公布第二次估算；第二次估算的街市共识暂无权威来源。BEA官方JSON确认发布日期为11/25 08:30 ET","BEA、gov.house经济日历 2026-11-08查"),
}
CLAIMS_EXP="11/12（截至11/7当周，今晚21:30北京时间公布）一致预期：初请约19.5–19.6万（WSJ/Dow Jones 19.6万，6位经济学家；gov.house共识19.5万、模型19.1万；前值18.9万）；续请约172.0万（前值171.8万）——WSJ(经MarketScreener 11/6)、gov.house 2026-11-12查。上周（11/5）实际初请18.9万、续请171.8万"
def addexp(uid,title,desc,cat):
    if uid in EXP:
        suf,txt,src=EXP[uid]
        when=EXP_UPDATED.get(uid, EXP_NEW if uid in REFRESHED else EXP_DATE)
        return title+suf, desc+f"\n预期：{txt}\n预期来源: {src}\n预期更新于 {when}"
    if cat in("宏观","财报") or uid.startswith("fomc-stmt"):
        return title, desc+"\n预期：暂无（临近时更新）"
    return title,desc
cal=Calendar(); cal.add("prodid","-//Investing//sherlock//CN"); cal.add("version","2.0"); cal.add("calscale","GREGORIAN")
cal.add("x-wr-calname","Investing"); cal.add("x-wr-timezone","Asia/Shanghai")
stamp=datetime(2026,11,9,11,0,tzinfo=ZoneInfo("UTC"))
def mk(uid,title,s,e,desc,allday):
    x=Event(); x.add("uid",uid); x.add("dtstamp",stamp); x.add("summary",title); x.add("dtstart",s); x.add("dtend",e); x.add("description",desc)
    if allday: x.add("transp","TRANSPARENT")
    return x
for c,u,t,s,e,d,a in ev:
    t,d=addexp(u,t,d,c); cal.add_component(mk(u,t,s,e,d,a))
# jobless claims
cn="美国劳工部(DOL)每周四08:30 ET发布；节假日可能调整"
x=mk("claims-weekly-est@investing","美国初请失业金人数",datetime(2026,11,5,21,30,tzinfo=SH),datetime(2026,11,5,22,0,tzinfo=SH),"美东时间: 每周四 08:30 ET（冬令时=北京21:30）\n"+cn+"\n感恩节周预计改为周三11/25\n来源: "+DOL+"\n预期："+CLAIMS_EXP+"\n预期更新于 "+EXP_NEW,False)
x.add("rrule",{"freq":"weekly","byday":"TH","until":datetime(2027,3,11,13,30,tzinfo=ZoneInfo("UTC"))}); x.add("exdate",datetime(2026,11,26,21,30,tzinfo=SH)); cal.add_component(x)
x=mk("claims-weekly-edt@investing","美国初请失业金人数",datetime(2027,3,18,20,30,tzinfo=SH),datetime(2027,3,18,21,0,tzinfo=SH),"美东时间: 每周四 08:30 ET（夏令时=北京20:30）\n"+cn+"\n来源: "+DOL,False)
x.add("rrule",{"freq":"weekly","byday":"TH","until":datetime(2027,3,25,12,30,tzinfo=ZoneInfo("UTC"))}); cal.add_component(x)
T("宏观","claims-20261125@investing","(预计) 美国初请失业金人数（感恩节提前）",(2026,11,25),(8,30),DOL,"感恩节周按惯例提前至周三，待DOL确认")
_c,_u,_t,_s,_e,_d,_a=ev[-1]; _t,_d=addexp(_u,_t,_d,_c); cal.add_component(mk(_u,_t,_s,_e,_d,_a))
cal.add_missing_timezones()
open("Investing.ics","wb").write(cal.to_ical())
c2=Calendar.from_ical(open("Investing.ics","rb").read()); vs=c2.walk("VEVENT")
uids=[str(v["uid"]) for v in vs]; assert len(uids)==len(set(uids))
from collections import Counter; print(len(vs),Counter(e[0] for e in ev)+Counter({"宏观(初请重复)":2}))
for c,u,t,s,e,d,a in sorted(ev,key=lambda z:str(z[3])):
    if str(s)[:10]<="2026-11-20": print(str(s)[:16],t)
