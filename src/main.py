from graph import research_agent

if __name__ == "__main__":
    query = "What are the latest developments in generative AI and Agentic AI in 2026?"
    
    # 1. بنحدد الـ ID بتاع التقرير
    thread_id = "report_001"
    config = {"configurable": {"thread_id": thread_id}}
    
    print(f"🚀 Starting task: {query}\n" + "="*50)

    # 2. بنسأل الـ Redis: هل التقرير ده موجود قبل كده؟
    # الفانكشن دي بتجيب آخر حالة اتسجلت للـ Thread ده
    state_history = research_agent.get_state(config)
    
    # لو الـ State مش فاضية، وفيها مفتاح 'draft' (يعني الكاتب خلص شغله قبل كده)
    if state_history and state_history.values and "draft" in state_history.values:
        print("⚡ تم العثور على التقرير في الذاكرة (Redis Cache)! جاري الاسترجاع بدون إعادة بحث...")
        print("="*50 + "\nالتقرير النهائي:\n")
        print(state_history.values["draft"])
        
    else:
        # لو التقرير مش موجود أو مكملش، نشغل الـ Agents من الصفر
        print("🆕 لم يتم العثور على تقرير سابق. سيقوم الفريق بالبحث وكتابته الآن...")
        
        final_state = research_agent.invoke({
            "query": query,
            "research_data": [],
            "revision_count": 0
        }, config=config)

        print("="*50 + "\nالتقرير النهائي:\n")
        print(final_state.get("draft", "لم يتم إنشاء مسودة."))