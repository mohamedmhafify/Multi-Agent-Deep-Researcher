import streamlit as st
from graph import research_agent

st.set_page_config(page_title="Multi-Agent Researcher", page_icon="🕵️‍♂️")

st.title("🕵️‍♂️ Multi-Agent Deep Researcher")
st.markdown("أدخل موضوع البحث، وسيقوم فريق من الوكلاء الأذكياء (مدير، باحث، كاتب، مراجع) بإعداد تقرير شامل لك.")

query = st.text_input("ما هو الموضوع الذي تريد البحث عنه؟")

if st.button("بدء البحث العيق 🚀"):
    if query:
        with st.spinner("فريق العمل يقوم بالبحث والمراجعة... الرجاء الانتظار ⏳"):
            # بندي ID مختلف لكل بحث عشان الـ Redis يفصل بينهم
            thread_id = query[:10].replace(" ", "_") 
            config = {"configurable": {"thread_id": thread_id}}
            
            final_state = research_agent.invoke({
                "query": query,
                "research_data": [],
                "revision_count": 0
            }, config=config)
            
            st.success("✅ تم الانتهاء من التقرير بنجاح!")
            st.markdown("---")
            st.markdown(final_state.get("draft", "حدث خطأ أثناء كتابة التقرير."))
    else:
        st.warning("يرجى إدخال موضوع للبحث أولاً.")