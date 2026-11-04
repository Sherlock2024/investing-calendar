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
    n="2027年GDP估算轮次按BEA惯例推断，日期与时间以BEA官方JSON为准" if d[0]==2027 else ""
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
EXP_NEW="2026-11-04"
REFRESHED={"er-aapl-20261102@investing","er-amd-20261103@investing","jolts-20261103@investing","isms-20261104@investing","nfp-20261106@investing","cpi-20261110@investing","fomc-stmt-20261209@investing","fomc-stmt-20270127@investing","er-nvda-20261117@investing"}
EXP={
"er-aapl-20261102@investing":("（实际EPS $2.10/营收$1144.8亿；预期$1.99/$1134亿）","已公布：FQ4营收$1144.8亿（+12% YoY，高于一致预期约$1134亿）、EPS $2.10（+14% YoY，高于一致预期$1.99）；iPhone销售强劲但大中华区营收低于预期。赛前一致预期：营收约$1133–1134亿，EPS $1.98–1.99","Apple Newsroom、MarketBeat、Investing.com、Yahoo Finance 2026-11-04查"),
"er-amd-20261103@investing":("（实际EPS $2.09/营收$133.8亿；预期$1.95/$130.9亿）","已公布（11/3盘后）：Q3营收$133.77亿（+45% YoY，一致预期约$130.6–130.9亿），调整后EPS $2.09（+74% YoY，一致预期$1.94–1.95），GAAP EPS $1.46；数据中心营收创纪录$85亿（+97%，预期$82亿）；Q4指引营收约$170亿±3%（分析师预期$162.3亿），非GAAP毛利率约55%；CEO称2027年营收增长超80%（分析师预期77%）；财报后盘后股价约+8%","AMD IR新闻稿、CNBC(LSEG)、Reuters/Investing.com 2026-11-04查"),
"er-nvda-20261117@investing":("（预期EPS ~$2.47/营收~$1090亿）","一致预期：营收约$1088–1114亿（最常引用约$1088–1090亿；个别源$1113.6亿），EPS $2.47–2.53（最常引用$2.47）；公司指引营收$1080亿±2%，毛利率74%±0.5pt","MarketBeat、Theta Research、FN2、ChartMill、hulicalendar、NVIDIA IR 2026-11-04查"),
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
"fomc-stmt-20261209@investing":("（市场押注加息25bp，概率约77–80%）","当前目标区间3.75%–4.00%（10/28以10-2投票维持不变，Cook、Hammack异议支持加息）。CME FedWatch（11/4 06:05北京时间转引）：加息25bp至4.00%–4.25%概率78.9%、维持21.1%；其他快照：Gate转引CME 76.9%（Nov 4早间，中期选举后由70%升至76.9%）、growbeansprout 77.4%、联邦基金期货法约80%、Kalshi约76–77%。降息概率约1%。期货隐含会后有效利率约4.08%（较当前+约20bp）。圣路易斯联储Musalem称“需尽快进一步加息”，达拉斯联储Logan称至少还需加息两次各25bp","CME FedWatch(经5iter/AiCoin 11/4转引)、Gate News、cdes.com、growbeansprout、Kalshi 2026-11-04查"),
"fomc-stmt-20270127@investing":("","CME FedWatch（11/4 06:05转引）：至1月累计维持不变15.3%、累计加息25bp（4.00%–4.25%）63.0%、累计加息50bp 21.8%（累计至少加息25bp约84.8%）","CME FedWatch(经5iter/AiCoin 11/4转引) 2026-11-04查（远期）"),
"fomc-stmt-20270317@investing":("","市场隐含3月会后利率约4.28%（Fisclear），最可能区间4.25%–4.50%（FinBoss约60%，4.00%–4.25%约40%）","Fisclear、FinBoss(基于CME联邦基金期货) 2026-11-03查（远期）"),
"nfp-20261106@investing":("（预期 +5.5~6万）","一致预期：非农约+5.5万（mrkts/Wells Fargo汇总共识约+5.5~6万），各机构：BofA +7.5万（高于共识）、Wells Fargo +6.5万、Continuum +5万、KPMG +4.5万；前值+2.9万（9月，远低于预期+8.4万）。失业率预期4.2%（前值4.2%；BofA称若劳动参与率降幅更大可能降至4.1%）；平均时薪环比预期+0.3%（Continuum +0.2%；前值+0.1%），同比预期2.8–2.9%（前值3.0%）；周工时预期34.4小时（Continuum 34.3）。11/6 20:30北京时间公布","mrkts.gg、Wells Fargo Economics Week Ahead(10/30)、eFXdata引BofA(11/3)、KPMG、Continuum Economics 2026-11-04查"),
"jolts-20261103@investing":("（实际752.3万/预期716万）","已公布：9月职位空缺752.3万（预期约715–716万，Dow Jones 715万、Econoday 716万、Reuters 710万；8月上修至719.0万），环比+33.3万，职位空缺率4.5%；离职人数336.5万（18个月新高）、招聘540.2万、裁员164.1万（自2025年3月以来最低）。每1名失业者对应约1.05个空缺。10月JOLTS将于12/1公布","BLS、CNBC、Econoday(CME)、Quartz 2026-11-04查"),
"ismm-20261102@investing":("（实际55.5/预期54.6）","已公布：10月制造业PMI 55.5（一致预期54.6，前值54.5），连续第10个月扩张；价格支付指数75.2（预期77.0，前值77.9）；就业52.4（预期53.0）；新订单55.5","Sigmanomics经济日历、FXStreet 2026-11-03查"),
"isms-20261104@investing":("（预期 54.8）","一致预期：54.8（FX Blue/Makkler；部分源54.5；Continuum 55.0；Wells Fargo 54.0；前值54.9）；价格支付预期约75（Continuum；前值74.0）；就业预期约50（前值50.1）。Polymarket市场押注最集中于55.0–55.9区间。北京时间今晚23:00公布，本次更新(19:00)时尚未发布","FX Blue、Makkler、for-ex.news、Continuum Economics(11/3)、Wells Fargo、Polymarket 2026-11-04查"),
"cpi-20261110@investing":("（预期核心环比+0.2%）","暂无统一的权威共识（11/4仍未形成）。10月CPI环比：Continuum +0.2%（0.24%）、TD +0.30%、克利夫兰联储Nowcast +0.24%、Kalshi隐含约+0.28%；核心CPI环比：Continuum +0.2%（0.22%）、TD +0.21%、克利夫兰联储 +0.21%、Macrogauge综合预测0.25%（个别预测0.20%–0.34%）。同比：克利夫兰联储Nowcast 3.74%（核心2.48%）、Nowflation预测3.82%；Continuum按对比2025年9月测算约3.9%（核心2.8%）（2025年10月因政府停摆无CPI数据）。前值：环比+0.6%/同比3.7%，核心环比+0.3%","Continuum Economics、TD Securities(Octa转引)、Macrogauge、Prediction.com(引TD/Kalshi)、Cleveland Fed Nowcasting、Nowflation 2026-11-04查"),
}
CLAIMS_EXP="11/5（截至10/31当周）一致预期：初请19.6万（前值19.4万；gov.house模型11/3为19.5万，80%区间18.3–20.7万），续请约171.0万（前值170.1万，11/3数据）——来源: Briefing.com、Helious、for-ex.news、gov.house 2026-11-04查；之后各周：预期：暂无（临近时更新）"
def addexp(uid,title,desc,cat):
    if uid in EXP:
        suf,txt,src=EXP[uid]
        return title+suf, desc+f"\n预期：{txt}\n预期来源: {src}\n预期更新于 {EXP_NEW if uid in REFRESHED else EXP_DATE}"
    if cat in("宏观","财报") or uid.startswith("fomc-stmt"):
        return title, desc+"\n预期：暂无（临近时更新）"
    return title,desc
cal=Calendar(); cal.add("prodid","-//Investing//sherlock//CN"); cal.add("version","2.0"); cal.add("calscale","GREGORIAN")
cal.add("x-wr-calname","Investing"); cal.add("x-wr-timezone","Asia/Shanghai")
stamp=datetime(2026,11,4,10,50,tzinfo=ZoneInfo("UTC"))
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
    if str(s)<"2026-11-17" or str(s)[:10]<="2026-11-16": print(str(s)[:16],t)
