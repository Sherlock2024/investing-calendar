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
for d,m,s in [((2026,11,10),"10月",BLS),((2026,12,10),"11月",BLS),((2027,1,13),"12月",BLS27),((2027,2,11),"1月",BLS27),((2027,3,10),"2月",BLS27),((2027,4,13),"3月",BLS27)]:
    T("宏观","cpi-%04d%02d%02d"%d+"@investing",f"美国{m}CPI",d,(8,30),s)
for d,m,s in [((2026,11,13),"10月",BLS),((2026,12,15),"11月",BLS),((2027,1,14),"12月",BLS27),((2027,2,12),"1月",BLS27),((2027,3,12),"2月",BLS27),((2027,4,14),"3月",BLS27)]:
    T("宏观","ppi-%04d%02d%02d"%d+"@investing",f"美国{m}PPI",d,(8,30),s)
for d,m,s in [((2026,11,6),"10月",BLS),((2026,12,4),"11月",BLS),((2027,1,8),"12月",BLS27),((2027,2,5),"1月",BLS27),((2027,3,5),"2月",BLS27),((2027,4,2),"3月",BLS27)]:
    T("宏观","nfp-%04d%02d%02d"%d+"@investing",f"美国{m}非农就业报告",d,(8,30),s)
for d,m,s in [((2026,11,3),"9月","https://www.bls.gov/schedule/news_release/jolts.htm"),((2026,12,1),"10月","https://www.bls.gov/schedule/news_release/jolts.htm"),((2027,1,5),"11月",BLS27),((2027,2,2),"12月",BLS27),((2027,3,9),"1月",BLS27),((2027,3,30),"2月",BLS27)]:
    T("宏观","jolts-%04d%02d%02d"%d+"@investing",f"美国{m}JOLTS职位空缺",d,(10,0),s)
for d,p,g in [((2026,11,25),"10月","三季度GDP修正值(第二次估算)"),((2026,12,23),"11月","三季度GDP终值(第三次估算)"),((2027,1,28),"12月","四季度GDP初值"),((2027,2,25),"1月","四季度GDP修正值"),((2027,3,31),"2月","四季度GDP终值"),((2027,4,29),"3月","一季度GDP初值")]:
    n="2027年日期与时间已由BEA官方JSON列出；GDP初值/修正值/终值轮次按BEA惯例标注" if d[0]==2027 else ""
    T("宏观","pce-%04d%02d%02d"%d+"@investing",f"美国{p}PCE/个人收入与支出",d,(8,30),BEA)
    T("宏观","gdp-%04d%02d%02d"%d+"@investing",f"美国{g}",d,(8,30),BEA,n)
for d,m in [((2026,11,17),"10月"),((2026,12,16),"11月"),((2027,1,15),"12月"),((2027,2,17),"1月"),((2027,3,16),"2月"),((2027,4,16),"3月")]:
    T("宏观","retail-%04d%02d%02d"%d+"@investing",f"美国{m}零售销售",d,(8,30),CEN,"Census Advance Monthly Retail Trade Report")
for d,m in [((2026,11,2),"10月"),((2026,12,1),"11月")]:
    T("宏观","ismm-%04d%02d%02d"%d+"@investing",f"ISM{m}制造业PMI",d,(10,0),ISM)
for d,m in [((2026,11,4),"10月"),((2026,12,3),"11月")]:
    T("宏观","isms-%04d%02d%02d"%d+"@investing",f"ISM{m}服务业PMI",d,(10,0),ISM)
for d,m,k in [((2027,1,4),"12月","制造业"),((2027,2,1),"1月","制造业"),((2027,3,1),"2月","制造业"),((2027,4,1),"3月","制造业"),((2027,1,6),"12月","服务业"),((2027,2,3),"1月","服务业"),((2027,3,3),"2月","服务业"),((2027,4,5),"3月","服务业")]:
    A("宏观","ism%s-%04d%02d%02d"%(("m" if k=="制造业" else "s"),*d)+"@investing",f"(预计) ISM{m}{k}PMI",d,ISM,"ISM尚未公布2027年日程；按ISM规则（制造业=每月第1个工作日，服务业=第3个工作日，10:00 ET）推算。冬令时10:00 EST=北京23:00，2027-03-14起夏令时10:00 EDT=北京22:00")
