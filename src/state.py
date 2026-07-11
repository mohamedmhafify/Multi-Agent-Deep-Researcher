from typing import TypedDict, List, Annotated
import operator

#1- هنا بنعمل ملف مشترك علشان الايجنتس هيباصو لبعض فيه
class ResearchState(TypedDict): 
    query: str # سؤال المستخدم
    plan: List[str] # الاسئلة الي بلانر بيحطها
    research_data: Annotated[List[str], operator.add] # الداتا الي الريشيرشر بيجمعها عن الاسئلة
    draft: str # المكان الي الكاتب بيكتب فيه
    feedback: str # زي ميتا داتا او تعليقات المراجع
    revision_count: int # عدد مرات التعديل علشان منخشش في حلقة مفرغة
    