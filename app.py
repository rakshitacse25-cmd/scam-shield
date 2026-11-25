import io
import os

import requests
import streamlit as st
from mutagen import File as AudioFile

DETECT_URL = "https://platform.detectif.ai/v1/deepfake/detect"
API_KEY = os.environ.get("DETECTIF_API_KEY", "")
MIN_SEC, MAX_SEC = 4, 120

st.set_page_config(page_title="Scam Shield", page_icon="🛡️")
st.title("🛡️ Scam Shield")
st.write(
    "Got a suspicious voice note asking for money? Upload it and we'll check "
    "whether the voice may be AI-generated."
)
st.caption("Only upload clips you have permission to check.")

if not API_KEY:
    st.error("DETECTIF_API_KEY is not set. Set it and restart the app.")
    st.stop()

uploaded = st.file_uploader(
    "Upload a voice note (4 to 120 seconds)",
    type=["wav", "mp3", "ogg", "m4a", "opus"],
)

if uploaded:
    audio_bytes = uploaded.getvalue()
    st.audio(audio_bytes)

    duration = None
    try:
        info = AudioFile(io.BytesIO(audio_bytes))
        duration = info.info.length if info else None
    except Exception:
        pass

    if duration is not None and not (MIN_SEC <= duration <= MAX_SEC):
        st.warning(
            f"Your clip is {duration:.1f} seconds. Please upload audio "
            f"between {MIN_SEC} and {MAX_SEC} seconds."
        )
    elif st.button("Check this voice"):
        with st.spinner("Checking the voice..."):
            try:
                r = requests.post(
                    DETECT_URL,
                    headers={"Authorization": f"Bearer {API_KEY}"},
                    files={"file": (uploaded.name, audio_bytes)},
                    timeout=60,
                )
                r.raise_for_status()
                data = r.json()
            except requests.HTTPError as e:
                if e.response is not None and e.response.status_code == 422:
                    st.warning(
                        "This clip could not be processed. Please upload clear "
                        "audio between 4 and 120 seconds."
                    )
                else:
                    st.error(f"Could not check the clip: {e}")
                st.info("If this is urgent, call the person directly to verify.")
                st.stop()
            except Exception as e:
                st.error(f"Could not check the clip: {e}")
                st.info("If this is urgent, call the person directly to verify.")
                st.stop()

        result = data.get("result", {})
        label = str(result.get("label", "unknown"))
        score = result.get("score")
        threshold = result.get("threshold")

        if result.get("is_synthetic") is True:
            st.error(f"⚠️ Result: {label}. This voice may be AI-generated.")
        elif result.get("is_synthetic") is False:
            st.success(f"✅ Result: {label}. No sign of AI generation found.")
        else:
            st.warning(f"Result: {label}")

        if score is not None:
            st.metric("Score (higher means more likely AI)", f"{score:.2f}")
        if threshold is not None:
            st.caption(f"Decision threshold: {threshold}")

        st.info(
            "This is evidence, not proof. Background noise and poor audio "
            "quality can affect the result."
        )
        st.subheader("What to do next")
        st.markdown(
            "- Call the person back on a number you already have saved.\n"
            "- Ask a question only they would know.\n"
            "- Do not send money or share OTPs until you confirm."
        )

        with st.expander("Raw response"):
            st.json(data)

st.divider()
st.subheader("How to spot voice scams")
st.markdown(
    "- Urgent requests for money or OTPs\n"
    "- Caller asks you to keep it secret\n"
    "- Unknown number claiming to be family\n"
    "- Pressure to act right now"
)