# FOMC
for d,nm in [((2026,12,9),"12月"),((2027,1,27),"1月"),((2027,3,17),"3月"),((2027,4,28),"4月")]:
    T("FOMC","fomc-stmt-%04d%02d%02d"%d+"@investing",f"FOMC{nm}利率决议/声明",d,(14,0),FED,"会议为两天，第二天14:00 ET发布声明"+("；附经济预测(SEP)" if nm in("12月","3月") else "")+("。美联储2026-11-12宣布修订后的2027年暂定日程，4/27–28为常规议息会议" if nm=="4月" else ""))
    T("FOMC","fomc-pc-%04d%02d%02d"%d+"@investing",f"美联储主席新闻发布会({nm}FOMC)",d,(14,30),FED,"按惯例声明后30分钟举行",dur=60)
for d,nm in [((2026,11,18),"10月"),((2026,12,30),"12月"),((2027,2,17),"1月")]:
    T("FOMC","fomc-min-%04d%02d%02d"%d+"@investing",f"FOMC{nm}会议纪要",d,(14,0),FED,"美联储官网货币政策页Upcoming Dates已正式列出该发布日，14:00 ET（https://www.federalreserve.gov/monetarypolicy.htm）")
# holidays
for d,n in [((2026,11,26),"感恩节"),((2026,12,25),"圣诞节"),((2027,1,1),"元旦"),((2027,1,18),"马丁路德金纪念日"),((2027,2,15),"总统日"),((2027,3,26),"耶稣受难日")]:
    A("休市","nyse-closed-%04d%02d%02d"%d+"@investing",f"美股休市（{n}）",d,NYSE)
for d,n in [((2026,11,27),"感恩节次日"),((2026,12,24),"平安夜")]:
    T("休市","nyse-early-%04d%02d%02d"%d+"@investing",f"美股提前收盘13:00 ET（{n}）",d,(13,0),NYSE,"NYSE 13:00 ET 提前收盘（期权13:15）",dur=15)
# earnings confirmed
T("财报","er-aapl-20261102@investing","苹果财报 FY26Q4（盘后）",(2026,11,2),(16,30),"https://investor.apple.com/investor-relations/event-details/2026/FY-26-Fourth-Quarter-Results/default.aspx","公司已确认：财报16:30 ET发布，电话会17:00 ET",dur=60)
T("财报","er-amd-20261103@investing","AMD财报 Q3（盘后）",(2026,11,3),(17,0),"https://ir.amd.com/news-events/ir-calendar/detail/20261103-amd-fiscal-third-quarter-2026-financial-results","公司已确认：盘后发布，电话会17:00 ET（所示时间为电话会）",dur=60)
T("财报","er-nvda-20261117@investing","英伟达财报 FY27Q3（盘后）",(2026,11,17),(16,20),"https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Sets-Conference-Call-for-Third-Quarter-Financial-Results/default.aspx","公司已确认：约16:20 ET发布，电话会17:00 ET",dur=60)
T("财报","er-avgo-20261209@investing","博通财报 FY26Q4（盘后）",(2026,12,9),(17,0),"https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announce-fourth-quarter-and-fiscal-year-2026","公司已确认（2026-11-09官方新闻稿）：12/9美股收盘后发布财报及展望，电话会14:00 PT/17:00 ET（所示时间为电话会）",dur=60)
T("财报","er-jpm-20270114@investing","摩根大通财报 Q4（盘前）",(2027,1,14),(6,45),"https://www.jpmorganchase.com/ir","公司已确认：约06:45 ET发布，电话会08:30 ET",dur=105)
for d,co,tm,code in [((2026,12,14),"甲骨文","盘后","orcl"),((2026,12,23),"美光","盘后","mu"),((2027,1,14),"台积电","美股盘前","tsm"),((2027,1,14),"摩根士丹利","盘前","ms"),((2027,1,19),"高盛","盘前","gs"),((2027,1,19),"奈飞","盘后","nflx"),((2027,1,27),"微软","盘后","msft"),((2027,1,27),"特斯拉","盘后","tsla"),((2027,1,27),"Meta","盘后","meta"),((2027,1,28),"英特尔","盘后","intc"),((2027,2,3),"谷歌Alphabet","盘后","googl"),((2027,2,4),"亚马逊","盘后","amzn")]:
    A("财报",f"er-{code}-%04d%02d%02d"%d+"@investing",f"(预计) {co}财报（{tm}）",d,AF+"%04d-%02d"%d[:2]+" ; https://www.wallstreethorizon.com","公司尚未确认，日期为第三方财报日历预测，可能变动。注意：美东盘后≈北京时间次日早晨")

