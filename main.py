import streamlit as st
from agent import moderate_text, get_rag_response, load_config
from rag import RAG

st.title("Content Firewall ")
config = load_config()
rag_pipe = RAG("policies/", top_k=config['rag']['top_k']) if config['rag']['enabled'] else None

input_text = st.text_area("Paste text for compliance check:")

if st.button("Analyze"):
    st.subheader("Moderation Results")
    mod_outs = moderate_text(input_text, config['moderation'])
    for k, v in mod_outs.items():
        st.write(f"**{k}:** {v}")

    if rag_pipe:
        st.subheader("Policy Evaluation")
        rag_out = get_rag_response(input_text, rag_pipe)
        st.write(f"**Policy Check:** {rag_out['policy_check']}")
        st.write(f"**Citations:** {rag_out['citations']}")

st.markdown("----")
st.markdown("Logs and trace available in console for debugging.")
