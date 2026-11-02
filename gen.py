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
T("财报","er-jpm-20270114@investing","摩根大通财报 Q4（盘前）",(2027,1,14),(6,45),"https://www.jpmorganchase.com/ir","公司已确认：约06:45 ET发布，电话会08:30 ET",dur=105)
for d,co,tm,code in [((2026,12,10),"博通","盘后","avgo"),((2026,12,14),"甲骨文","盘后","orcl"),((2026,12,23),"美光","盘后","mu"),((2027,1,14),"台积电","美股盘前","tsm"),((2027,1,14),"摩根士丹利","盘前","ms"),((2027,1,19),"高盛","盘前","gs"),((2027,1,19),"奈飞","盘后","nflx"),((2027,1,27),"微软","盘后","msft"),((2027,1,27),"特斯拉","盘后","tsla"),((2027,1,27),"Meta","盘后","meta"),((2027,1,28),"英特尔","盘后","intc"),((2027,2,3),"谷歌Alphabet","盘后","googl"),((2027,2,4),"亚马逊","盘后","amzn")]:
    A("财报",f"er-{code}-%04d%02d%02d"%d+"@investing",f"(预计) {co}财报（{tm}）",d,AF+"%04d-%02d"%d[:2]+" ; https://www.wallstreethorizon.com","公司尚未确认，日期为第三方财报日历预测，可能变动。注意：美东盘后≈北京时间次日早晨")
cal=Calendar(); cal.add("prodid","-//Investing//sherlock//CN"); cal.add("version","2.0"); cal.add("calscale","GREGORIAN")
cal.add("x-wr-calname","Investing"); cal.add("x-wr-timezone","Asia/Shanghai")
stamp=datetime(2026,11,2,4,0,tzinfo=ZoneInfo("UTC"))
def mk(uid,title,s,e,desc,allday):
    x=Event(); x.add("uid",uid); x.add("dtstamp",stamp); x.add("summary",title); x.add("dtstart",s); x.add("dtend",e); x.add("description",desc)
    if allday: x.add("transp","TRANSPARENT")
    return x
for c,u,t,s,e,d,a in ev: cal.add_component(mk(u,t,s,e,d,a))
# jobless claims
cn="美国劳工部(DOL)每周四08:30 ET发布；节假日可能调整"
x=mk("claims-weekly-est@investing","美国初请失业金人数",datetime(2026,11,5,21,30,tzinfo=SH),datetime(2026,11,5,22,0,tzinfo=SH),"美东时间: 每周四 08:30 ET（冬令时=北京21:30）\n"+cn+"\n感恩节周预计改为周三11/25\n来源: "+DOL,False)
x.add("rrule",{"freq":"weekly","byday":"TH","until":datetime(2027,3,11,13,30,tzinfo=ZoneInfo("UTC"))}); x.add("exdate",datetime(2026,11,26,21,30,tzinfo=SH)); cal.add_component(x)
x=mk("claims-weekly-edt@investing","美国初请失业金人数",datetime(2027,3,18,20,30,tzinfo=SH),datetime(2027,3,18,21,0,tzinfo=SH),"美东时间: 每周四 08:30 ET（夏令时=北京20:30）\n"+cn+"\n来源: "+DOL,False)
x.add("rrule",{"freq":"weekly","byday":"TH","until":datetime(2027,3,25,12,30,tzinfo=ZoneInfo("UTC"))}); cal.add_component(x)
T("宏观","claims-20261125@investing","(预计) 美国初请失业金人数（感恩节提前）",(2026,11,25),(8,30),DOL,"感恩节周按惯例提前至周三，待DOL确认")
cal.add_component(mk(*ev[-1][1:]))
cal.add_missing_timezones()
open("Investing.ics","wb").write(cal.to_ical())
c2=Calendar.from_ical(open("Investing.ics","rb").read()); vs=c2.walk("VEVENT")
uids=[str(v["uid"]) for v in vs]; assert len(uids)==len(set(uids))
from collections import Counter; print(len(vs),Counter(e[0] for e in ev)+Counter({"宏观(初请重复)":2}))
for c,u,t,s,e,d,a in sorted(ev,key=lambda z:str(z[3])):
    if str(s)<"2026-11-17" or str(s)[:10]<="2026-11-16": print(str(s)[:16],t)