# ===== 市场预期数据（每日更新此处；uid -> (标题后缀, 预期说明, 来源)）=====
EXP_DATE="2026-11-03"
EXP_NEW="2026-11-19"
# uid -> last expectation refresh date (overrides EXP_DATE/EXP_NEW when present)
EXP_UPDATED={
"er-aapl-20261102@investing":"2026-11-04",
"er-amd-20261103@investing":"2026-11-04",
"retail-20261117@investing":"2026-11-18",
"jolts-20261103@investing":"2026-11-04",
"ismm-20261102@investing":"2026-11-03",
"isms-20261104@investing":"2026-11-05",
"er-avgo-20261209@investing":"2026-11-15",
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
"ppi-20261113@investing":"2026-11-14",
"pce-20261125@investing":"2026-11-19",
"gdp-20261125@investing":"2026-11-18",
"fomc-stmt-20261209@investing":"2026-11-19",
"fomc-stmt-20270127@investing":"2026-11-19",
"fomc-stmt-20270317@investing":"2026-11-19",
"er-nvda-20261117@investing":"2026-11-18",
"jolts-20261201@investing":"2026-11-13",
"fomc-stmt-20270428@investing":"2026-11-19",
"nfp-20261204@investing":"2026-11-17",
}

REFRESHED=set(k for k,v in EXP_UPDATED.items() if v==EXP_NEW)
EXP={
"er-aapl-20261102@investing":("（实际EPS $2.10/营收$1144.8亿；预期$1.99/$1134亿）","已公布：FQ4营收$1144.8亿（+12% YoY，高于一致预期约$1134亿）、EPS $2.10（+14% YoY，高于一致预期$1.99）；iPhone销售强劲但大中华区营收低于预期。赛前一致预期：营收约$1133–1134亿，EPS $1.98–1.99","Apple Newsroom、MarketBeat、Investing.com、Yahoo Finance 2026-11-04查"),
"ppi-20261113@investing":("（实际环比+0.3%/同比+6.5%；预期+0.4%，核心+0.3%符合预期）","已公布（11/13 08:30 ET）：最终需求PPI环比+0.3%（Dow Jones共识+0.4%；9月修订后为+1.4%），同比+6.5%（为2022年11月+7.4%以来最大升幅）。核心PPI（剔除食品和能源）环比+0.3%，符合预期，同比+5.0%（与9月持平，Haver）。BLS口径“剔除食品、能源和贸易服务”环比+0.5%（与9月相同），同比+4.9%。分项：商品+0.5%、服务+0.2%、食品+1.3%、能源-0.1%；商品（剔食品能源）+0.5%。11月PPI将于12/15 08:30 ET公布","BLS官网新闻稿、CNBC、Haver Analytics 2026-11-14查"),
"er-amd-20261103@investing":("（实际EPS $2.09/营收$133.8亿；预期$1.95/$130.9亿）","已公布（11/3盘后）：Q3营收$133.77亿（+45% YoY，一致预期约$130.6–130.9亿），调整后EPS $2.09（+74% YoY，一致预期$1.94–1.95），GAAP EPS $1.46；数据中心营收创纪录$85亿（+97%，预期$82亿）；Q4指引营收约$170亿±3%（分析师预期$162.3亿），非GAAP毛利率约55%；CEO称2027年营收增长超80%（分析师预期77%）；财报后盘后股价约+8%","AMD IR新闻稿、CNBC(LSEG)、Reuters/Investing.com 2026-11-04查"),
"er-nvda-20261117@investing":("（实际调整后EPS $2.68/营收$1158亿；预期约$2.47/$1087–1093亿）","已公布（11/17盘后）：FY27Q3营收$1158亿（环比+20%、同比+103%，远高于赛前一致预期约$1087–1093亿：Yahoo/Bloomberg $109.15B、Theta $108.71B、Visible Alpha $109.3B），GAAP每股收益$2.70、调整后EPS $2.68（预期$2.47）；数据中心营收$1076亿（环比+21%、同比+110%；彭博共识曾约$1018.5亿）。GAAP/非GAAP毛利率74.8%/74.9%（公司指引74%±0.5个百分点）。Q4（该季多一周）指引营收$1300亿±3%（不含中国数据中心计算收入），毛利率71%–72%，GAAP/非GAAP营业费用约$110亿/$107亿；并将2028财年营收增速预期上调至约75%（此前约70%）。Vera Rubin NVL72已出货。Q3向股东返还$281亿，回购额度剩余约$2273亿。董事会主席在电话会上称不考虑请黄仁勋复任CEO，已聘Heidrick & Struggles寻永久CEO。CNBC报道股价盘后上涨近4%（24/7 Wall St.报道约+2.3%）。","NVIDIA官网Q3财报新闻稿2026-11-17、CNBC 2026-11-18查"),
"er-avgo-20261209@investing":("（预期EPS ~$3.84/营收~$349亿）","公司已发官方新闻稿确认：12/9美股收盘后发布FY26Q4财报及展望，电话会14:00 PT/17:00 ET。一致预期已更新：Theta Research（数据截至11/13）营收$349.1亿、调整后EPS $3.84；与此前11/2较宽区间（营收约$349–356亿，EPS $3.82–3.90）相比，共识向约$349亿/$3.84靠拢。公司指引营收约$348亿、AI半导体营收$217亿","Broadcom IR新闻稿2026-11-09；Theta Research 2026-11-15查"),
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
"fomc-stmt-20261209@investing":("（市场押注加息25bp约93.9%，50bp约6.1%）","当前目标区间3.75%–4.00%（10/28以10-2投票维持不变）。Investing.com Fed Rate Monitor（基于CME 30天联邦基金期货，2026-11-19 05:25 AM EST更新）：12月维持在3.75%–4.00%概率为0%；加息25bp至4.00%–4.25%概率93.9%（工具所示前一日93.9%、前一周94.4%），加息50bp至4.25%–4.50%概率6.1%（前一日6.1%、前一周5.6%）。较本日历11/18早间记录（97.5%/2.5%）相比，25bp定价明显回落，50bp尾部升至6.1%；该变动出现在11/18 14:00 ET公布10月FOMC纪要之后的报价中。12/9 14:00 ET公布","Investing.com Fed Rate Monitor（CME期货，11/19 05:25 AM EST）2026-11-19查"),
"fomc-stmt-20270127@investing":("（到1月累计：加50bp约71.0%，加25bp约24.5%，加75bp约4.5%）","当前目标区间3.75%–4.00%。Investing.com Fed Rate Monitor（CME期货，2026-11-19 05:25 AM EST）：1月会后最可能落在4.25%–4.50%（71.0%，工具所示前一日71.0%；即若12月加25bp后再加一次），其次4.00%–4.25% 24.5%（前一日24.5%；12月加息后1月按兵不动），4.50%–4.75% 4.5%（前一日4.5%）。累计看：加50bp约71.0%、加25bp约24.5%、加75bp约4.5%。维持在3.75%–4.00%的概率为0%。较本日历11/18早间记录（70.5%/27.8%/1.8%）相比，+50bp略升，+25bp下降，+75bp尾部升至4.5%。1/27 14:00 ET公布","Investing.com Fed Rate Monitor（CME期货，11/19 05:25 AM EST）2026-11-19查"),
"fomc-stmt-20270317@investing":("（到3月加75bp约49.0%，加50bp约39.9%）","Investing.com Fed Rate Monitor（CME期货，2026-11-19 05:25 AM EST）：3月会后目标区间概率为4.50%–4.75% 49.0%（工具所示前一日45.1%）、4.25%–4.50% 39.9%（前一日42.6%）、4.00%–4.25% 8.1%（前一日9.5%）、4.75%–5.00% 3.0%（前一日2.7%）。即到3月累计加息三次（至4.50%–4.75%）已明显领先两次（至4.25%–4.50%）。较本日历11/18早间记录（45.0%/43.6%/10.3%/1.1%）相比，三次加息概率升至约一半，两次加息回落。3/17 14:00 ET公布","Investing.com Fed Rate Monitor（CME期货，11/19 05:25 AM EST）2026-11-19查"),
"retail-20261117@investing":("（实际整体环比+0.2%/扣汽车+0.6%；预期+0.2%/+0.4%）","已公布（11/17 08:30 ET，Census CB26-181）：10月零售与餐饮销售经季调$7482亿，环比+0.2%（90%置信区间±0.4个百分点，包含零，统计局称不足以断言确有上升；一致预期+0.2%），同比+6.8%；9月环比+0.8%未修订（$7466亿）。扣汽车+0.6%（预期+0.4%），扣汽车与汽油+0.5%（彭博/TD此前预期+0.3%），控制组（再剔除建材和餐饮）+0.6%（预期+0.4%；Reuters称9月控制组由原报+0.1%上修至+0.5%）。分项：汽车及配件-1.6%、家具-2.3%、服装-0.7%、加油站+1.5%、非店面/线上+1.2%、杂项零售+4.7%、保健个护+1.5%、建材+0.5%、餐饮+0.2%。8–10月合计同比+6.4%。下一次11月速报将于12/16公布","美国普查局CB26-181、Reuters、gov.house 2026-11-18查"),
"nfp-20261106@investing":("（实际 +16.5万/失业率4.1%；预期约+5.9~6.5万）","已公布（11/6 08:30 ET）：非农新增就业+16.5万（远超华尔街预期：CNBC/Dow Jones约+5.9万、Haver/共识约+6.5万、Reuters调查中位数约+6.5万）；失业率降至4.1%（预期4.2%，前值4.2%）；平均时薪环比+0.4%、同比+3.1%（预期分别+0.3%/+2.9%）；平均工时34.4小时持平。8月上修至+18.6万（+5.3万）、9月上修至+6.0万（+3.1万），合计上修+8.4万。专业商务服务+7.0万、医疗保健约+4.2~5.5万、制造业+1.9万；劳动力增加42.1万、劳动参与率升至61.9%；U-6升至7.9%（+0.3pt）。11月非农预计12/4公布","BLS、CNBC、Haver Analytics、Reuters/MarketScreener 2026-11-07查"),
"jolts-20261103@investing":("（实际752.3万/预期716万）","已公布：9月职位空缺752.3万（预期约715–716万，Dow Jones 715万、Econoday 716万、Reuters 710万；8月上修至719.0万），环比+33.3万，职位空缺率4.5%；离职人数336.5万（18个月新高）、招聘540.2万、裁员164.1万（自2025年3月以来最低）。每1名失业者对应约1.05个空缺。10月JOLTS将于12/1公布","BLS、CNBC、Econoday(CME)、Quartz 2026-11-04查"),
"ismm-20261102@investing":("（实际55.5/预期54.6）","已公布：10月制造业PMI 55.5（一致预期54.6，前值54.5），连续第10个月扩张；价格支付指数75.2（预期77.0，前值77.9）；就业52.4（预期53.0）；新订单55.5","Sigmanomics经济日历、FXStreet 2026-11-03查"),
"isms-20261104@investing":("（实际54.5/预期54.8）","已公布（11/4 23:00北京时间）：10月服务业PMI 54.5（Reuters调查预期54.8，Action Economics预期54.7，Dow Jones预期54.6；前值54.9），连续第28个月扩张、为三个月低点；商业活动指数53.8（前值56.5）、新订单55.9（前值59.8）、就业51.4（前值50.1）、价格指数73.0（前值74.0）。ISM称关税与燃料成本是最主要的供应链问题。11月数据将于12/3公布","ISM官网、Reuters/Investing.com、Haver Analytics、Forex Factory 2026-11-05查"),
"cpi-20261110@investing":("（实际环比+0.4%/核心+0.3%；预期+0.3%/+0.2%）","已公布（11/10 08:30 ET）：10月CPI环比+0.4%（Dow Jones/Reuters预期+0.3%；9月+0.6%），连续第三个月涨幅≥0.4%；核心CPI环比+0.3%（预期+0.2%；9月+0.3%），连续第三个月+0.3%。BLS因2025年10月停摆无同比官方数字；Reuters引经济学家估计核心同比约2.8%（9月2.6%）。数据高于预期，推升12月加息预期","CNBC、Reuters/Investing.com 2026-11-11查"),
"pce-20261125@investing":("（共识环比约+0.3%，Nowcast约+0.31%）","街市共识仍为：gov.house日历列10月PCE环比+0.3%（前值+0.5%）、核心PCE环比+0.3%（前值+0.3%）、核心同比3.2%（前值3.1%）；PCE同比尚未列街市共识。Reuters（11/17）亦称经济学家继续预期核心PCE环比连续第三个月+0.3%、同比+3.2%。克利夫兰联储Nowcast页面截至11/19早间仍标注11/18更新（每个工作日约10:00 ET；当日例行更新尚未发布）：10月PCE读数未变，仍为环比+0.31%、核心+0.27%，同比3.81%/核心3.21%。11月Nowcast亦未再变动：环比+0.17%/核心+0.26%，同比3.78%/核心3.32%；11月CPI Nowcast环比+0.07%/核心+0.21%，同比3.86%/核心2.87%。2026年四季度年化（官网11/18表格）：PCE 3.89%、核心PCE 3.38%；CPI 4.32%、核心CPI 3.40%（11/18早间记录曾写PCE 3.87%、CPI 4.28%，已按官网当前表格更正）。gov.house模型预测10月PCE同比约3.9%（区间3.7–4.0%）。前值（9月，10/29公布）：PCE环比+0.5%/同比3.6%，核心环比+0.3%/同比3.1%。11/25 21:30北京时间与三季度GDP修正值同日公布","Cleveland Fed Inflation Nowcasting（页面截至11/19早间仍标注11/18更新，当日约10:00 ET例行更新尚未发布）、gov.house、Reuters、BEA 2026-11-19查"),
"gdp-20261125@investing":("（第二次估算共识年化+3.4%，与初值持平）","三季度GDP初值（10/29已公布）年化增长3.4%（当时一致预期约3.2%）。11/25公布第二次估算；gov.house日历现已列出街市共识仍为年化+3.4%，与初值持平（Null Strategies同期亦列预报3.4%）。Reuters（11/17零售销售稿）称有迹象指向第二次估算可能上修，但尚未成为更广泛的新共识。BEA官方JSON确认发布日期为11/25 08:30 ET","gov.house经济日历、Null Strategies、BEA、Reuters 2026-11-18查"),
"jolts-20261201@investing":("（gov.house模型约750万）","暂无统一街市共识。gov.house模型预测10月职位空缺约750万（80%区间711–789万）；9月实际752.3万。12/1 10:00 ET公布","gov.house、BLS 2026-11-13查"),
"fomc-stmt-20270428@investing":("（市场定价4月会后多在4.50%–4.75%，约46.2%）","美联储11/12宣布修订后的2027年FOMC暂定日程：4/27–28为常规议息会议（声明于第二天发布，无SEP）。Investing.com Fed Rate Monitor（CME期货，2026-11-19 05:25 AM EST）：4月会后概率4.50%–4.75% 46.2%（工具所示前一日44.4%）、4.25%–4.50% 30.0%（前一日33.0%）、4.75%–5.00% 17.3%（前一日15.0%）、4.00%–4.25% 5.6%（前一日6.8%）、5.00%–5.25% 0.9%（前一日0.8%）。众数仍在4.50%–4.75%。较本日历11/18早间记录（44.6%/33.3%/14.8%/7.1%/0.3%）相比，4.50%–4.75%与4.75%–5.00%均上升。当前目标区间3.75%–4.00%。4/28 14:00 ET公布","美联储官网新闻稿2026-11-12；Investing.com Fed Rate Monitor（CME期货，11/19 05:25 AM EST）2026-11-19查"),
"nfp-20261204@investing":("（gov.house模型约+9.3万/失业率4.1%）","暂无统一街市共识与时薪预期。gov.house模型预测11月非农新增约+9.3万（80%区间-1.5万至+20.2万），失业率基线4.1%（区间4.0%–4.2%）。10月实际为新增+16.5万、失业率4.1%。12/4 08:30 ET公布","gov.house、BLS 2026-11-17查"),
}
CLAIMS_EXP="11/19已公布（截至11/14当周）：初请实际20.3万（预期约19.7–19.8万：路透调查37位经济学家中位数19.7万，区间19.0–20.5万；Investing.com 19.8万；IBKR 11/18亦称约19.7万；前值上修至20.2万，原报20.0万），四周均值19.775万（前值上修至19.575万，原报19.525万）；续请（截至11/7）176.3万（预期171.0万，前值下修至169.3万，原报169.7万），投保失业率1.1%持平，四周均值171.7万。下一期已确认提前至周三11/25 08:30 ET（FRED发布日历已列）——DOL官网（USDL 26-1722-NAT）、Investing.com、路透/IBKR、FRED 2026-11-20查"
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
stamp=datetime(2026,11,20,1,15,tzinfo=ZoneInfo("UTC"))
def mk(uid,title,s,e,desc,allday):
    x=Event(); x.add("uid",uid); x.add("dtstamp",stamp); x.add("summary",title); x.add("dtstart",s); x.add("dtend",e); x.add("description",desc)
    if allday: x.add("transp","TRANSPARENT")
    return x
for c,u,t,s,e,d,a in ev:
    t,d=addexp(u,t,d,c); cal.add_component(mk(u,t,s,e,d,a))
# jobless claims
cn="美国劳工部(DOL)每周四08:30 ET发布；节假日可能调整"
x=mk("claims-weekly-est@investing","美国初请失业金人数",datetime(2026,11,5,21,30,tzinfo=SH),datetime(2026,11,5,22,0,tzinfo=SH),"美东时间: 每周四 08:30 ET（冬令时=北京21:30）\n"+cn+"\n感恩节周改为周三11/25（FRED发布日历已列）\n来源: "+DOL+"\n预期："+CLAIMS_EXP+"\n预期更新于 2026-11-20",False)
x.add("rrule",{"freq":"weekly","byday":"TH","until":datetime(2027,3,11,13,30,tzinfo=ZoneInfo("UTC"))}); x.add("exdate",datetime(2026,11,26,21,30,tzinfo=SH)); cal.add_component(x)
x=mk("claims-weekly-edt@investing","美国初请失业金人数",datetime(2027,3,18,20,30,tzinfo=SH),datetime(2027,3,18,21,0,tzinfo=SH),"美东时间: 每周四 08:30 ET（夏令时=北京20:30）\n"+cn+"\n来源: "+DOL,False)
x.add("rrule",{"freq":"weekly","byday":"TH","until":datetime(2027,3,25,12,30,tzinfo=ZoneInfo("UTC"))}); cal.add_component(x)
T("宏观","claims-20261125@investing","美国初请失业金人数（感恩节提前至周三）",(2026,11,25),(8,30),DOL,"FRED发布日历（Unemployment Insurance Weekly Claims，rid=180；注明日期来自数据源）已列出周三11/25 07:30 CT（=08:30 ET）发布；Investing.com经济日历亦已列该日。周四11/26为感恩节休市，每周四重复事件已排除该日")
_c,_u,_t,_s,_e,_d,_a=ev[-1]; _t,_d=addexp(_u,_t,_d,_c); cal.add_component(mk(_u,_t,_s,_e,_d,_a))
cal.add_missing_timezones()
open("Investing.ics","wb").write(cal.to_ical())
c2=Calendar.from_ical(open("Investing.ics","rb").read()); vs=c2.walk("VEVENT")
uids=[str(v["uid"]) for v in vs]; assert len(uids)==len(set(uids))
from collections import Counter; print(len(vs),Counter(e[0] for e in ev)+Counter({"宏观(初请重复)":2}))
for c,u,t,s,e,d,a in sorted(ev,key=lambda z:str(z[3])):
    if str(s)[:10]<="2026-11-27": print(str(s)[:16],t)
